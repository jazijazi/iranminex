import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Sum , Q , Prefetch
from django.db.models.expressions import RawSQL
from docx import Document
from docx.shared import Pt, RGBColor , Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from initialborders.models.models import InitialBorder, InitialBorderDomin
from initialborders.models.attachment import InitialBorderAttachment , InitialBorderAttachmentDomain
from contracts.models.models import Contract, ContractBorder
from common.models import Company , Province
from accounts.models import User

from initialborders.models.models import (
    InitialBorder,
    InitialBorderDomin,
)
from contracts.models.models import (
    Contract,
    ContractBorderAttachment,
    ContractDomin,
    ContractBorder,
    ShrhLayer,
    ShrhBase,
)
from datetime import datetime

def add_rtl_paragraph(document, text, style=None, alignment=WD_ALIGN_PARAGRAPH.LEFT, bold=False, font_size=11):
    """Add a paragraph with RTL (Right-to-Left) support for Persian text"""
    paragraph = document.add_paragraph(text, style=style)
    paragraph.alignment = alignment
    
    # Set RTL direction
    pPr = paragraph._element.get_or_add_pPr()
    bidi_element = OxmlElement('w:bidi')
    pPr.append(bidi_element)
    
    # Format the run
    for run in paragraph.runs:
        rPr = run._element.get_or_add_rPr()
        
        # Set font name via XML directly
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), 'B Nazanin')
        rFonts.set(qn('w:hAnsi'), 'B Nazanin')
        rFonts.set(qn('w:eastAsia'), 'B Nazanin')
        rFonts.set(qn('w:cs'), 'B Nazanin')
        rPr.insert(0, rFonts)
        
        # Set bold via XML directly
        if bold:
            b = OxmlElement('w:b')
            bCs = OxmlElement('w:bCs')
            rPr.append(b)
            rPr.append(bCs)
        
        # Set font size via XML directly (half-points, so multiply by 2)
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), str(font_size * 2))
        szCs = OxmlElement('w:szCs')  # font size for complex scripts (RTL/Persian)
        szCs.set(qn('w:val'), str(font_size * 2))
        rPr.append(sz)
        rPr.append(szCs)
    
    return paragraph

def add_page_border(document):
    for section in document.sections:
        sectPr = section._sectPr

        # Remove existing borders
        for el in sectPr.findall(qn('w:pgBdr')):
            sectPr.remove(el)

        # Create border container
        pgBdr = OxmlElement('w:pgBdr')
        pgBdr.set(qn('w:offsetFrom'), 'page')  # important

        # Create borders
        for side in ['top', 'left', 'bottom', 'right']:
            border = OxmlElement(f'w:{side}')
            border.set(qn('w:val'), 'single')
            border.set(qn('w:sz'), '24')
            border.set(qn('w:space'), '20')
            border.set(qn('w:color'), '000000')
            pgBdr.append(border)

        # Append to section properties
        sectPr.append(pgBdr)

def add_document_header(document, report_date, preparer_name):
    """Add a professional 3-column header to every page"""
    for section in document.sections:
        section.different_first_page_header_footer = False
        header = section.header

        # Clear existing header content
        for para in header.paragraphs:
            p = para._element
            p.getparent().remove(p)

        # ── Header table ───────────────────────────────────────────────────
        header_table = header.add_table(rows=1, cols=3, width=Pt(0))
        # header_table.style = 'Table Normal'  # ← change from 'Table Grid'

        # Set total table width
        tbl   = header_table._tbl
        tblPr = tbl.find(qn('w:tblPr'))
        if tblPr is None:
            tblPr = OxmlElement('w:tblPr')
            tbl.insert(0, tblPr)

        tblW = OxmlElement('w:tblW')
        tblW.set(qn('w:w'), '8400')
        tblW.set(qn('w:type'), 'dxa')
        tblPr.append(tblW)

        # Remove all table borders — must come after style is set
        tblBorders = OxmlElement('w:tblBorders')
        for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            b = OxmlElement(f'w:{side}')
            b.set(qn('w:val'),   'none')
            b.set(qn('w:sz'),    '0')
            b.set(qn('w:space'), '0')
            b.set(qn('w:color'), 'auto')
            tblBorders.append(b)
        tblPr.append(tblBorders)

        # Also remove borders on each cell individually
        row        = header_table.rows[0]
        col_widths = [1800, 4800, 1800]
        for idx, cell in enumerate(row.cells):
            tc   = cell._tc
            tcPr = tc.find(qn('w:tcPr'))
            if tcPr is None:
                tcPr = OxmlElement('w:tcPr')
                tc.insert(0, tcPr)

            # Cell width
            tcW = OxmlElement('w:tcW')
            tcW.set(qn('w:w'),    str(col_widths[idx]))
            tcW.set(qn('w:type'), 'dxa')
            tcPr.append(tcW)

            # Cell borders — none on every side
            tcBorders = OxmlElement('w:tcBorders')
            for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                b = OxmlElement(f'w:{side}')
                b.set(qn('w:val'),   'none')
                b.set(qn('w:sz'),    '0')
                b.set(qn('w:space'), '0')
                b.set(qn('w:color'), 'auto')
                tcBorders.append(b)
            tcPr.append(tcBorders)

        left_cell   = row.cells[0]
        middle_cell = row.cells[1]
        right_cell  = row.cells[2]

        # ── Left cell: logo ────────────────────────────────────────────────
        logo_path = os.path.join(settings.BASE_DIR, 'report', 'images', 'ipclogo.png')
        left_para = left_cell.paragraphs[0]
        left_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if os.path.exists(logo_path):
            logo_run = left_para.add_run()
            logo_run.add_picture(logo_path, width=Inches(1.1))
        else:
            print(f'[WARNING] Logo not found at: {logo_path}')
            left_para.add_run('[ logo ]')

        # ── Middle cell: report title ──────────────────────────────────────
        mid_tc   = middle_cell._tc
        mid_tcPr = mid_tc.find(qn('w:tcPr'))
        if mid_tcPr is None:
            mid_tcPr = OxmlElement('w:tcPr')
            mid_tc.insert(0, mid_tcPr)
        vAlign = OxmlElement('w:vAlign')
        vAlign.set(qn('w:val'), 'center')
        mid_tcPr.append(vAlign)

        mid_para = middle_cell.paragraphs[0]
        mid_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pPr_mid = mid_para._element.get_or_add_pPr()
        pPr_mid.append(OxmlElement('w:bidi'))
        mid_run      = mid_para.add_run('خلاصه گزارش قرارداد')
        mid_run.bold = True
        mid_run.font.size = Pt(10)
        rPr_mid  = mid_run._element.get_or_add_rPr()
        rFonts_m = OxmlElement('w:rFonts')
        rFonts_m.set(qn('w:ascii'), 'B Nazanin')
        rFonts_m.set(qn('w:hAnsi'), 'B Nazanin')
        rFonts_m.set(qn('w:cs'),    'B Nazanin')
        rPr_mid.insert(0, rFonts_m)

        # ── Right cell: date (line 1) and preparer (line 2) ────────────────
        right_tc   = right_cell._tc
        right_tcPr = right_tc.find(qn('w:tcPr'))
        if right_tcPr is None:
            right_tcPr = OxmlElement('w:tcPr')
            right_tc.insert(0, right_tcPr)
        vAlign_right = OxmlElement('w:vAlign')
        vAlign_right.set(qn('w:val'), 'center')
        right_tcPr.append(vAlign_right)

        def add_right_line(paragraph, text):
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pPr = paragraph._element.get_or_add_pPr()
            pPr.append(OxmlElement('w:bidi'))
            run = paragraph.add_run(text)
            run.font.size = Pt(8)
            rPr    = run._element.get_or_add_rPr()
            rFonts = OxmlElement('w:rFonts')
            rFonts.set(qn('w:ascii'), 'B Nazanin')
            rFonts.set(qn('w:hAnsi'), 'B Nazanin')
            rFonts.set(qn('w:cs'),    'B Nazanin')
            rPr.insert(0, rFonts)
            # force complex script (Persian) size to match
            sz = OxmlElement('w:sz')
            sz.set(qn('w:val'), '16')    # 8pt × 2 = 16 half-points
            szCs = OxmlElement('w:szCs')
            szCs.set(qn('w:val'), '16')
            rPr.append(sz)
            rPr.append(szCs)

        add_right_line(right_cell.paragraphs[0], f'تاریخ گزارش: {report_date}')
        add_right_line(right_cell.add_paragraph(), f'تهیه کننده: {preparer_name}')

        # ── Separator line under header ────────────────────────────────────
        sep_para = header.add_paragraph()
        pPr_sep  = sep_para._element.get_or_add_pPr()

        # Minimize vertical space the paragraph occupies
        spacing = OxmlElement('w:spacing')
        spacing.set(qn('w:before'), '0')
        spacing.set(qn('w:after'),  '0')
        spacing.set(qn('w:line'),   '120')   # minimum line height (half-points)
        spacing.set(qn('w:lineRule'), 'exact')
        pPr_sep.append(spacing)

        pBdr  = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'),   'single')
        bottom.set(qn('w:sz'),    '6')
        bottom.set(qn('w:space'), '4')
        bottom.set(qn('w:color'), '000000')
        pBdr.append(bottom)
        pPr_sep.append(pBdr)




def get_display_name(u):
            if u.first_name_fa and u.last_name_fa:
                return f'{u.first_name_fa} {u.last_name_fa}'
            return u.username

def create_word_form_contract_summary(
    contractid,
    user,
) -> str | None:
    
    try:
        contract: Contract = Contract.objects.get(pk=contractid)

        # Create document
        document = Document()

        # Set document direction to RTL (A4)
        sections = document.sections
        for section in sections:
            section.page_height = Pt(842)
            section.page_width = Pt(595)

        # ── Page Border ────────────────────────────────────────────────────────
        add_page_border(document)

        # ── Logo Header ────────────────────────────────────────────────────────
        # ── Document Header (logo + title + date/preparer) ─────────────────────
        report_date   = datetime.now().strftime("%Y/%m/%d")
        preparer_name = get_display_name(user)
        add_document_header(document, report_date=report_date, preparer_name=preparer_name)
        
        # document.add_paragraph()  # spacing after header

        # ── Title ──────────────────────────────────────────────────────────────
        add_rtl_paragraph(
            document=document,
            text=f'{contract.title}',
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
            font_size=14,
        )

        document.add_paragraph()  # Empty line

        # ── Contract Summary Table ─────────────────────────────────────────────
        companies = contract.company.all()
        company_names = '، '.join([c.name for c in companies]) if companies.exists() else 'نامشخص'

        contract_number = contract.number if contract.number else 'ندارد'

        if contract.start_date and contract.end_date:
            contract_date = f'{contract.start_date} تا {contract.end_date}'
        elif contract.start_date:
            contract_date = str(contract.start_date)
        else:
            contract_date = 'تعریف نشده'

        status_text = 'خاتمه یافته' if contract.is_completed else 'جاری'

        supervisor_users = contract.users_with_access_contracts.filter(
            Q(roles__title='مجری') | Q(is_controller=True)
        ).select_related('roles')

        supervisor_names = '، '.join([get_display_name(u) for u in supervisor_users]) if supervisor_users.exists() else 'تعریف نشده'


        # ── Create table ──────────────────────────────────────────────────────
        table = document.add_table(rows=1, cols=5)
        table.style = 'Light Grid Accent 1'

        headers = [
            'وضعیت',
            'ناظرین',
            'تاریخ قرارداد',
            'شماره قرارداد',
            'شرکت',
        ]

        # ── Header row ────────────────────────────────────────────────────────
        hdr_cells = table.rows[0].cells

        for i, header in enumerate(headers):
            cell = hdr_cells[i]
            cell.text = header

            # 👉 Vertical center
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            vAlign = OxmlElement('w:vAlign')
            vAlign.set(qn('w:val'), 'center')
            tcPr.append(vAlign)

            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pPr = paragraph._element.get_or_add_pPr()
                pPr.append(OxmlElement('w:bidi'))

                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.name = 'B Nazanin'
                    run.font.size = Pt(12)


        # ── Data row ──────────────────────────────────────────────────────────
        row_cells = table.add_row().cells

        values = [
            status_text,
            supervisor_names,
            contract_date,
            contract_number,
            company_names,
        ]

        for i, value in enumerate(values):
            cell = row_cells[i]
            cell.text = value

            # 👉 Vertical center
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            vAlign = OxmlElement('w:vAlign')
            vAlign.set(qn('w:val'), 'center')
            tcPr.append(vAlign)

            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pPr = paragraph._element.get_or_add_pPr()
                pPr.append(OxmlElement('w:bidi'))

                for run in paragraph.runs:
                    run.font.name = 'B Nazanin'
                    run.font.size = Pt(11) 
        
        # ── ShrhLayer Table ────────────────────────────────────────────────────
        
        document.add_paragraph()
        add_rtl_paragraph(document, 'لایه‌های شرح خدمات', bold=True, font_size=12 , alignment=WD_ALIGN_PARAGRAPH.CENTER,)

        contract_borders = ContractBorder.objects.filter(
            contract=contract
        ).prefetch_related(
            Prefetch(
                'rcontractborderlayers',
                queryset=ShrhLayer.objects.all(),
                to_attr='all_layers'
            )
        )

        if contract_borders.exists():
            table = document.add_table(rows=1, cols=3)
            table.style = 'Light Grid Accent 1'

            # Header row
            hdr_cells = table.rows[0].cells
            headers = [
                'تایید شده',
                'بارگذاری شده',
                'محدوده قرارداد',
            ]

            for idx, header in enumerate(headers):
                hdr_cells[idx].text = header
                for paragraph in hdr_cells[idx].paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    pPr = paragraph._element.get_or_add_pPr()
                    bidi_element = OxmlElement('w:bidi')
                    pPr.append(bidi_element)
                    for run in paragraph.runs:
                        run.font.bold = True
                        run.font.name = 'B Nazanin'
                        run.font.size = Pt(12)

            # Data rows — one row per ContractBorder
            for cb in contract_borders:
                layers = cb.all_layers  # already fetched, no extra query
                total = len(layers)
                uploaded_count = sum(1 for l in layers if l.is_uploaded)
                verified_count = sum(1 for l in layers if l.is_verified)

                row_cells = table.add_row().cells
                row_cells[0].text = f'{verified_count} از {total}'
                row_cells[1].text = f'{uploaded_count} از {total}'
                row_cells[2].text = cb.title

                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        pPr = paragraph._element.get_or_add_pPr()
                        bidi_element = OxmlElement('w:bidi')
                        pPr.append(bidi_element)
                        for run in paragraph.runs:
                            run.font.name = 'B Nazanin'
                            run.font.size = Pt(10)

        else:
            add_rtl_paragraph(document, 'هیچ محدوده قراردادی برای این قرارداد ثبت نشده است.')

        # ── ContractBorder Attachments Table ───────────────────────────────────
        document.add_paragraph()
        add_rtl_paragraph(document, 'پیوست‌های محدوده‌های قرارداد', bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, font_size=14)

        attachments = ContractBorderAttachment.objects.filter(
            contractborder__contract=contract
        ).select_related('contractborder', 'dtyp').order_by('contractborder__title', 'upload_date')

        if attachments.exists():
            table = document.add_table(rows=1, cols=2)
            table.style = 'Light Grid Accent 1'

            # Header row
            hdr_cells = table.rows[0].cells
            headers = [ 'تاریخ بارگذاری' , 'عنوان']

            for idx, header in enumerate(headers):
                hdr_cells[idx].text = header
                for paragraph in hdr_cells[idx].paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    pPr = paragraph._element.get_or_add_pPr()
                    bidi_element = OxmlElement('w:bidi')
                    pPr.append(bidi_element)
                    for run in paragraph.runs:
                        run.font.bold = True
                        run.font.name = 'B Nazanin'
                        run.font.size = Pt(11)

            # Data rows
            for attachment in attachments:
                row_cells = table.add_row().cells

                # Extract filename from the file field path
                file_name = os.path.basename(attachment.file.name) if attachment.file else 'بدون فایل'

                upload_date_text = attachment.upload_date.strftime("%Y/%m/%d - %H:%M") if attachment.upload_date else 'نامشخص'

                row_cells[0].text = upload_date_text
                row_cells[1].text = file_name 

                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        pPr = paragraph._element.get_or_add_pPr()
                        bidi_element = OxmlElement('w:bidi')
                        pPr.append(bidi_element)
                        for run in paragraph.runs:
                            run.font.name = 'B Nazanin'
                            run.font.size = Pt(9)

        else:
            add_rtl_paragraph(document, 'هیچ پیوستی برای محدوده‌های این قرارداد ثبت نشده است.')


        # ── Save ───────────────────────────────────────────────────────────────
        reports_dir = os.path.join(settings.MEDIA_ROOT, "contract_word_summary_reports")
        os.makedirs(reports_dir, exist_ok=True)

        filename = f'contract_report_{contract.pk}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx'
        file_path = os.path.join(reports_dir, filename)

        document.save(file_path)

        print(f'Report generated successfully: {file_path}')
        return os.path.join("contract_word_summary_reports", filename)

    except Contract.DoesNotExist:
        print(f'contract with this id {contractid} does not exist')
    except Exception as e:
        print(f'Error generating report: {str(e)}')
        import traceback
        traceback.print_exc()
