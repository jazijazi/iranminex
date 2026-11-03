import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Sum
from django.db.models.expressions import RawSQL
from docx import Document
from docx.shared import Pt, RGBColor
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

def create_word_from_initialborder_summary(
        initialborderid: InitialBorder,
) -> str|None:
    
    try:
        initialborder_instance : InitialBorder = InitialBorder.objects.get(pk=initialborderid)

        # Create document
        document = Document()
            
        # Set document direction to RTL
        sections = document.sections
        for section in sections:
            section.page_height = Pt(842)  # A4 height
            section.page_width = Pt(595)   # A4 width
            
        # Add title
        add_rtl_paragraph(
            document = document, 
            text = f'خلاصه گزارش محدوده اولیه: {initialborder_instance.title}',
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
            font_size=16
        )
            
        document.add_paragraph()  # Empty line
            
        # Add basic information            
        dtyp_text = f'نوع محدوده: {initialborder_instance.dtyp.title}' if initialborder_instance.dtyp else 'نوع محدوده: تعریف نشده'
        parent_text = f'محدوده والد: {initialborder_instance.parentid.title}' if initialborder_instance.parentid else 'محدوده والد: ندارد'
        add_rtl_paragraph(document, f'{dtyp_text} | {parent_text}')

        ###############################################################################################
        # Contracts part - Summary Table
        add_rtl_paragraph(document, 'خلاصه قراردادهای مرتبط', bold=True, font_size=14)
        
        # Get all contract borders for this initial border
        contract_borders = ContractBorder.objects.filter(
            initborder=initialborder_instance
        ).select_related('contract', 'contract__dtyp').prefetch_related('contract__company')
        
        if contract_borders.exists():
            # Create summary table
            table = document.add_table(rows=1, cols=5)
            table.style = 'Light Grid Accent 1'
            
            # Header row
            hdr_cells = table.rows[0].cells
            headers = ['عنوان قرارداد', 'شماره قرارداد', 'شرکت', 'لایه‌های تایید شده', 'وضعیت']
            
            for idx, header in enumerate(headers):
                hdr_cells[idx].text = header
                # Format header with RTL
                for paragraph in hdr_cells[idx].paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    pPr = paragraph._element.get_or_add_pPr()
                    bidi_element = OxmlElement('w:bidi')
                    pPr.append(bidi_element)
                    for run in paragraph.runs:
                        run.font.bold = True
                        run.font.name = 'B Nazanin'
                        run.font.size = Pt(11)
            
            # Get unique contracts
            processed_contracts = set()
            contract_data = []
            
            for cb in contract_borders:
                contract = cb.contract
                if contract.pk in processed_contracts:
                    continue
                processed_contracts.add(contract.pk)
                
                # Get all companies names for this contract
                companies = contract.company.all()
                company_names = '، '.join([company.name for company in companies]) if companies.exists() else 'نامشخص'
                
                # Count all ShrhLayers for this contract through ShrhBase
                all_layers_count = ShrhLayer.objects.filter(
                    shrh_base__contract=contract
                ).count()
                
                # Count verified ShrhLayers (is_verified = True)
                verified_layers_count = ShrhLayer.objects.filter(
                    shrh_base__contract=contract,
                    is_verified=True
                ).count()
                
                # Contract status
                status = 'خاتمه یافته' if contract.is_completed else f'در حال اجرا ({contract.progress}%)'
                
                contract_data.append({
                    'contract': contract,
                    'company_names': company_names,
                    'all_layers': all_layers_count,
                    'verified_layers': verified_layers_count,
                    'status': status
                })
            
            # Add rows to table
            for data in contract_data:
                row_cells = table.add_row().cells
                row_cells[0].text = data['contract'].title if data['contract'].title else 'بدون عنوان'
                row_cells[1].text = data['contract'].number if data['contract'].number else 'بدون شماره'
                row_cells[2].text = data['company_names']
                row_cells[3].text = f"{data['verified_layers']} از {data['all_layers']}"
                row_cells[4].text = data['status']
                
                # Format cells with RTL and center alignment
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
            add_rtl_paragraph(document, 'هیچ قرارداد مرتبطی برای این محدوده ثبت نشده است.')

        ###############################################################################################
        # Add footer
        document.add_paragraph()
        add_rtl_paragraph(document, '─' * 50, alignment=WD_ALIGN_PARAGRAPH.CENTER)
        add_rtl_paragraph(
            document, 
            f'تاریخ تولید گزارش: {datetime.now().strftime("%Y/%m/%d - %H:%M")}',
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            font_size=8
        )
        
        reports_dir = os.path.join(settings.MEDIA_ROOT, "init_word_summary_reports")
        os.makedirs(reports_dir, exist_ok=True)

        filename = f'initialborder_report_{initialborder_instance.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx'
        file_path = os.path.join(reports_dir, filename)

        document.save(file_path)

        file_path = os.path.join(reports_dir, filename)

        print(f'Report generated successfully: {file_path}')
        # return file_path

        return os.path.join("init_word_summary_reports", filename)


    except InitialBorder.DoesNotExist:
        print(f'initialborder with this id {initialborderid} does not exist')
    except Exception as e:
        print(f'Error generating report: {str(e)}')
        import traceback
        traceback.print_exc()

def create_word_from_a_initialborder(
        initialborderid: InitialBorder,
) -> str|None:

    try: 
        initialborder_instance : InitialBorder = InitialBorder.objects.get(pk=initialborderid)

        # Create document
        document = Document()
            
        # Set document direction to RTL
        sections = document.sections
        for section in sections:
            section.page_height = Pt(842)  # A4 height
            section.page_width = Pt(595)   # A4 width
            
        # Add title
        add_rtl_paragraph(
            document = document, 
            text = f'گزارش محدوده اولیه: {initialborder_instance.title}',
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
            font_size=16
        )
            
        document.add_paragraph()  # Empty line
            
        # Add basic information
        add_rtl_paragraph(document, 'اطلاعات اصلی', bold=True, font_size=14)
            
        # Title
        add_rtl_paragraph(document, f'عنوان: {initialborder_instance.title}')
            
        # Domain type
        if initialborder_instance.dtyp:
            add_rtl_paragraph(document, f'نوع محدوده: {initialborder_instance.dtyp.title}')
            add_rtl_paragraph(document, f'کد نوع محدوده: {initialborder_instance.dtyp.code}')
        else:
            add_rtl_paragraph(document, 'نوع محدوده: تعریف نشده')
            
        # Parent
        if initialborder_instance.parentid:
            add_rtl_paragraph(document, f'محدوده والد: {initialborder_instance.parentid.title}')
        else:
            add_rtl_paragraph(document, 'محدوده والد: ندارد')

        ###############################################################################################
        # Provinces
        document.add_page_break()
        add_rtl_paragraph(document, 'استان‌های مرتبط', bold=True, font_size=14)
        document.add_paragraph()
        
        provinces = initialborder_instance.province.all()
        if provinces.exists():
            # Create table for provinces
            table = document.add_table(rows=1, cols=2)
            table.style = 'Light Grid Accent 1'
            
            # Header row
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = 'ردیف'
            hdr_cells[1].text = 'نام استان'
            
            # Format header with RTL
            for cell in hdr_cells:
                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    pPr = paragraph._element.get_or_add_pPr()
                    bidi_element = OxmlElement('w:bidi')
                    pPr.append(bidi_element)
                    
                    for run in paragraph.runs:
                        run.font.bold = True
                        run.font.name = 'B Nazanin'
                        run.font.size = Pt(11)
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'B Nazanin')
                        run._element.rPr.rFonts.set(qn('w:cs'), 'B Nazanin')
            
            # Add province rows
            for idx, province in enumerate(provinces, 1):
                row_cells = table.add_row().cells
                row_cells[0].text = str(idx)
                row_cells[1].text = province.name_fa
                
                # Format cells with RTL
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        pPr = paragraph._element.get_or_add_pPr()
                        bidi_element = OxmlElement('w:bidi')
                        pPr.append(bidi_element)
                        
                        for run in paragraph.runs:
                            run.font.name = 'B Nazanin'
                            run.font.size = Pt(11)
                            run._element.rPr.rFonts.set(qn('w:eastAsia'), 'B Nazanin')
                            run._element.rPr.rFonts.set(qn('w:cs'), 'B Nazanin')
            
            document.add_paragraph()
            add_rtl_paragraph(document, f'تعداد کل استان‌ها: {provinces.count()}')
        else:
            add_rtl_paragraph(document, 'هیچ استانی یافت نشد')

            
        ###############################################################################################
        # Geographic information
        document.add_page_break()
        add_rtl_paragraph(document, 'اطلاعات جغرافیایی', bold=True, font_size=14)
        
        center = initialborder_instance.center
        add_rtl_paragraph(document, f'مختصات مرکز: {center[0]:.6f}, {center[1]:.6f}')
        
        bbox = initialborder_instance.bbox
        add_rtl_paragraph(document, f'محدوده جغرافیایی (Bounding Box):')
        add_rtl_paragraph(document, f'  - حداقل طول جغرافیایی: {bbox[0]:.6f}')
        add_rtl_paragraph(document, f'  - حداقل عرض جغرافیایی: {bbox[1]:.6f}')
        add_rtl_paragraph(document, f'  - حداکثر طول جغرافیایی: {bbox[2]:.6f}')
        add_rtl_paragraph(document, f'  - حداکثر عرض جغرافیایی: {bbox[3]:.6f}')
        
        # Calculate area (in square meters)
        area_result = InitialBorder.objects.filter(
            pk=initialborder_instance.pk
        ).aggregate(
            total_area=Sum(
                RawSQL("ST_Area(border::geography)", [])
            )
        )

        total_area_m2 = area_result['total_area'] if area_result['total_area'] else 0
        area_sq_km = total_area_m2 / 1_000_000
        add_rtl_paragraph(document, f'مساحت: {area_sq_km:.2f} کیلومتر مربع')

        # Vertices (راس‌های محدوده)
        add_rtl_paragraph(document, 'راس‌های محدوده', bold=True, font_size=14)
        
        # Extract vertices from the border geometry
        vertices = []
        for polygon in initialborder_instance.border:
            for linear_ring in polygon:
                for coord in linear_ring.coords:
                    vertices.append(coord)
        
        if vertices:
            # Create table for vertices
            table = document.add_table(rows=1, cols=3)
            table.style = 'Light Grid Accent 1'
            
            # Header row
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = 'ردیف'
            hdr_cells[1].text = 'طول جغرافیایی (X)'
            hdr_cells[2].text = 'عرض جغرافیایی (Y)'
            
            # Format header with RTL
            for cell in hdr_cells:
                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    pPr = paragraph._element.get_or_add_pPr()
                    bidi_element = OxmlElement('w:bidi')
                    pPr.append(bidi_element)
                    
                    for run in paragraph.runs:
                        run.font.bold = True
                        run.font.name = 'B Nazanin'
                        run.font.size = Pt(11)
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'B Nazanin')
                        run._element.rPr.rFonts.set(qn('w:cs'), 'B Nazanin')
            
            # Add vertex rows
            for idx, vertex in enumerate(vertices, 1):
                row_cells = table.add_row().cells
                row_cells[0].text = str(idx)
                row_cells[1].text = f'{vertex[0]:.6f}'
                row_cells[2].text = f'{vertex[1]:.6f}'
                
                # Format cells with RTL
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        pPr = paragraph._element.get_or_add_pPr()
                        bidi_element = OxmlElement('w:bidi')
                        pPr.append(bidi_element)
                        
                        for run in paragraph.runs:
                            run.font.name = 'B Nazanin'
                            run.font.size = Pt(11)
                            run._element.rPr.rFonts.set(qn('w:eastAsia'), 'B Nazanin')
                            run._element.rPr.rFonts.set(qn('w:cs'), 'B Nazanin')
            
            document.add_paragraph()
            add_rtl_paragraph(document, f'تعداد کل راس‌ها: {len(vertices)}')
        else:
            add_rtl_paragraph(document, 'هیچ راسی یافت نشد')


    ###############################################################################################

        # Attachments (پیوست‌ها)
        document.add_page_break()

        add_rtl_paragraph(document, 'پیوست‌های مرتبط', bold=True, font_size=14)
        document.add_paragraph()
        
        attachments = InitialBorderAttachment.objects.filter(
            rinitialborder=initialborder_instance
        ).select_related('dtyp_attach', 'writer')
        
        if attachments.exists():
            for idx, attachment in enumerate(attachments, 1):
                # Get attachment type name
                attach_type = attachment.dtyp_attach.name if attachment.dtyp_attach else 'نامشخص'
                attach_category = attachment.dtyp_attach.category if attachment.dtyp_attach else 'نامشخص'
                
                # Get writer information
                if attachment.writer:
                    writer_name = f"{attachment.writer.first_name_fa or ''} {attachment.writer.last_name_fa or ''}".strip()
                    if not writer_name:
                        writer_name = attachment.writer.username
                else:
                    writer_name = 'نامشخص'
                
                # Format dates
                upload_date = attachment.upload_date.strftime('%Y/%m/%d - %H:%M') if attachment.upload_date else 'نامشخص'
                writed_date = attachment.writed_date.strftime('%Y/%m/%d') if attachment.writed_date else 'ثبت نشده'
                
                # Get absolute file path
                file_path = attachment.file.path if attachment.file else 'فایل موجود نیست'
                file_url = attachment.file.url if attachment.file else '#'
                file_name = os.path.basename(file_path) if attachment.file else 'نامشخص'
                
                # Create bullet point text
                bullet_text = (
                    f"پیوست {idx}: {attach_type} | "
                    f"دسته‌بندی: {attach_category} | "
                    f"نویسنده: {writer_name} | "
                    f"تاریخ نوشتن: {writed_date} | "
                    f"تاریخ بارگذاری: {upload_date} | "
                    f"نام فایل: {file_name} | "
                    f"مسیر: {file_path}"
                )
                
                # Add as paragraph with bullet
                p = add_rtl_paragraph(
                    document, 
                    bullet_text,
                    alignment=WD_ALIGN_PARAGRAPH.LEFT,
                    font_size=10
                )
                # Add bullet style
                p.style = 'List Bullet'
                
                document.add_paragraph()  # Add spacing between attachments
            
            add_rtl_paragraph(document, f'تعداد کل پیوست‌ها: {attachments.count()}', bold=True)
        else:
            add_rtl_paragraph(document, 'هیچ پیوستی برای این محدوده ثبت نشده است.')
        
    ###############################################################################################

        # Metadata (شناسنامه)
        document.add_page_break()
        add_rtl_paragraph(document, 'شناسنامه و مشخصات فنی', bold=True, font_size=14)
        
        # Get the metadata based on domain code
        metadata_text = ""
        if initialborder_instance.dtyp:
            code = initialborder_instance.dtyp.code
            
            try:
                if code == 404:  # Pahneh
                    metadata = initialborder_instance.initialbordermetadatapahneh_rinitialborder
                    metadata_text = f"بدینوسیله به استحضار می‌رساند که محدوده موصوف تحت عنوان «{metadata.name if metadata.name else 'نامشخص'}» به مساحت {metadata.masahat if metadata.masahat else 'نامعلوم'} کیلومتر مربع واقع در استان {metadata.ostan if metadata.ostan else 'نامشخص'} و شهرستان {metadata.shahrestan if metadata.shahrestan else 'نامشخص'} که مالکیت آن متعلق به {metadata.malekiyat if metadata.malekiyat else 'نامشخص'} می‌باشد، به عنوان پهنه معدنی در سامانه ثبت و ضبط گردیده است."
                
                elif code == 22:  # Darkhast ekteshaf
                    metadata = initialborder_instance.initialbordermetadatadarkhastekteshaf_rinitialborder
                    metadata_text = f"احتراماً به استحضار می‌رساند که درخواست اکتشاف ماده معدنی «{metadata.noemademadani if metadata.noemademadani else 'نامشخص'}» تحت عنوان «{metadata.name if metadata.name else 'نامشخص'}» به مساحت {metadata.masahat if metadata.masahat else 'نامعلوم'} کیلومتر مربع با شماره کاداستر {metadata.cadastre if metadata.cadastre else 'فاقد شماره'} واقع در استان {metadata.ostan if metadata.ostan else 'نامشخص'} و شهرستان {metadata.shahrestan if metadata.shahrestan else 'نامشخص'} که مالکیت آن در تصرف {metadata.malekiyat if metadata.malekiyat else 'نامشخص'} می‌باشد، طی مراحل قانونی در دست اقدام بوده و از ارگان‌های ذیربط شامل {metadata.organs if metadata.organs else 'ارگان‌های مربوطه'} استعلام لازم به عمل آمده است."
                
                elif code == 33:  # Parvane ekteshaf
                    metadata = initialborder_instance.initialbordermetadataparvaneekteshaf_rinitialborder
                    tarikh_parvane = metadata.tarikhparvane.strftime('%Y/%m/%d') if metadata.tarikhparvane else 'نامشخص'
                    tarikh_etebar = metadata.tarikhetebar.strftime('%Y/%m/%d') if metadata.tarikhetebar else 'نامشخص'
                    metadata_text = f"مستنداً به مقررات و ضوابط قانونی مربوطه، پروانه اکتشاف ماده معدنی «{metadata.noemademadani if metadata.noemademadani else 'نامشخص'}» به نام «{metadata.name if metadata.name else 'نامشخص'}» به مساحت {metadata.masahat if metadata.masahat else 'نامعلوم'} کیلومتر مربع با شماره کاداستر {metadata.cadastre if metadata.cadastre else 'فاقد شماره'} واقع در استان {metadata.ostan if metadata.ostan else 'نامشخص'} و شهرستان {metadata.shahrestan if metadata.shahrestan else 'نامشخص'} به شماره پروانه {metadata.shomareparvaneh if metadata.shomareparvaneh else 'بدون شماره'} در تاریخ {tarikh_parvane} صادر و اعتبار آن تا تاریخ {tarikh_etebar} به {metadata.malekiyat if metadata.malekiyat else 'متقاضی'} اعطا گردیده است."
                
                elif code == 44:  # Govahi kashf
                    metadata = initialborder_instance.initialbordermetadatagovahikashf_rinitialborder
                    tarikh_parvane = metadata.tarikhparvane.strftime('%Y/%m/%d') if metadata.tarikhparvane else 'نامشخص'
                    tarikh_etebar = metadata.tarietebargovahi.strftime('%Y/%m/%d') if metadata.tarietebargovahi else 'نامشخص'
                    tarikh_sodur = metadata.tarikhsodurgivahikashf.strftime('%Y/%m/%d') if metadata.tarikhsodurgivahikashf else 'نامشخص'
                    metadata_text = f"بموجب گواهی کشف به شماره {metadata.shomaregovahikashf if metadata.shomaregovahikashf else 'فاقد شماره'} مورخ {tarikh_sodur}، محدوده معدنی «{metadata.name if metadata.name else 'نامشخص'}» به مساحت {metadata.masahat if metadata.masahat else 'نامعلوم'} کیلومتر مربع با شماره کاداستر {metadata.cadastre if metadata.cadastre else 'فاقد شماره'} واقع در استان {metadata.ostan if metadata.ostan else 'نامشخص'} و شهرستان {metadata.shahrestan if metadata.shahrestan else 'نامشخص'} حاوی ماده معدنی «{metadata.noemademadani if metadata.noemademadani else 'نامشخص'}» با ذخیره احتمالی {metadata.zakhireehtemali if metadata.zakhireehtemali else 'نامعلوم'} تن و ذخیره قطعی {metadata.zakhireghatei if metadata.zakhireghatei else 'نامعلوم'} تن به عیار حد {metadata.ayarehad if metadata.ayarehad else 'نامشخص'} درصد و عیار میانگین {metadata.ayaremeyangin if metadata.ayaremeyangin else 'نامشخص'} درصد، به موجب پروانه اکتشاف شماره {metadata.shomareparvaneh if metadata.shomareparvaneh else 'فاقد شماره'} مورخ {tarikh_parvane} که اعتبار آن تا تاریخ {tarikh_etebar} می‌باشد، متعلق به {metadata.malekiyat if metadata.malekiyat else 'نامشخص'} تایید و ثبت گردیده است."
                
                elif code == 55:  # Parvane bahre bardari
                    metadata = initialborder_instance.initialbordermetadataparvanebahrebardai_rinitialborder
                    tarikh_parvane = metadata.tarikhparvane.strftime('%Y/%m/%d') if metadata.tarikhparvane else 'نامشخص'
                    tarikh_etebar = metadata.tarietebarparvane.strftime('%Y/%m/%d') if metadata.tarietebarparvane else 'نامشخص'
                    metadata_text = f"طبق مفاد پروانه بهره‌برداری به شماره {metadata.shomareparvaneh if metadata.shomareparvaneh else 'فاقد شماره'} مورخ {tarikh_parvane}، محدوده معدنی «{metadata.name if metadata.name else 'نامشخص'}» به مساحت {metadata.masahat if metadata.masahat else 'نامعلوم'} کیلومتر مربع با شماره کاداستر {metadata.cadastre if metadata.cadastre else 'فاقد شماره'} واقع در استان {metadata.ostan if metadata.ostan else 'نامشخص'} و شهرستان {metadata.shahrestan if metadata.shahrestan else 'نامشخص'} حاوی ماده معدنی «{metadata.noemademadani if metadata.noemademadani else 'نامشخص'}» با ذخیره احتمالی {metadata.zakhireehtemali if metadata.zakhireehtemali else 'نامعلوم'} تن و ذخیره قطعی {metadata.zakhireghatei if metadata.zakhireghatei else 'نامعلوم'} تن به عیار حد {metadata.ayarehad if metadata.ayarehad else 'نامشخص'} درصد و عیار میانگین {metadata.ayaremeyangin if metadata.ayaremeyangin else 'نامشخص'} درصد با ظرفیت استخراج سالیانه {metadata.estekhrajsaleyane if metadata.estekhrajsaleyane else 'نامعلوم'} تن، جهت انجام عملیات بهره‌برداری به {metadata.malekiyat if metadata.malekiyat else 'نامشخص'} اعطا گردیده و اعتبار این پروانه تا تاریخ {tarikh_etebar} معتبر می‌باشد."
                
                elif code == 303:  # Potansielyabi
                    metadata = initialborder_instance.initialbordermetadatapotansielyabi_rinitialborder
                    metadata_text = f"محدوده پتانسیل‌یابی تحت عنوان «{metadata.name if metadata.name else 'نامشخص'}» به مساحت {metadata.masahat if metadata.masahat else 'نامعلوم'} کیلومتر مربع واقع در استان {metadata.ostan if metadata.ostan else 'نامشخص'} و شهرستان {metadata.shahrestan if metadata.shahrestan else 'نامشخص'} جهت بررسی و ارزیابی پتانسیل ماده معدنی «{metadata.noemademadani if metadata.noemademadani else 'نامشخص'}» که مالکیت آن متعلق به {metadata.malekiyat if metadata.malekiyat else 'نامشخص'} می‌باشد، در سامانه به ثبت رسیده و مطالعات اولیه در دست انجام است."
                
                if metadata_text:
                    add_rtl_paragraph(document, metadata_text, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
                else:
                    add_rtl_paragraph(document, 'شناسنامه برای این محدوده تعریف نشده است.')
                    
            except Exception as e:
                add_rtl_paragraph(document, 'شناسنامه برای این محدوده ثبت نگردیده است.')
        else:
            add_rtl_paragraph(document, 'نوع محدوده مشخص نشده است.')

    ###############################################################################################

        # Contracts (قراردادهای مرتبط)
        document.add_page_break()
        add_rtl_paragraph(document, 'قراردادهای مرتبط', bold=True, font_size=14)
        document.add_paragraph()
        
        contract_borders = ContractBorder.objects.filter(
            initborder=initialborder_instance
        ).select_related('contract', 'contract__dtyp').prefetch_related('contract__company')
        
        if contract_borders.exists():
            # Create formal paragraph first
            contract_texts = []
            for cb in contract_borders:
                contract = cb.contract
                
                # Get contract type
                contract_type = contract.dtyp.title if contract.dtyp else 'نامشخص'
                
                # Get companies
                companies = contract.company.all()
                company_names = '، '.join([comp.name for comp in companies]) if companies.exists() else 'نامشخص'
                
                # Get department
                department_display = dict(Contract.DEPARTMENT_CHOICES).get(contract.department, 'نامشخص')
                
                # Format dates
                start_date = contract.start_date.strftime('%Y/%m/%d') if contract.start_date else 'نامشخص'
                end_date = contract.end_date.strftime('%Y/%m/%d') if contract.end_date else 'نامشخص'
                
                # Format money
                mablagh = f"{contract.mablagh:,}" if contract.mablagh else 'نامشخص'
                
                # Build contract text
                status_text = "خاتمه یافته" if contract.is_completed else "در حال اجرا"
                elhaghye_text = ""
                if contract.elhaghye and contract.mablaghe_elhaghye:
                    tarikh_elhaghye = contract.tarikh_elhaghye.strftime('%Y/%m/%d') if contract.tarikh_elhaghye else 'نامشخص'
                    mablagh_elhaghye = f"{contract.mablaghe_elhaghye:,}"
                    elhaghye_text = f" که در تاریخ {tarikh_elhaghye} الحاقیه‌ای به مبلغ {mablagh_elhaghye} ریال به آن افزوده شده است"
                
                contract_text = (
                    f"قرارداد «{contract.title}» به شماره {contract.number if contract.number else 'بدون شماره'} "
                    f"از نوع {contract_type} با {company_names} در بخش {department_display} "
                    f"به مبلغ {mablagh} ریال{elhaghye_text}، "
                    f"از تاریخ {start_date} لغایت {end_date} با پیشرفت {contract.progress}% "
                    f"و وضعیت {status_text} می‌باشد"
                )
                contract_texts.append(contract_text)


            add_rtl_paragraph(
                document,
                'بدین وسیله به اطلاع می‌رساند که محدوده مذکور مشمول قراردادهای ذیل می‌باشد:',
                alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                bold=True
            )

            # Add a separate paragraph for each contract
            for idx, contract_text in enumerate(contract_texts, 1):
                add_rtl_paragraph(
                    document,
                    f'{idx}. {contract_text}.',
                    alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
                )
                document.add_paragraph()
            
            
            document.add_paragraph()

            document.add_page_break()                

            # Create contract table 
            add_rtl_paragraph(document, 'جدول خلاصه قراردادها', bold=True, font_size=12)
            document.add_paragraph()
            
            table = document.add_table(rows=1, cols=6)
            table.style = 'Light Grid Accent 1'
            
            # Header row
            hdr_cells = table.rows[0].cells
            headers = [
                'ردیف',
                'عنوان و شماره',
                'نوع و بخش',
                'شرکت',
                'بازه زمانی',
                'وضعیت'
            ]
            
            for idx, header in enumerate(headers):
                hdr_cells[idx].text = header
            
            # Format header with RTL
            for cell in hdr_cells:
                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    pPr = paragraph._element.get_or_add_pPr()
                    bidi_element = OxmlElement('w:bidi')
                    pPr.append(bidi_element)
                    
                    for run in paragraph.runs:
                        run.font.bold = True
                        run.font.name = 'B Nazanin'
                        run.font.size = Pt(10)
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'B Nazanin')
                        run._element.rPr.rFonts.set(qn('w:cs'), 'B Nazanin')
            
            # Add contract rows
            for idx, cb in enumerate(contract_borders, 1):
                contract = cb.contract
                row_cells = table.add_row().cells
                
                # Get data
                contract_type = contract.dtyp.title if contract.dtyp else '-'
                companies = contract.company.all()
                company_names = '\n'.join([comp.name for comp in companies]) if companies.exists() else '-'
                department_display = dict(Contract.DEPARTMENT_CHOICES).get(contract.department, '-')
                start_date = contract.start_date.strftime('%Y/%m/%d') if contract.start_date else '-'
                end_date = contract.end_date.strftime('%Y/%m/%d') if contract.end_date else '-'
                
                # Status with progress
                if contract.is_completed:
                    status = '✓ خاتمه یافته'
                else:
                    status = f'در حال اجرا\n({contract.progress}%)'
                
                # Fill cells
                row_cells[0].text = str(idx)
                row_cells[1].text = f"{contract.title}\n({contract.number if contract.number else 'بدون شماره'})"
                row_cells[2].text = f"{contract_type}\n{department_display}"
                row_cells[3].text = company_names
                row_cells[4].text = f"{start_date}\nتا\n{end_date}"
                row_cells[5].text = status
                
                # Format cells with RTL
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        pPr = paragraph._element.get_or_add_pPr()
                        bidi_element = OxmlElement('w:bidi')
                        pPr.append(bidi_element)
                        
                        for run in paragraph.runs:
                            run.font.name = 'B Nazanin'
                            run.font.size = Pt(9)
                            run._element.rPr.rFonts.set(qn('w:eastAsia'), 'B Nazanin')
                            run._element.rPr.rFonts.set(qn('w:cs'), 'B Nazanin')
            
            document.add_paragraph()
            add_rtl_paragraph(document, f'تعداد کل قراردادها: {contract_borders.count()}', bold=True)
            
        else:
            add_rtl_paragraph(document, 'هیچ قرارداد مرتبطی برای این محدوده ثبت نشده است.')

        ###############################################################################################
        # ShrhBase and ShrhLayer details per contract
        document.add_page_break()
        add_rtl_paragraph(document, 'شرح خدمات قراردادها', bold=True, font_size=14)
        document.add_paragraph()

        if contract_borders.exists():
            # Get unique contracts from contract_borders
            processed_contracts = set()
            for cb in contract_borders:
                contract = cb.contract
                if contract.pk in processed_contracts:
                    continue
                processed_contracts.add(contract.pk)

                # Contract heading
                add_rtl_paragraph(
                    document,
                    f'قرارداد: {contract.title} (شماره: {contract.number if contract.number else "بدون شماره"})',
                    bold=True,
                    font_size=12
                )
                document.add_paragraph()

                shrh_items = contract.shrh_items.all().prefetch_related('shr_layers__layer_name', 'shr_layers__last_uploaded_by', 'shr_layers__verified_by')

                if shrh_items.exists():
                    for shrh_base in shrh_items:
                        # ShrhBase info
                        add_rtl_paragraph(
                            document,
                            f'بند: {shrh_base.title}',
                            bold=True,
                            font_size=11
                        )

                        # ShrhBase details as small info line
                        total_price_formatted = f"{shrh_base.total_price:,.0f}" if shrh_base.total_price else '0'
                        completed_price_formatted = f"{shrh_base.completed_price:,.0f}" if shrh_base.completed_price else '0'
                        add_rtl_paragraph(
                            document,
                            f'درصد بند: {shrh_base.percentage}% | درصد کار انجام شده: {shrh_base.worked_percentage}% | '
                            f'درصد تکمیل: {shrh_base.completion_percentage:.1f}% | باقی‌مانده: {shrh_base.remaining_percentage}% | '
                            f'مبلغ بند: {total_price_formatted} ریال | مبلغ انجام شده: {completed_price_formatted} ریال',
                            font_size=10
                        )
                        document.add_paragraph()

                        # ShrhLayer table
                        layers = shrh_base.shr_layers.all()
                        if layers.exists():
                            table = document.add_table(rows=1, cols=7)
                            table.style = 'Light Grid Accent 1'

                            headers = [
                                'ردیف',
                                'نام لایه',
                                'محدوده قرارداد',
                                'واحد',
                                'مقیاس',
                                'وضعیت',
                                'تاریخ آخرین بارگذاری',
                            ]

                            hdr_cells = table.rows[0].cells
                            for i, header in enumerate(headers):
                                hdr_cells[i].text = header
                                for paragraph in hdr_cells[i].paragraphs:
                                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                    pPr = paragraph._element.get_or_add_pPr()
                                    bidi_element = OxmlElement('w:bidi')
                                    pPr.append(bidi_element)
                                    for run in paragraph.runs:
                                        run.font.bold = True
                                        run.font.name = 'B Nazanin'
                                        run.font.size = Pt(9)
                                        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'B Nazanin')
                                        run._element.rPr.rFonts.set(qn('w:cs'), 'B Nazanin')

                            for idx, layer in enumerate(layers, 1):
                                row_cells = table.add_row().cells

                                layer_name = layer.layer_name.layername_fa if hasattr(layer.layer_name, 'layername_fa') and layer.layer_name.layername_fa else (layer.layer_name.layername_en if hasattr(layer.layer_name, 'layername_en') else str(layer.layer_name))
                                contract_border_title = layer.contractborder.title if layer.contractborder else '-'
                                unit = layer.unit if layer.unit else '-'
                                scale = str(layer.scale) if layer.scale else '-'
                                status = layer.status
                                last_upload = layer.last_uploaded_date.strftime('%Y/%m/%d') if layer.last_uploaded_date else 'بارگذاری نشده'

                                row_data = [str(idx), layer_name, contract_border_title, unit, scale, status, last_upload]

                                for i, cell_text in enumerate(row_data):
                                    row_cells[i].text = cell_text
                                    for paragraph in row_cells[i].paragraphs:
                                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                        pPr = paragraph._element.get_or_add_pPr()
                                        bidi_element = OxmlElement('w:bidi')
                                        pPr.append(bidi_element)
                                        for run in paragraph.runs:
                                            run.font.name = 'B Nazanin'
                                            run.font.size = Pt(9)
                                            run._element.rPr.rFonts.set(qn('w:eastAsia'), 'B Nazanin')
                                            run._element.rPr.rFonts.set(qn('w:cs'), 'B Nazanin')

                            document.add_paragraph()
                            add_rtl_paragraph(document, f'تعداد لایه‌ها: {layers.count()}', font_size=10)
                        else:
                            add_rtl_paragraph(document, 'هیچ لایه‌ای برای این بند ثبت نشده است.', font_size=10)

                        document.add_paragraph()

                else:
                    add_rtl_paragraph(document, 'هیچ بند شرح خدماتی برای این قرارداد ثبت نشده است.')

                document.add_paragraph()
        else:
            add_rtl_paragraph(document, 'هیچ قرارداد مرتبطی وجود ندارد.')

    ###############################################################################################
        # Add footer
        document.add_paragraph()
        document.add_paragraph()
        add_rtl_paragraph(document, '─' * 50, alignment=WD_ALIGN_PARAGRAPH.CENTER)
        add_rtl_paragraph(
            document, 
            f'تاریخ تولید گزارش: {datetime.now().strftime("%Y/%m/%d - %H:%M")}',
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            font_size=8
        )
        
        reports_dir = os.path.join(settings.MEDIA_ROOT, "init_word_reports")
        os.makedirs(reports_dir, exist_ok=True)

        filename = f'initialborder_report_{initialborder_instance.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx'
        file_path = os.path.join(reports_dir, filename)

        document.save(file_path)

        file_path = os.path.join(reports_dir, filename)

        print(f'Report generated successfully: {file_path}')
        # return file_path

        return os.path.join("init_word_reports", filename)


    except InitialBorder.DoesNotExist:
        print(f'initialborder with this id {initialborderid} does not exist')
    except Exception as e:
        print(f'Error generating report: {str(e)}')
        import traceback
        traceback.print_exc()
    