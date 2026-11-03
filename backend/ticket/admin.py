from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from ticket.models import Ticket, TicketComment


STATUS_COLORS = {
    Ticket.Status.OPEN: "#2563eb",
    Ticket.Status.IN_PROGRESS: "#d97706",
    Ticket.Status.ON_HOLD: "#6b7280",
    Ticket.Status.RESOLVED: "#16a34a",
    Ticket.Status.CLOSED: "#374151",
}

PRIORITY_COLORS = {
    Ticket.Priority.LOW: "#16a34a",
    Ticket.Priority.MEDIUM: "#2563eb",
    Ticket.Priority.HIGH: "#d97706",
    Ticket.Priority.URGENT: "#dc2626",
}


class OpenStatusFilter(admin.SimpleListFilter):
    """Lets staff filter by the ticket's is_open property, not just raw status."""

    title = _("open status")
    parameter_name = "open_status"

    def lookups(self, request, model_admin):
        return (
            ("open", _("Open (active)")),
            ("closed", _("Resolved / Closed")),
        )

    def queryset(self, request, queryset):
        if self.value() == "open":
            return queryset.exclude(status__in=[Ticket.Status.RESOLVED, Ticket.Status.CLOSED])
        if self.value() == "closed":
            return queryset.filter(status__in=[Ticket.Status.RESOLVED, Ticket.Status.CLOSED])
        return queryset


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0
    fields = ("author", "body", "file", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("author",)
    show_change_link = True


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "title",
        "category",
        "colored_status",
        "colored_priority",
        "created_by",
        "comment_count",
        "created_at",
    )
    list_filter = ("status", "priority", "category", OpenStatusFilter, "created_at")
    search_fields = ("number", "title", "body", "created_by__username", "created_by__email")
    readonly_fields = ("number", "created_at", "updated_at", "resolved_at")
    autocomplete_fields = ("created_by",)
    date_hierarchy = "created_at"
    list_per_page = 25
    list_select_related = ("created_by",)
    inlines = [TicketCommentInline]
    actions = ["mark_in_progress", "mark_resolved", "mark_closed"]

    fieldsets = (
        (None, {"fields": ("number", "title", "body")}),
        (_("Classification"), {"fields": ("category", "status", "priority")}),
        (_("People"), {"fields": ("created_by",)}),
        (_("Attachment"), {"fields": ("file",)}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at", "resolved_at")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("comments")

    @admin.display(description=_("Status"), ordering="status")
    def colored_status(self, obj):
        color = STATUS_COLORS.get(obj.status, "#000")
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; '
            'border-radius:10px; font-size:12px; white-space:nowrap;">{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.display(description=_("Priority"), ordering="priority")
    def colored_priority(self, obj):
        color = PRIORITY_COLORS.get(obj.priority, "#000")
        return format_html(
            '<span style="background:{}; color:#fff; padding:2px 8px; '
            'border-radius:10px; font-size:12px; white-space:nowrap;">{}</span>',
            color,
            obj.get_priority_display(),
        )

    @admin.display(description=_("Comments"))
    def comment_count(self, obj):
        return obj.comments.count()

    @admin.action(description=_("Mark selected tickets as In Progress"))
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status=Ticket.Status.IN_PROGRESS)
        self.message_user(request, f"{updated} ticket(s) marked as in progress.")

    @admin.action(description=_("Mark selected tickets as Resolved"))
    def mark_resolved(self, request, queryset):
        # Looping (instead of .update()) so the model's save() logic
        # still sets resolved_at automatically.
        updated = 0
        for ticket in queryset:
            ticket.status = Ticket.Status.RESOLVED
            ticket.save()
            updated += 1
        self.message_user(request, f"{updated} ticket(s) marked as resolved.")

    @admin.action(description=_("Mark selected tickets as Closed"))
    def mark_closed(self, request, queryset):
        updated = queryset.update(status=Ticket.Status.CLOSED)
        self.message_user(request, f"{updated} ticket(s) marked as closed.")


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author", "short_body", "has_file", "created_at")
    list_filter = ("created_at",)
    search_fields = ("body", "ticket__number", "ticket__title", "author__username")
    autocomplete_fields = ("ticket", "author")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("ticket", "author")

    @admin.display(description=_("Comment"))
    def short_body(self, obj):
        return (obj.body[:75] + "…") if len(obj.body) > 75 else obj.body

    @admin.display(description=_("Has attachment"), boolean=True)
    def has_file(self, obj):
        return bool(obj.file)