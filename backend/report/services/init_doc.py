import os
import uuid
from typing import Iterable, Union

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from initialborders.models.models import InitialBorder
from initialborders.models.attachment import InitialBorderAttachment
from contracts.models.models import (
    ContractBorder,
    Contract,
)
from contracts.models.attachment import (
    ContractAttachment,
    ContractBorderAttachment,
)
from contracts.models.SharhKhadamats import (
    ShrhLayer,
    ShrhBase
)
from layers.models.models import (
    FeatureAttachment
)
from layers.apps import LayersConfig  # اپ‌کانفیگ اپی که جداول داینامیک عوارض در آن هستند
from layers.utils import get_model_from_string  # همان تابعی که در ویوی FeatureAttachment استفاده شده


# مقادیر خام "نوع داده" (doc / vector / raster) معمولا به انگلیسی در دیتابیس ذخیره می‌شوند.
# این دیکشنری فقط برای نمایش بهتر در گزارش است؛ اگر مقدار ناشناخته بود، همان مقدار خام چاپ می‌شود.
DATA_TYPE_FA_MAP = {
    "doc": "سند (Doc)",
    "document": "سند (Doc)",
    "vector": "وکتور (Vector)",
    "raster": "رستر (Raster)",
}


# ==================== ROW TYPE (ستون «نوع ردیف») ====================
# هر ردیف گزارش از یکی از این منابع می‌آید. از ثابت (به‌جای رشته خام) استفاده
# می‌کنیم تا اشتباه تایپی رخ ندهد و تغییر برچسب/رنگ در آینده فقط در یک‌جا
# (ROW_TYPE_STYLES) انجام شود.
ROW_TYPE_INITIALBORDER_ATTACHMENT = "initialborder_attachment"
ROW_TYPE_CONTRACT_ATTACHMENT = "contract_attachment"
ROW_TYPE_CONTRACTBORDER_ATTACHMENT = "contractborder_attachment"
ROW_TYPE_FEATURE_ATTACHMENT = "feature_attachment"
ROW_TYPE_VECTOR_LAYER = "vector_layer"
ROW_TYPE_RASTER_LAYER = "raster_layer"

# برچسب فارسی + رنگ پس‌زمینه‌ی روشن هر نوع ردیف (برای جداسازی بصری سطرها در گزارش).
# label می‌تواند شامل placeholder باشد (مثل {object_id}) که با .format() پر می‌شود.
ROW_TYPE_STYLES = {
    ROW_TYPE_INITIALBORDER_ATTACHMENT: {
        "label": "پیوست محدوده اولیه",
        "color": "DDEBF7",  # آبی روشن
    },
    ROW_TYPE_CONTRACTBORDER_ATTACHMENT: {
        "label": "پیوست محدوده قرارداد",
        "color": "FCE4D6",  # نارنجی روشن
    },
    ROW_TYPE_CONTRACT_ATTACHMENT: {
        "label": "پیوست قرارداد",
        "color": "E2EFDA",  # سبز روشن
    },
    ROW_TYPE_FEATURE_ATTACHMENT: {
        "label": "پیوست عارضه شماره {object_id}",
        "color": "FFF2CC",  # زرد روشن
    },
    ROW_TYPE_VECTOR_LAYER: {
        "label": "لایه وکتوری",
        "color": "E4DFEC",  # بنفش روشن
    },
    ROW_TYPE_RASTER_LAYER: {
        "label": "لایه رستری",
        "color": "F2DCDB",  # صورتی روشن
    },
}


def _get_data_type_label(raw_value) -> str:
    if not raw_value:
        return "نامشخص"
    return DATA_TYPE_FA_MAP.get(str(raw_value).strip().lower(), str(raw_value))


def _get_row_type_style(kind: str, **label_kwargs):
    """
    برای یک نوع ردیف (kind)، برچسب فارسی و کد رنگ پس‌زمینه را برمی‌گرداند.
    label_kwargs برای پرکردن placeholder داخل برچسب استفاده می‌شود
    (مثلا object_id برای پیوست عارضه).
    """
    style = ROW_TYPE_STYLES.get(kind)
    if not style:
        return kind or "نامشخص", None
    label = style["label"].format(**label_kwargs) if label_kwargs else style["label"]
    return label, style["color"]


def _format_file_size(size_bytes) -> str:
    if size_bytes is None:
        return "—"

    size_bytes = float(size_bytes)
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size_bytes < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size_bytes)} {unit}"
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

    return "—"


def _calc_row_height(text, col_width, line_height=15, min_height=20):
    """
    تخمین تعداد خطوطی که یک متن با wrap_text در یک ستون با عرض مشخص اشغال می‌کند
    و بر اساس آن، ارتفاع مناسب سطر را برمی‌گرداند. این یک تخمین است نه محاسبه دقیق فونت.
    """
    if not text:
        return min_height

    text = str(text)
    chars_per_line = max(int(col_width * 1.8), 1)  # فاکتور تجربی برای فونت پیش‌فرض
    wrap_lines = -(-len(text) // chars_per_line)  # سقف تقسیم (ceil)
    explicit_lines = text.count("\n") + 1
    total_lines = max(wrap_lines, explicit_lines) + 4

    return max(min_height, total_lines * line_height)


def create_excel_from_initialborder_attachments(
    initialborders: Union[InitialBorder, Iterable[InitialBorder]]
) -> str:
    """
    برای یک queryset (یا هر iterable) از محدوده‌های اولیه، یک فایل اکسل واحد می‌سازد.
    به ازای هر محدوده اولیه، یک بلاک کامل (تیتر + هدر جدول + ردیف‌های همان محدوده)
    نوشته می‌شود و بلاک محدوده‌ی اولیه‌ی بعدی، درست زیر آن (با یک سطر خالی فاصله،
    در همان شیت) می‌آید.

    هر بلاک شامل همان چیزی است که قبلا برای یک محدوده اولیه ساخته می‌شد:
      - پیوست‌های خود محدوده اولیه          -> InitialBorderAttachment
      - پیوست‌های قراردادهای مرتبط با آن     -> ContractAttachment
      - پیوست‌های محدوده‌های قراردادِ مرتبط   -> ContractBorderAttachment
      - لایه‌های بارگذاری‌شده (وکتور/رستر) هر محدوده قرارداد
      - پیوست‌های عارضه‌ای (FeatureAttachment) روی عوارض هر لایه

    Args:
        initialborders: یک queryset یا هر iterable از نمونه‌های InitialBorder.
            برای سازگاری با کد قدیمی، یک نمونه‌ی تکی InitialBorder هم پذیرفته
            می‌شود و به‌صورت خودکار به یک لیست تک‌عضوی تبدیل می‌شود.

    خروجی: مسیر نسبی فایل ساخته‌شده (نسبت به MEDIA_ROOT)
    """

    # سازگاری با کد قدیمی: اگر یک نمونه‌ی تکی داده شد، آن را به لیست تک‌عضوی تبدیل کن.
    # در غیر این صورت (queryset/لیست/هر iterable دیگر) آن را یک‌بار به لیست تبدیل
    # می‌کنیم تا هم بتوانیم طولش را بگیریم و هم چند بار (برای هر initialborder) پیمایشش کنیم.
    if isinstance(initialborders, InitialBorder):
        initialborders = [initialborders]
    else:
        initialborders = list(initialborders)

    if not initialborders:
        raise ValueError("initialborders نمی‌تواند خالی باشد.")

    wb = openpyxl.Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)
    ws = wb.create_sheet(title="گزارش پیوست‌ها")
    ws.sheet_view.rightToLeft = True

    # --- Styles (یک‌بار برای کل فایل ساخته می‌شوند و بین همه‌ی بلاک‌ها مشترک‌اند) ---
    header_font = Font(bold=True, size=11, color="FFFFFF")
    header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    title_font = Font(bold=True, size=14, color="FFFFFF")
    title_fill = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
    title_alignment = Alignment(horizontal="center", vertical="center")

    value_alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    row_type_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    row_type_font = Font(bold=True, size=10)

    thin_side = Side(style="thin", color="000000")
    thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    table_headers = [
        "عنوان محدوده اولیه",
        "عنوان قرارداد",
        "شماره قرارداد",
        "نوع داده",
        "نوع ردیف",
        "نام فایل",
        "حجم فایل",
        "توضیحات",
    ]
    col_letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    col_widths = [28, 30, 20, 16, 24, 45, 16, 50]
    # به ازای هر ستون، تراز و فونت اختصاصی (None یعنی از مقدار پیش‌فرض استفاده شود)
    col_alignments = [
        value_alignment, value_alignment, value_alignment, value_alignment,
        row_type_alignment, value_alignment, value_alignment, value_alignment,
    ]
    col_fonts = [None, None, None, None, row_type_font, None, None, None]

    for col_letter, width in zip(col_letters, col_widths):
        ws.column_dimensions[col_letter].width = width

    last_col = col_letters[-1]

    # ==================== HELPERS (مشترک بین تمام بلاک‌ها) ====================
    def write_block_title(r, initialborder_title):
        ws.merge_cells(f"A{r}:{last_col}{r}")
        cell = ws[f"A{r}"]
        cell.value = f"گزارش پیوست‌های محدوده اولیه «{initialborder_title}»"
        cell.font = title_font
        cell.fill = title_fill
        cell.alignment = title_alignment
        cell.border = thin_border
        ws.row_dimensions[r].height = 30

    def write_table_header(r):
        for col_index, header in enumerate(table_headers):
            c = ws[f"{col_letters[col_index]}{r}"]
            c.value = header
            c.font = header_font
            c.fill = header_fill
            c.alignment = header_alignment
            c.border = thin_border
        ws.row_dimensions[r].height = 22

    def write_row(
        r,
        initialborder_title,
        contract_title,
        contract_number,
        data_type_raw,
        row_type_kind,
        description,
        file_name=None,
        file_size=None,
        **row_type_kwargs,
    ):
        """
        یک سطر از گزارش را می‌نویسد.
        file_name و file_size فقط برای ردیف‌های مربوط به پیوست‌ها پر می‌شوند؛
        برای ردیف‌های لایه (وکتور/رستر) مقدار آن‌ها None است.
        """
        row_type_label, row_type_color = _get_row_type_style(row_type_kind, **row_type_kwargs)
        row_fill = (
            PatternFill(start_color=row_type_color, end_color=row_type_color, fill_type="solid")
            if row_type_color else None
        )

        values = [
            initialborder_title or "نامشخص",
            contract_title or "—",
            contract_number or "—",
            _get_data_type_label(data_type_raw),
            row_type_label,
            file_name or "—",
            _format_file_size(file_size),
            description or "—",
        ]

        for col_index, value in enumerate(values):
            c = ws[f"{col_letters[col_index]}{r}"]
            c.value = value
            c.alignment = col_alignments[col_index]
            c.border = thin_border
            if col_fonts[col_index] is not None:
                c.font = col_fonts[col_index]
            if row_fill is not None:
                c.fill = row_fill

        needed_height = max(
            _calc_row_height(value, col_widths[col_index])
            for col_index, value in enumerate(values)
        )
        ws.row_dimensions[r].height = needed_height

    def write_not_found_row(r):
        ws.merge_cells(f"A{r}:{last_col}{r}")
        cell = ws[f"A{r}"]
        cell.value = "هیچ پیوستی برای این محدوده اولیه و قراردادهای مرتبط با آن یافت نشد."
        cell.alignment = title_alignment
        cell.border = thin_border
        ws.row_dimensions[r].height = 20

    # ==================== یک بلاک به‌ازای هر محدوده اولیه ====================
    row = 1

    for initialborder in initialborders:
        write_block_title(row, initialborder.title)
        row += 1

        write_table_header(row)
        row += 1

        has_any_row = False
        content_type_cache = {}  # model_class -> ContentType، برای جلوگیری از کوئری تکراری

        # --- پیوست‌های خود محدوده اولیه ---
        initialborder_attachments = initialborder.rinitialborderachment.select_related("dtyp_attach").all()
        for attachment in initialborder_attachments:
            has_any_row = True
            data_type_raw = attachment.dtyp_attach.category if attachment.dtyp_attach else None
            write_row(
                row,
                initialborder.title,
                None,
                None,
                data_type_raw,
                ROW_TYPE_INITIALBORDER_ATTACHMENT,
                "این پیوست برای تمامی قراردادهای این محدوده اولیه مشترک است.",
                file_name=attachment.file.name,
                file_size=attachment.file.size,
            )
            row += 1

        # --- قراردادهای مرتبط با این محدوده اولیه ---
        contracts = Contract.objects.filter(
            rcontractborders__initborder=initialborder
        ).distinct()

        for contract in contracts:

            # --- پیوست‌های سطح قرارداد ---
            contract_attachments = contract.rcontractattachment.select_related("dtyp").all()
            for attachment in contract_attachments:
                has_any_row = True
                data_type_raw = attachment.dtyp.typ if attachment.dtyp else None
                write_row(
                    row,
                    initialborder.title,
                    contract.title,
                    contract.number,
                    data_type_raw,
                    ROW_TYPE_CONTRACT_ATTACHMENT,
                    None,
                    file_name=attachment.file.name,
                    file_size=attachment.file.size,
                )
                row += 1

            # --- پیوست‌های سطح محدوده قرارداد (فقط محدوده‌های مربوط به همین محدوده اولیه) ---
            contract_borders = ContractBorder.objects.filter(
                contract=contract,
                initborder=initialborder,
            ).prefetch_related(
                "rcontractborderattachment__dtyp",
                "rcontractborderlayers__layer_name",
            )

            for contract_border in contract_borders:
                for attachment in contract_border.rcontractborderattachment.all():
                    has_any_row = True
                    data_type_raw = attachment.dtyp.typ if attachment.dtyp else None
                    write_row(
                        row,
                        initialborder.title,
                        contract.title,
                        contract.number,
                        data_type_raw,
                        ROW_TYPE_CONTRACTBORDER_ATTACHMENT,
                        f"مربوط به محدوده قرارداد «{contract_border.title}».",
                        file_name=attachment.file.name,
                        file_size=attachment.file.size,
                    )
                    row += 1

                # --- لایه‌های بارگذاری‌شده این محدوده قرارداد (وکتور/رستر) ---
                uploaded_layers = [
                    layer for layer in contract_border.rcontractborderlayers.all()
                    if layer.is_uploaded
                ]
                for layer in uploaded_layers:
                    has_any_row = True
                    is_raster = bool(layer.raster_uuid)
                    data_type_raw = "raster" if is_raster else "vector"
                    row_type_kind = ROW_TYPE_RASTER_LAYER if is_raster else ROW_TYPE_VECTOR_LAYER

                    if layer.layer_name:
                        lyrgroup_fa = layer.layer_name.lyrgroup_fa or "نامشخص"
                        layername_fa = layer.layer_name.layername_fa or "نامشخص"
                    else:
                        lyrgroup_fa = "نامشخص"
                        layername_fa = "نامشخص"

                    write_row(
                        row,
                        initialborder.title,
                        contract.title,
                        contract.number,
                        data_type_raw,
                        row_type_kind,
                        f"لایه «{layername_fa}» از گروه «{lyrgroup_fa}» "
                        f"در محدوده قرارداد «{contract_border.title}».",
                    )
                    row += 1

                    # --- پیوست‌های عارضه‌ای (FeatureAttachment) روی تک‌تک عوارضِ همین لایه ---
                    layername_en = layer.layer_name.layername_en if layer.layer_name else None
                    if not layername_en:
                        continue

                    try:
                        model_class = get_model_from_string(
                            model_app_label=LayersConfig.name,
                            model_class_name=layername_en,
                        )
                    except Exception as exc:
                        # جدول عارضه‌ی این لایه پیدا نشد (خطا)؛ از این لایه صرف‌نظر می‌شود
                        print(
                            f"[create_excel_from_initialborder_attachments] "
                            f"دریافت مدل لایه «{layername_en}» با خطا مواجه شد: {exc}"
                        )
                        continue

                    if model_class is None:
                        # get_model_from_string به‌جای raise کردن، در برخی موارد
                        # فقط پیام چاپ می‌کند و None برمی‌گرداند؛ این حالت را هم
                        # صریحا هندل می‌کنیم تا AttributeError نگیریم.
                        print(
                            f"[create_excel_from_initialborder_attachments] "
                            f"مدل لایه «{layername_en}» در اپ «{LayersConfig.name}» یافت نشد؛ "
                            f"این لایه از گزارش صرف‌نظر می‌شود."
                        )
                        continue

                    feature_ids = list(
                        model_class.objects.filter(shr_layer=layer).values_list("pk", flat=True)
                    )
                    if not feature_ids:
                        continue

                    if model_class not in content_type_cache:
                        content_type_cache[model_class] = ContentType.objects.get_for_model(model_class)
                    content_type = content_type_cache[model_class]

                    feature_attachments = FeatureAttachment.objects.filter(
                        content_type=content_type,
                        object_id__in=feature_ids,
                    ).select_related("writer")

                    for f_attachment in feature_attachments:
                        has_any_row = True
                        description = f"از لایه «{layername_fa}» گروه «{lyrgroup_fa}»."
                        if f_attachment.description:
                            description += f" توضیح پیوست: {f_attachment.description}"

                        write_row(
                            row,
                            initialborder.title,
                            contract.title,
                            contract.number,
                            "doc",
                            ROW_TYPE_FEATURE_ATTACHMENT,
                            description,
                            object_id=f_attachment.object_id,
                            # نکته: اینجا باید فایل خودِ پیوست عارضه (f_attachment) گزارش شود،
                            # نه آخرین attachment محدوده قرارداد از حلقه‌ی قبلی.
                            file_name=f_attachment.file.name,
                            file_size=f_attachment.file.size,
                        )
                        row += 1

        if not has_any_row:
            write_not_found_row(row)
            row += 1

        # یک سطر خالی به‌عنوان فاصله‌ی بصری بین بلاک این محدوده اولیه و بلاک بعدی
        row += 1

    # ==================== SAVE ====================
    reports_dir = os.path.join(settings.MEDIA_ROOT, "initialborder_attachment_reports")
    os.makedirs(reports_dir, exist_ok=True)

    if len(initialborders) == 1:
        filename = f"initialborder_{initialborders[0].pk}_attachments_{uuid.uuid4().hex[:8]}.xlsx"
    else:
        filename = f"initialborders_batch_{len(initialborders)}_attachments_{uuid.uuid4().hex[:8]}.xlsx"

    file_path = os.path.join(reports_dir, filename)
    wb.save(file_path)

    return os.path.join("initialborder_attachment_reports", filename)