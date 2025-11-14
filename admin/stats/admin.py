"""
Django admin configuration for statistics.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Profile, Event, EventParticipation, QRScan


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Админ-интерфейс для профилей пользователей."""

    list_display = [
        "id",
        "first_name",
        "last_name",
        "max_id",
        "university",
        "is_superuser",
        "created_at",
        "registrations_count",
        "attended_count",
    ]
    list_filter = ["is_superuser", "created_at", "university"]
    search_fields = ["first_name", "last_name", "max_id", "university"]
    readonly_fields = [
        "id",
        "max_id",
        "created_at",
        "registrations_list",
        "attended_list",
    ]
    fieldsets = (
        ("Основная информация", {"fields": ("id", "first_name", "last_name", "max_id")}),
        (
            "Дополнительная информация",
            {"fields": ("gender", "birth_date", "university", "bio", "avatar")},
        ),
        ("Права", {"fields": ("is_superuser",)}),
        ("Регистрации на мероприятия", {"fields": ("registrations_list",)}),
        ("Посещенные мероприятия", {"fields": ("attended_list",)}),
        ("Системная информация", {"fields": ("invited_by", "created_at")}),
    )

    def registrations_count(self, obj):
        """Count of event registrations."""
        count = EventParticipation.objects.filter(user_id=obj.id).count()
        return count

    registrations_count.short_description = "Регистраций"

    def attended_count(self, obj):
        """Count of attended events (with QR scan)."""
        participations = EventParticipation.objects.filter(user_id=obj.id).values_list(
            "id", flat=True
        )
        count = QRScan.objects.filter(participation_id__in=participations).count()
        return count

    attended_count.short_description = "Посетил"

    def registrations_list(self, obj):
        """List of event registrations with links."""
        participations = EventParticipation.objects.filter(user_id=obj.id)
        if not participations.exists():
            return "Нет регистраций"

        # Get all event IDs
        event_ids = [p.event_id for p in participations]
        events_dict = {e.id: e for e in Event.objects.filter(id__in=event_ids)}

        # Get all participation IDs for QR scans
        participation_ids = [p.id for p in participations]
        scans_dict = {
            s.participation_id: s
            for s in QRScan.objects.filter(participation_id__in=participation_ids)
        }

        html = "<ul>"
        for part in participations:
            event = events_dict.get(part.event_id)
            if event:
                event_url = reverse("admin:stats_event_change", args=[event.id])
                scan = scans_dict.get(part.id)
                status = "✅ Пришел" if scan else "❌ Не пришел"
                html += f'<li><a href="{event_url}">{event.title}</a> - {status} ({part.participation_type})</li>'
            else:
                html += f"<li>Мероприятие {part.event_id} (не найдено)</li>"
        html += "</ul>"
        return format_html(html)

    registrations_list.short_description = "История регистраций"

    def attended_list(self, obj):
        """List of attended events."""
        participations = EventParticipation.objects.filter(user_id=obj.id).values_list(
            "id", flat=True
        )
        scans = QRScan.objects.filter(participation_id__in=participations)
        if not scans.exists():
            return "Нет посещений"

        # Get all participation IDs and event IDs
        participation_ids = list(scans.values_list("participation_id", flat=True))
        participations_dict = {
            p.id: p for p in EventParticipation.objects.filter(id__in=participation_ids)
        }
        event_ids = [p.event_id for p in participations_dict.values()]
        events_dict = {e.id: e for e in Event.objects.filter(id__in=event_ids)}

        html = "<ul>"
        for scan in scans:
            part = participations_dict.get(scan.participation_id)
            if part:
                event = events_dict.get(part.event_id)
                if event:
                    event_url = reverse("admin:stats_event_change", args=[event.id])
                    html += f'<li><a href="{event_url}">{event.title}</a> - {scan.scanned_at}</li>'
                else:
                    html += f"<li>Сканирование {scan.id}</li>"
            else:
                html += f"<li>Сканирование {scan.id}</li>"
        html += "</ul>"
        return format_html(html)

    attended_list.short_description = "Посещенные мероприятия"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Админ-интерфейс для мероприятий."""

    list_display = [
        "title",
        "start_date",
        "end_date",
        "status",
        "registered_count",
        "attended_count",
        "attendance_rate",
        "creator_name",
    ]
    list_filter = ["status", "start_date", "end_date"]
    search_fields = ["title", "body", "place"]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
        "registered_count_display",
        "attended_count_display",
        "participants_list",
    ]
    fieldsets = (
        ("Основная информация", {"fields": ("id", "title", "body")}),
        (
            "Детали мероприятия",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "place",
                    "tags",
                    "photo",
                )
            },
        ),
        (
            "Регистрация",
            {
                "fields": (
                    "max_participants",
                    "registration_start_date",
                    "registration_end_date",
                )
            },
        ),
        ("Статус", {"fields": ("status",)}),
        ("Статистика", {"fields": ("registered_count_display", "attended_count_display", "participants_list")}),
        ("Системная информация", {"fields": ("creator", "created_at", "updated_at")}),
    )

    def registered_count(self, obj):
        """Count of registered participants."""
        return EventParticipation.objects.filter(event_id=obj.id).count()

    registered_count.short_description = "Зарегистрировано"

    def registered_count_display(self, obj):
        """Display registered count in detail view."""
        count = self.registered_count(obj)
        max_participants = obj.max_participants
        if max_participants:
            return f"{count} / {max_participants}"
        return str(count)

    registered_count_display.short_description = "Зарегистрировано"

    def attended_count(self, obj):
        """Count of participants who actually attended (scanned QR)."""
        participations = EventParticipation.objects.filter(event_id=obj.id).values_list(
            "id", flat=True
        )
        return QRScan.objects.filter(participation_id__in=participations).count()

    attended_count.short_description = "Пришло"

    def attended_count_display(self, obj):
        """Display attended count in detail view."""
        count = self.attended_count(obj)
        registered = self.registered_count(obj)
        return f"{count} / {registered}"

    attended_count_display.short_description = "Пришло"

    def attendance_rate(self, obj):
        """Calculate attendance rate."""
        registered = self.registered_count(obj)
        if registered == 0:
            return "0%"
        attended = self.attended_count(obj)
        rate = (attended / registered) * 100
        return f"{rate:.1f}%"

    attendance_rate.short_description = "Посещаемость"

    def creator_name(self, obj):
        """Get creator's name."""
        try:
            creator = Profile.objects.get(id=obj.creator)
            return f"{creator.first_name} {creator.last_name}"
        except Profile.DoesNotExist:
            return obj.creator

    creator_name.short_description = "Создатель"

    def participants_list(self, obj):
        """List of participants with attendance status."""
        participations = EventParticipation.objects.filter(event_id=obj.id)
        if not participations.exists():
            return "Нет участников"

        # Get all user IDs and participation IDs
        user_ids = [p.user_id for p in participations]
        participation_ids = [p.id for p in participations]
        users_dict = {u.id: u for u in Profile.objects.filter(id__in=user_ids)}
        scans_dict = {
            s.participation_id: s
            for s in QRScan.objects.filter(participation_id__in=participation_ids)
        }

        html = "<table><tr><th>Пользователь</th><th>Тип</th><th>Статус</th></tr>"
        for part in participations:
            user = users_dict.get(part.user_id)
            if user:
                user_url = reverse("admin:stats_profile_change", args=[user.id])
                scan = scans_dict.get(part.id)
                status = "✅ Пришел" if scan else "❌ Не пришел"
                html += f'<tr><td><a href="{user_url}">{user.first_name} {user.last_name}</a></td>'
                html += f"<td>{part.participation_type}</td><td>{status}</td></tr>"
            else:
                html += f"<tr><td>Пользователь {part.user_id}</td><td>{part.participation_type}</td><td>-</td></tr>"
        html += "</table>"
        return format_html(html)

    participants_list.short_description = "Список участников"


@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    """Админ-интерфейс для участий в мероприятиях."""

    list_display = ["user_name", "event_title", "participation_type", "has_attended", "created_at"]
    list_filter = ["participation_type", "created_at"]
    search_fields = ["user_id", "event_id"]
    readonly_fields = ["id", "user_id", "event_id", "created_at", "has_attended"]

    def user_name(self, obj):
        """Get user's name."""
        try:
            user = Profile.objects.get(id=obj.user_id)
            return f"{user.first_name} {user.last_name}"
        except Profile.DoesNotExist:
            return obj.user_id

    user_name.short_description = "Пользователь"

    def event_title(self, obj):
        """Get event's title."""
        try:
            event = Event.objects.get(id=obj.event_id)
            return event.title
        except Event.DoesNotExist:
            return obj.event_id

    event_title.short_description = "Мероприятие"

    def has_attended(self, obj):
        """Check if user attended (QR scanned)."""
        return QRScan.objects.filter(participation_id=obj.id).exists()

    has_attended.boolean = True
    has_attended.short_description = "Пришел"


@admin.register(QRScan)
class QRScanAdmin(admin.ModelAdmin):
    """Админ-интерфейс для сканирований QR-кодов."""

    list_display = ["participation_info", "scanned_by_user", "scanned_at"]
    list_filter = ["scanned_at"]
    search_fields = ["participation_id", "scanned_by_user_id"]
    readonly_fields = ["id", "participation_id", "scanned_by_user_id", "scanned_at"]

    def participation_info(self, obj):
        """Get participation info with links."""
        try:
            part = EventParticipation.objects.get(id=obj.participation_id)
            user = Profile.objects.get(id=part.user_id)
            event = Event.objects.get(id=part.event_id)
            user_url = reverse("admin:stats_profile_change", args=[user.id])
            event_url = reverse("admin:stats_event_change", args=[event.id])
            return format_html(
                '<a href="{}">{}</a> - <a href="{}">{}</a>',
                user_url,
                f"{user.first_name} {user.last_name}",
                event_url,
                event.title,
            )
        except (EventParticipation.DoesNotExist, Profile.DoesNotExist, Event.DoesNotExist):
            return obj.participation_id

    participation_info.short_description = "Участие"

    def scanned_by_user(self, obj):
        """Get scanner's name."""
        try:
            scanner = Profile.objects.get(max_id=obj.scanned_by_user_id)
            return f"{scanner.first_name} {scanner.last_name}"
        except Profile.DoesNotExist:
            return str(obj.scanned_by_user_id)

    scanned_by_user.short_description = "Сканировал"
