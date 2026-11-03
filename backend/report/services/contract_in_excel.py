import openpyxl
from openpyxl.styles import Border, Side, Alignment, PatternFill, Font
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from datetime import datetime
import os

from django.conf import settings
from django.db.models import Count, Q, Prefetch

from contracts.models.models import (
    Contract,
    ContractBorder,
    ContractBorderAttachment,
)
from accounts.models import User

from common.utils import to_jalali, to_jalali_datetime


def get_display_name(u):
    if u.first_name_fa and u.last_name_fa:
        return f'{u.first_name_fa} {u.last_name_fa}'
    return u.username


# ── Border helpers ─────────────────────────────────────────────────────────────

def _apply_border_range(ws, min_row, min_col, max_row, max_col, border):
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            ws.cell(row=r, column=c).border = border


def _write_merged(ws, min_row, min_col, max_row, max_col,
                  value, font, fill, alignment, border):
    if not (min_row == max_row and min_col == max_col):
        ws.merge_cells(
            start_row=min_row, start_column=min_col,
            end_row=max_row,   end_column=max_col,
        )
    anchor = ws.cell(row=min_row, column=min_col, value=value)
    anchor.font      = font
    anchor.alignment = alignment
    if fill:
        anchor.fill = fill
    _apply_border_range(ws, min_row, min_col, max_row, max_col, border)


# ── RTL-aware alignment constructors ──────────────────────────────────────────

def _align_center():
    return Alignment(horizontal="center", vertical="center",
                     wrap_text=True, readingOrder=2)

def _align_right():
    return Alignment(horizontal="right", vertical="center",
                     wrap_text=True, readingOrder=2)

def _align_left():
    return Alignment(horizontal="left", vertical="center",
                     wrap_text=True, readingOrder=2)


def create_excel_form_contract_summary(contractid, user) -> str | None:
    try:
        # ── Single consolidated DB fetch ───────────────────────────────────────
        # Attachments are prefetched INSIDE the ContractBorder queryset so that
        # to_attr='_borders' (a plain list) does not break the nested prefetch path.
        contract = Contract.objects.prefetch_related(
            'company',
            Prefetch(
                'users_with_access_contracts',
                queryset=User.objects.filter(
                    Q(roles__title='مجری') | Q(is_controller=True)
                ),
                to_attr='_supervisor_list',
            ),
            Prefetch(
                'rcontractborders',
                queryset=ContractBorder.objects.defer('border').annotate(
                    total_layers=Count('rcontractborderlayers'),
                    uploaded_count=Count(
                        'rcontractborderlayers',
                        filter=Q(rcontractborderlayers__is_uploaded=True),
                    ),
                    verified_count=Count(
                        'rcontractborderlayers',
                        filter=Q(rcontractborderlayers__is_verified=True),
                    ),
                ).prefetch_related(
                    Prefetch(
                        'rcontractborderattachment',
                        queryset=ContractBorderAttachment.objects.select_related('dtyp').order_by('upload_date'),
                        to_attr='_attachments',
                    )
                ),
                to_attr='_borders',
            ),
        ).get(pk=contractid)

        # ── Pre-compute everything from prefetched data (zero extra DB hits) ───
        companies     = contract.company.all()
        company_names = '، '.join(c.name for c in companies) if companies else 'نامشخص'

        contract_num = contract.number or 'ندارد'

        if contract.start_date and contract.end_date:
            contract_date = f'{to_jalali(contract.start_date)} تا {to_jalali(contract.end_date)}'
        elif contract.start_date:
            contract_date = to_jalali(contract.start_date)
        else:
            contract_date = 'تعریف نشده'

        status_text = 'خاتمه یافته' if contract.is_completed else 'جاری'

        supervisor_names = (
            '، '.join(get_display_name(u) for u in contract._supervisor_list)
            if contract._supervisor_list else 'تعریف نشده'
        )

        contract_borders = contract._borders  # plain list — no DB hit

        # Flatten attachments from all borders — no DB hit
        all_attachments = [
            att
            for cb in contract_borders
            for att in cb._attachments
        ]

        # Cache logo existence once — avoids repeated filesystem stat
        logo_path   = os.path.join(settings.BASE_DIR, 'report', 'images', 'ipclogo.png')
        logo_exists = os.path.exists(logo_path)

        # ══════════════════════════════════════════════════════════════════════
        # Excel workbook setup
        # ══════════════════════════════════════════════════════════════════════
        wb = openpyxl.Workbook()
        wb.remove(wb.active)
        ws = wb.create_sheet(title="گزارش قرارداد")
        ws.sheet_view.rightToLeft = True

        # ── Shared styles ──────────────────────────────────────────────────────
        thin_side   = Side(style="thin",   color="000000")
        medium_side = Side(style="medium", color="2F5496")
        THIN  = Border(left=thin_side,   right=thin_side,
                       top=thin_side,    bottom=thin_side)
        THICK = Border(left=medium_side, right=medium_side,
                       top=medium_side,  bottom=medium_side)  # noqa: F841

        def _font(bold=False, size=11, color="000000"):
            return Font(name='B Nazanin', bold=bold, size=size, color=color)

        def _fill(hex_color):
            return PatternFill(start_color=hex_color, end_color=hex_color,
                               fill_type="solid")

        FILL_DARK   = _fill("1F3864")
        FILL_BLUE   = _fill("2F5496")
        FILL_LIGHT  = _fill("D6E4F0")
        FILL_HEADER = _fill("EBF3FB")

        # ── Column widths A–E ──────────────────────────────────────────────────
        for i, w in enumerate([20, 28, 22, 20, 22], start=1):
            ws.column_dimensions[get_column_letter(i)].width = w

        row = 1

        # ══════════════════════════════════════════════════════════════════════
        # HEADER BLOCK  (rows 1-3):  logo | title | date & preparer
        # ══════════════════════════════════════════════════════════════════════
        LOGO_ROWS = 3
        for r in range(1, LOGO_ROWS + 1):
            ws.row_dimensions[r].height = 22
            for c in range(1, 6):
                cell = ws.cell(row=r, column=c)
                cell.fill   = FILL_HEADER
                cell.border = THIN

        # Logo  A1:B3
        ws.merge_cells(start_row=1, start_column=1,
                       end_row=LOGO_ROWS, end_column=2)
        _apply_border_range(ws, 1, 1, LOGO_ROWS, 2, THIN)

        if logo_exists:
            img        = XLImage(logo_path)
            img.width  = 80
            img.height = 55
            img.anchor = 'A1'
            ws.add_image(img)
        else:
            ph = ws.cell(row=1, column=1, value='[ logo ]')
            ph.font      = _font(bold=True, size=9, color="888888")
            ph.alignment = _align_center()

        # Centre label  C1:C3
        ws.merge_cells(start_row=1, start_column=3,
                       end_row=LOGO_ROWS, end_column=3)
        _apply_border_range(ws, 1, 3, LOGO_ROWS, 3, THIN)
        lbl = ws.cell(row=1, column=3, value='خلاصه گزارش قرارداد')
        lbl.font      = _font(bold=True, size=11, color="1F3864")
        lbl.fill      = FILL_HEADER
        lbl.alignment = _align_center()

        # Date  D1:E1  /  Preparer  D2:E2  /  blank  D3:E3
        report_date   = to_jalali(datetime.now().date())
        preparer_name = get_display_name(user)

        for r, text in [(1, f'تاریخ گزارش: {report_date}'),
                        (2, f'تهیه‌کننده: {preparer_name}')]:
            ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
            _apply_border_range(ws, r, 4, r, 5, THIN)
            mc = ws.cell(row=r, column=4, value=text)
            mc.font      = _font(size=9, color="444444")
            mc.fill      = FILL_HEADER
            mc.alignment = _align_right()

        ws.merge_cells(start_row=3, start_column=4, end_row=3, end_column=5)
        _apply_border_range(ws, 3, 4, 3, 5, THIN)

        row = LOGO_ROWS + 1

        # ── Contract title  A:E ────────────────────────────────────────────────
        ws.row_dimensions[row].height = 28
        _write_merged(ws, row, 1, row, 5,
                      contract.title,
                      _font(bold=True, size=14, color="FFFFFF"),
                      FILL_DARK, _align_center(), THIN)
        row += 1

        # Spacer
        ws.row_dimensions[row].height = 6
        _apply_border_range(ws, row, 1, row, 5, THIN)
        row += 1

        # ══════════════════════════════════════════════════════════════════════
        # SECTION 1 — General contract info
        # ══════════════════════════════════════════════════════════════════════
        ws.row_dimensions[row].height = 22
        _write_merged(ws, row, 1, row, 5,
                      'اطلاعات کلی قرارداد',
                      _font(bold=True, size=12, color="FFFFFF"),
                      FILL_DARK, _align_center(), THIN)
        row += 1

        # Column headers
        ws.row_dimensions[row].height = 20
        for col_idx, h in enumerate(
            ['وضعیت', 'ناظرین', 'تاریخ قرارداد', 'شماره قرارداد', 'شرکت'],
            start=1,
        ):
            c = ws.cell(row=row, column=col_idx, value=h)
            c.font      = _font(bold=True, size=11, color="FFFFFF")
            c.fill      = FILL_BLUE
            c.alignment = _align_center()
            c.border    = THIN
        row += 1

        # Data values
        ws.row_dimensions[row].height = 20
        for col_idx, val in enumerate(
            [status_text, supervisor_names, contract_date, contract_num, company_names],
            start=1,
        ):
            c = ws.cell(row=row, column=col_idx, value=val)
            c.font      = _font(size=11)
            c.alignment = _align_center()
            c.border    = THIN
        row += 1

        # Spacer
        ws.row_dimensions[row].height = 6
        _apply_border_range(ws, row, 1, row, 5, THIN)
        row += 1

        # ══════════════════════════════════════════════════════════════════════
        # SECTION 2 — ShrhLayer table
        # Uses DB-annotated counts — no Python iteration over layer objects
        # ══════════════════════════════════════════════════════════════════════
        ws.row_dimensions[row].height = 22
        _write_merged(ws, row, 1, row, 5,
                      'لایه‌های شرح خدمات',
                      _font(bold=True, size=12, color="FFFFFF"),
                      FILL_DARK, _align_center(), THIN)
        row += 1

        LAYER_SPANS = [(1, 2), (3, 4), (5, 5)]
        LAYER_HDRS  = ['محدوده قرارداد', 'بارگذاری شده', 'تایید شده']

        if contract_borders:
            ws.row_dimensions[row].height = 20
            for (sc, ec), h in zip(LAYER_SPANS, LAYER_HDRS):
                _write_merged(ws, row, sc, row, ec, h,
                              _font(bold=True, size=11),
                              FILL_LIGHT, _align_center(), THIN)
            row += 1

            for cb in contract_borders:
                ws.row_dimensions[row].height = 18
                for (sc, ec), val in zip(
                    LAYER_SPANS,
                    [cb.title,
                     f'{cb.uploaded_count} از {cb.total_layers}',
                     f'{cb.verified_count} از {cb.total_layers}'],
                ):
                    _write_merged(ws, row, sc, row, ec, val,
                                  _font(size=11), None, _align_center(), THIN)
                row += 1
        else:
            ws.row_dimensions[row].height = 18
            _write_merged(ws, row, 1, row, 5,
                          'هیچ محدوده قراردادی برای این قرارداد ثبت نشده است.',
                          _font(size=11), None, _align_center(), THIN)
            row += 1

        # Spacer
        ws.row_dimensions[row].height = 6
        _apply_border_range(ws, row, 1, row, 5, THIN)
        row += 1

        # ══════════════════════════════════════════════════════════════════════
        # SECTION 3 — ContractBorder Attachments
        # Uses pre-flattened all_attachments — no extra DB hit
        # ══════════════════════════════════════════════════════════════════════
        ws.row_dimensions[row].height = 22
        _write_merged(ws, row, 1, row, 5,
                      'پیوست‌های محدوده‌های قرارداد',
                      _font(bold=True, size=12, color="FFFFFF"),
                      FILL_DARK, _align_center(), THIN)
        row += 1

        ATT_SPANS = [(1, 3), (4, 5)]
        ATT_HDRS  = ['عنوان', 'تاریخ بارگذاری']

        if all_attachments:
            ws.row_dimensions[row].height = 20
            for (sc, ec), h in zip(ATT_SPANS, ATT_HDRS):
                _write_merged(ws, row, sc, row, ec, h,
                              _font(bold=True, size=11),
                              FILL_LIGHT, _align_center(), THIN)
            row += 1

            for attachment in all_attachments:
                try:
                    file_name = (os.path.basename(attachment.file.name)
                                 if attachment.file else 'بدون فایل')
                except ValueError:
                    # Django raises ValueError when accessing .name on an empty FileField
                    file_name = 'بدون فایل'

                date_text = to_jalali_datetime(attachment.upload_date) if attachment.upload_date else 'نامشخص'

                ws.row_dimensions[row].height = 18
                for (sc, ec), val in zip(ATT_SPANS, [file_name, date_text]):
                    _write_merged(ws, row, sc, row, ec, val,
                                  _font(size=11), None, _align_center(), THIN)
                row += 1
        else:
            ws.row_dimensions[row].height = 18
            _write_merged(ws, row, 1, row, 5,
                          'هیچ پیوستی برای محدوده‌های این قرارداد ثبت نشده است.',
                          _font(size=11), None, _align_center(), THIN)
        
        # Make sure row pointer is fresh after Section 3 (handles the
        # "no attachments" else-branch which doesn't increment row itself)
        row += 1

        # Spacer
        ws.row_dimensions[row].height = 6
        _apply_border_range(ws, row, 1, row, 5, THIN)
        row += 1

        # ══════════════════════════════════════════════════════════════════════
        # SECTION 4 — Signatures
        # ══════════════════════════════════════════════════════════════════════
        ws.row_dimensions[row].height = 22
        _write_merged(ws, row, 1, row, 5,
                      'امضاها',
                      _font(bold=True, size=12, color="FFFFFF"),
                      FILL_DARK, _align_center(), THIN)
        row += 1

        # Two signature squares side by side, touching (no gap column)
        SIGN_HEIGHT = 5  # number of rows tall each square will be
        sign_start_row = row
        sign_end_row   = row + SIGN_HEIGHT - 1

        for r in range(sign_start_row, sign_end_row + 1):
            ws.row_dimensions[r].height = 20

        # Right square (columns A-B) — امضا مشاور — no fill
        _write_merged(ws, sign_start_row, 1, sign_end_row, 2,
                      'امضا مشاور',
                      _font(bold=True, size=11),
                      None, _align_center(), THIN)

        # Left square (columns C-E) — امضا کارفرما — no fill, starts right after the first box
        _write_merged(ws, sign_start_row, 3, sign_end_row, 5,
                      'امضا مجری',
                      _font(bold=True, size=11),
                      None, _align_center(), THIN)

        row = sign_end_row + 1
        
        # ── Save ───────────────────────────────────────────────────────────────
        reports_dir = os.path.join(settings.MEDIA_ROOT, "contract_excel_summary_reports")
        os.makedirs(reports_dir, exist_ok=True)
        filename  = f'contract_report_{contract.pk}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        file_path = os.path.join(reports_dir, filename)
        wb.save(file_path)

        return os.path.join("contract_excel_summary_reports", filename)

    except Contract.DoesNotExist:
        print(f'contract with this id {contractid} does not exist')
    except Exception as e:
        print(f'Error generating report: {str(e)}')
        import traceback
        traceback.print_exc()