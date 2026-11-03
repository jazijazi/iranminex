
import os
import uuid
from typing import cast, Dict, Any
from django.conf import settings
from django.contrib.gis.geos import MultiPolygon
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
import openpyxl
from openpyxl.styles import Border, Side , Alignment , PatternFill, Font



def create_excel_from_contract_init(
        initialborder: InitialBorder,
        contract: Contract
) -> str:
    
    wb = openpyxl.Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)
    ws = wb.create_sheet(title="گزارش قرارداد")
    ws.sheet_view.rightToLeft = True


    # --- Styles ---
    header_font = Font(bold=True, size=11, color="FFFFFF")
    header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    section_font = Font(bold=True, size=11, color="000000")
    section_fill = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
    section_alignment = Alignment(horizontal="center", vertical="center")

    value_alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)

    thin_side = Side(style="thin", color="000000")
    thin_border = Border(
        left=thin_side,
        right=thin_side,
        top=thin_side,
        bottom=thin_side
    )

    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 50

    row = 1

    # ==================== MAIN HEADER ====================
    ws.merge_cells(f"A{row}:B{row}")
    cell = ws[f"A{row}"]
    cell.value = "گزارش قرارداد"
    cell.font = Font(bold=True, size=14, color="FFFFFF")
    cell.fill = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border
    ws.row_dimensions[row].height = 30
    row += 1

    # ==================== INITIAL BORDER SECTION ====================
    ws.merge_cells(f"A{row}:B{row}")
    cell = ws[f"A{row}"]
    cell.value = "اطلاعات محدوده اولیه"
    cell.font = section_font
    cell.fill = section_fill
    cell.alignment = section_alignment
    cell.border = thin_border
    ws.row_dimensions[row].height = 22
    row += 1

    # title
    ws[f"A{row}"].value = "عنوان محدوده"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = initialborder.title if initialborder.title else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # dtyp.title
    ws[f"A{row}"].value = "نوع محدوده"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = initialborder.dtyp.title if initialborder.dtyp else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # province.name_fa (ManyToMany - join all)
    provinces = initialborder.province.all()
    province_value = ", ".join([p.name_fa for p in provinces if p.name_fa]) if provinces.exists() else "نامشخص"
    ws[f"A{row}"].value = "استان‌ها"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = province_value
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # ==================== CONTRACT SECTION ====================
    ws.merge_cells(f"A{row}:B{row}")
    cell = ws[f"A{row}"]
    cell.value = "اطلاعات قرارداد"
    cell.font = section_font
    cell.fill = section_fill
    cell.alignment = section_alignment
    cell.border = thin_border
    ws.row_dimensions[row].height = 22
    row += 1

    # title
    ws[f"A{row}"].value = "عنوان قرارداد"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = contract.title if contract.title else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # number
    ws[f"A{row}"].value = "شماره قرارداد"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = contract.number if contract.number else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # start_date
    ws[f"A{row}"].value = "تاریخ شروع"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = str(contract.start_date) if contract.start_date else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # end_date
    ws[f"A{row}"].value = "تاریخ پایان"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = str(contract.end_date) if contract.end_date else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # progress
    ws[f"A{row}"].value = "پیشرفت"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = str(contract.progress) if contract.progress is not None else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # is_completed
    ws[f"A{row}"].value = "تکمیل شده"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = "بله" if contract.is_completed else "خیر"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # elhaghye
    ws[f"A{row}"].value = "الحاقیه"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = str(contract.elhaghye) if contract.elhaghye is not None else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # mablagh
    ws[f"A{row}"].value = "مبلغ"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = str(contract.mablagh) if contract.mablagh is not None else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # mablaghe_elhaghye
    ws[f"A{row}"].value = "مبلغ الحاقیه"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = str(contract.mablaghe_elhaghye) if contract.mablaghe_elhaghye is not None else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # tarikh_elhaghye
    ws[f"A{row}"].value = "تاریخ الحاقیه"
    ws[f"A{row}"].font = header_font
    ws[f"A{row}"].fill = header_fill
    ws[f"A{row}"].alignment = header_alignment
    ws[f"A{row}"].border = thin_border
    ws[f"B{row}"].value = str(contract.tarikh_elhaghye) if contract.tarikh_elhaghye else "نامشخص"
    ws[f"B{row}"].alignment = value_alignment
    ws[f"B{row}"].border = thin_border
    ws.row_dimensions[row].height = 20
    row += 1

    # ==================== COMPANY SECTION ====================
    companies = contract.company.all()

    ws.merge_cells(f"A{row}:B{row}")
    cell = ws[f"A{row}"]
    cell.value = "اطلاعات شرکت‌ها"
    cell.font = section_font
    cell.fill = section_fill
    cell.alignment = section_alignment
    cell.border = thin_border
    ws.row_dimensions[row].height = 22
    row += 1

    if not companies.exists():
        ws.merge_cells(f"A{row}:B{row}")
        cell = ws[f"A{row}"]
        cell.value = "نامشخص"
        cell.alignment = value_alignment
        cell.border = thin_border
        ws.row_dimensions[row].height = 20
        row += 1
    else:
        for index, company in enumerate(companies, start=1):

            # company sub-header
            ws.merge_cells(f"A{row}:B{row}")
            cell = ws[f"A{row}"]
            cell.value = f"شرکت {index}"
            cell.font = Font(bold=True, size=10, color="000000")
            cell.fill = PatternFill(start_color="EBF3FB", end_color="EBF3FB", fill_type="solid")
            cell.alignment = section_alignment
            cell.border = thin_border
            ws.row_dimensions[row].height = 20
            row += 1

            # name
            ws[f"A{row}"].value = "نام شرکت"
            ws[f"A{row}"].font = header_font
            ws[f"A{row}"].fill = header_fill
            ws[f"A{row}"].alignment = header_alignment
            ws[f"A{row}"].border = thin_border
            ws[f"B{row}"].value = company.name if company.name else "نامشخص"
            ws[f"B{row}"].alignment = value_alignment
            ws[f"B{row}"].border = thin_border
            ws.row_dimensions[row].height = 20
            row += 1

            # typ
            ws[f"A{row}"].value = "نوع شرکت"
            ws[f"A{row}"].font = header_font
            ws[f"A{row}"].fill = header_fill
            ws[f"A{row}"].alignment = header_alignment
            ws[f"A{row}"].border = thin_border
            ws[f"B{row}"].value = str(company.typ) if company.typ is not None else "نامشخص"
            ws[f"B{row}"].alignment = value_alignment
            ws[f"B{row}"].border = thin_border
            ws.row_dimensions[row].height = 20
            row += 1

            # service_typ
            ws[f"A{row}"].value = "نوع خدمات"
            ws[f"A{row}"].font = header_font
            ws[f"A{row}"].fill = header_fill
            ws[f"A{row}"].alignment = header_alignment
            ws[f"A{row}"].border = thin_border
            ws[f"B{row}"].value = str(company.service_typ) if company.service_typ is not None else "نامشخص"
            ws[f"B{row}"].alignment = value_alignment
            ws[f"B{row}"].border = thin_border
            ws.row_dimensions[row].height = 20
            row += 1

            # callnumber
            ws[f"A{row}"].value = "شماره تماس"
            ws[f"A{row}"].font = header_font
            ws[f"A{row}"].fill = header_fill
            ws[f"A{row}"].alignment = header_alignment
            ws[f"A{row}"].border = thin_border
            ws[f"B{row}"].value = company.callnumber if company.callnumber else "نامشخص"
            ws[f"B{row}"].alignment = value_alignment
            ws[f"B{row}"].border = thin_border
            ws.row_dimensions[row].height = 20
            row += 1

            # address
            ws[f"A{row}"].value = "آدرس"
            ws[f"A{row}"].font = header_font
            ws[f"A{row}"].fill = header_fill
            ws[f"A{row}"].alignment = header_alignment
            ws[f"A{row}"].border = thin_border
            ws[f"B{row}"].value = company.address if company.address else "نامشخص"
            ws[f"B{row}"].alignment = value_alignment
            ws[f"B{row}"].border = thin_border
            ws.row_dimensions[row].height = 20
            row += 1

    # ==================== CONTRACT BORDERS SECTION ====================
    contract_borders = ContractBorder.objects.filter(
        contract=contract,
        initborder=initialborder
    ).prefetch_related("rcontractborderlayers")

    ws.merge_cells(f"A{row}:B{row}")
    cell = ws[f"A{row}"]
    cell.value = "اطلاعات محدوده قراردادها"
    cell.font = section_font
    cell.fill = section_fill
    cell.alignment = section_alignment
    cell.border = thin_border
    ws.row_dimensions[row].height = 22
    row += 1

    if not contract_borders.exists():
        ws.merge_cells(f"A{row}:B{row}")
        cell = ws[f"A{row}"]
        cell.value = "نامشخص"
        cell.alignment = value_alignment
        cell.border = thin_border
        ws.row_dimensions[row].height = 20
        row += 1
    else:
        # --- Table headers ---
        table_headers = [
            "شرح خدمات",
            "گروه لایه",
            "نوع هندسه",
            "قیمت واحد",
            "وزن لایه",
            "حجم لایه",
            "بارگذاری شده",
            "تاریخ آخرین بارگذاری",
            "بارگذاری شده توسط",
            "تایید نهایی",
            "تایید شده توسط",
            "تاریخ تایید نهایی",
        ]

        col_letters = ["A","B","C","D","E","F","G","H","I","J","K","L"]
        col_widths   = [30,  25,  18,  15,  13,  13,  16,  25,        20,       14,       20,        20]

        for col_letter, width in zip(col_letters, col_widths):
            ws.column_dimensions[col_letter].width = width

        for contract_border in contract_borders:

            # contract border sub-header
            last_col = col_letters[len(table_headers) - 1]
            ws.merge_cells(f"A{row}:{last_col}{row}")
            cell = ws[f"A{row}"]
            cell.value = contract_border.title
            cell.font = Font(bold=True, size=10, color="000000")
            cell.fill = PatternFill(start_color="EBF3FB", end_color="EBF3FB", fill_type="solid")
            cell.alignment = section_alignment
            cell.border = thin_border
            ws.row_dimensions[row].height = 20
            row += 1

            # table column headers
            for col_index, header in enumerate(table_headers):
                cell = ws[f"{col_letters[col_index]}{row}"]
                cell.value = header
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
                cell.border = thin_border
            ws.row_dimensions[row].height = 20
            row += 1

            # layer rows
            layers = contract_border.rcontractborderlayers.select_related(
                "shrh_base",
                "layer_name",
                "last_uploaded_by",
                "verified_by"
            ).all()

            if not layers.exists():
                ws.merge_cells(f"A{row}:{last_col}{row}")
                cell = ws[f"A{row}"]
                cell.value = "لایه‌ای ثبت نشده"
                cell.alignment = value_alignment
                cell.border = thin_border
                ws.row_dimensions[row].height = 20
                row += 1
            else:
                for layer in layers:
                    row_values = [
                        layer.shrh_base.title if layer.shrh_base and layer.shrh_base.title else "نامشخص",
                        layer.layer_name.lyrgroup_fa if layer.layer_name and layer.layer_name.lyrgroup_fa else "نامشخص",
                        layer.layer_name.geometrytype if layer.layer_name and layer.layer_name.geometrytype else "نامشخص",
                        str(layer.unit_price) if layer.unit_price is not None else "نامشخص",
                        str(layer.layer_weight) if layer.layer_weight is not None else "نامشخص",
                        str(layer.layer_volume) if layer.layer_volume is not None else "نامشخص",
                        "بله" if layer.is_uploaded else "خیر",
                        str(layer.last_uploaded_date) if layer.last_uploaded_date else "نامشخص",
                        layer.last_uploaded_by.username if layer.last_uploaded_by else "نامشخص",
                        "بله" if layer.is_verified else "خیر",
                        layer.verified_by.username if layer.verified_by else "نامشخص",
                        str(layer.verified_at) if layer.verified_at else "نامشخص",
                    ]

                    for col_index, value in enumerate(row_values):
                        cell = ws[f"{col_letters[col_index]}{row}"]
                        cell.value = value
                        cell.alignment = value_alignment
                        cell.border = thin_border

                    ws.row_dimensions[row].height = 20
                    row += 1
                    
    # ==================== SAVE ====================
    reports_dir = os.path.join(settings.MEDIA_ROOT, "contract_init_reports")
    os.makedirs(reports_dir, exist_ok=True)

    filename = f"contract_{contract.pk}_border_{initialborder.pk}_{uuid.uuid4().hex[:8]}.xlsx"
    file_path = os.path.join(reports_dir, filename)
    wb.save(file_path)

    return os.path.join("contract_init_reports", filename)