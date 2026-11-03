from datetime import datetime
import os

from django.conf import settings
from django.db.models import Count, Q, Prefetch
from django.template.loader import render_to_string

from weasyprint import HTML

from contracts.models.models import (
    Contract,
    ContractBorder,
    ContractBorderAttachment,
)
from accounts.models import User
from common.utils import to_jalali, to_jalali_datetime


def get_display_name(u):
    if u.first_name_fa and u.last_name_fa:
        return f"{u.first_name_fa} {u.last_name_fa}"
    return u.username


def create_pdf_form_contract_summary(contractid, user) -> str | None:
    try:
        # ── Single consolidated DB fetch ──────────────────────────────

        contract = Contract.objects.prefetch_related(
            "company",
            Prefetch(
                "users_with_access_contracts",
                queryset=User.objects.filter(
                    Q(roles__title="مجری") |
                    Q(is_controller=True)
                ),
                to_attr="_supervisor_list",
            ),
            Prefetch(
                "rcontractborders",
                queryset=ContractBorder.objects.defer("border").annotate(
                    total_layers=Count("rcontractborderlayers"),
                    uploaded_count=Count(
                        "rcontractborderlayers",
                        filter=Q(
                            rcontractborderlayers__is_uploaded=True
                        ),
                    ),
                    verified_count=Count(
                        "rcontractborderlayers",
                        filter=Q(
                            rcontractborderlayers__is_verified=True
                        ),
                    ),
                ).prefetch_related(
                    Prefetch(
                        "rcontractborderattachment",
                        queryset=(
                            ContractBorderAttachment.objects
                            .select_related("dtyp")
                            .order_by("upload_date")
                        ),
                        to_attr="_attachments",
                    )
                ),
                to_attr="_borders",
            ),
        ).get(pk=contractid)

        # ── Prepare data ──────────────────────────────────────────────

        companies = contract.company.all()

        company_names = (
            "، ".join(c.name for c in companies)
            if companies
            else "نامشخص"
        )

        contract_num = contract.number or "ندارد"

        if contract.start_date and contract.end_date:
            contract_date = (
                f"{to_jalali(contract.start_date)} تا "
                f"{to_jalali(contract.end_date)}"
            )
        elif contract.start_date:
            contract_date = to_jalali(contract.start_date)
        else:
            contract_date = "تعریف نشده"

        status_text = (
            "خاتمه یافته"
            if contract.is_completed
            else "جاری"
        )

        supervisor_names = (
            "، ".join(
                get_display_name(u)
                for u in contract._supervisor_list
            )
            if contract._supervisor_list
            else "تعریف نشده"
        )

        contract_borders = contract._borders

        all_attachments = [
            attachment
            for border in contract_borders
            for attachment in border._attachments
        ]

        # ── Logo ──────────────────────────────────────────────────────

        logo_path = os.path.join(
            settings.BASE_DIR,
            "report",
            "images",
            "ipclogo.png",
        )

        logo_url = (
            f"file://{logo_path}"
            if os.path.exists(logo_path)
            else None
        )

        # ── Render HTML ───────────────────────────────────────────────

        context = {
            "contract": contract,
            "company_names": company_names,
            "contract_num": contract_num,
            "contract_date": contract_date,
            "status_text": status_text,
            "supervisor_names": supervisor_names,
            "contract_borders": contract_borders,
            "all_attachments": all_attachments,
            "report_date": to_jalali(datetime.now().date()),
            "preparer_name": get_display_name(user),
            "logo_url": logo_url,
        }

        html_string = render_to_string(
            "pdf/contract_summary.html",
            context,
        )

        # ── Generate PDF ──────────────────────────────────────────────

        reports_dir = os.path.join(
            settings.MEDIA_ROOT,
            "contract_pdf_summary_reports",
        )

        os.makedirs(reports_dir, exist_ok=True)

        filename = (
            f"contract_report_{contract.pk}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        file_path = os.path.join(
            reports_dir,
            filename,
        )

        HTML(
            string=html_string,
            base_url=settings.BASE_DIR,
        ).write_pdf(file_path)

        return os.path.join(
            "contract_pdf_summary_reports",
            filename,
        )

    except Contract.DoesNotExist:
        print(
            f"contract with this id {contractid} does not exist"
        )

    except Exception as e:
        print(f"Error generating PDF report: {str(e)}")

        import traceback
        traceback.print_exc()