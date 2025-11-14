"""
Django models that map to existing database tables.
These models use db_table to point to existing tables.
"""

from django.db import models


class Profile(models.Model):
    """Профиль пользователя - модель для существующей таблицы profiles."""

    id = models.CharField(primary_key=True, max_length=255, verbose_name="ID")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    gender = models.CharField(max_length=1, null=True, blank=True, verbose_name="Пол")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    avatar = models.CharField(max_length=255, null=True, blank=True, verbose_name="Аватар")
    university = models.CharField(max_length=255, null=True, blank=True, verbose_name="Университет")
    bio = models.TextField(null=True, blank=True, verbose_name="О себе")
    max_id = models.BigIntegerField(unique=True, db_index=True, verbose_name="Max ID")
    invited_by = models.CharField(max_length=255, null=True, blank=True, verbose_name="Приглашен")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперпользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "profiles"
        managed = False
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.max_id})"


class Event(models.Model):
    """Мероприятие - модель для существующей таблицы events."""

    id = models.CharField(primary_key=True, max_length=255, verbose_name="ID")
    title = models.CharField(max_length=255, verbose_name="Название")
    body = models.TextField(verbose_name="Описание")
    photo = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фото")
    tags = models.JSONField(default=list, verbose_name="Теги")
    place = models.CharField(max_length=255, null=True, blank=True, verbose_name="Место")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    max_participants = models.IntegerField(null=True, blank=True, verbose_name="Макс. участников")
    registration_start_date = models.DateField(null=True, blank=True, verbose_name="Начало регистрации")
    registration_end_date = models.DateField(null=True, blank=True, verbose_name="Конец регистрации")
    status = models.CharField(max_length=1, default="A", verbose_name="Статус")
    creator = models.CharField(max_length=255, verbose_name="Создатель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "events"
        managed = False
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.title


class EventParticipation(models.Model):
    """Участие в мероприятии - модель для существующей таблицы event_participations."""

    id = models.CharField(primary_key=True, max_length=255, verbose_name="ID")
    user_id = models.CharField(max_length=255, db_index=True, verbose_name="Пользователь")
    event_id = models.CharField(max_length=255, db_index=True, verbose_name="Мероприятие")
    participation_type = models.CharField(max_length=1, default="V", verbose_name="Тип участия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "event_participations"
        managed = False
        unique_together = [["user_id", "event_id"]]
        verbose_name = "Участие в мероприятии"
        verbose_name_plural = "Участия в мероприятиях"

    def __str__(self):
        return f"Пользователь {self.user_id} - Мероприятие {self.event_id} ({self.participation_type})"


class QRScan(models.Model):
    """Сканирование QR-кода - модель для существующей таблицы qr_scans."""

    id = models.CharField(primary_key=True, max_length=255, verbose_name="ID")
    participation_id = models.CharField(max_length=255, db_index=True, verbose_name="Участие")
    scanned_by_user_id = models.BigIntegerField(db_index=True, verbose_name="Сканировал (Max ID)")
    scanned_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата сканирования")

    class Meta:
        db_table = "qr_scans"
        managed = False
        verbose_name = "Сканирование QR"
        verbose_name_plural = "Сканирования QR"

    def __str__(self):
        return f"Сканирование {self.id} - Участие {self.participation_id}"
