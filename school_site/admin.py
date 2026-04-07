from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SchoolSettings, HeroSection, Statistic, AboutSection, AboutFeature,
    Program, Teacher, Achievement, GalleryImage, ContactInfo, ApplicationRequest, ProgramCategory
)

# ── Базовый админ с медиа ───────────────────────────────────────────────
class SchoolAdminBase(admin.ModelAdmin):
    class Media:
        css = {'all': ('css/admin_fix.css',)}

# ── Категории программ ───────────────────────────────────────────────────
@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {"slug": ("name_ru",)}
    search_fields = ('name_ru', 'name_kg')


# ── Программы обучения ───────────────────────────────────────────────────
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name_ru", "cat_badge", "tag_ru", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("name_ru",)
    list_filter = ("category", "is_active")
    ordering = ("order",)
    # Временно отключено до применения миграций: prepopulated_fields = {"slug": ("name_ru",)}
    fieldsets = (
        ("Основная информация", {
            "description": "Название программы, тип (категория для фильтра) и иконка.",
            "fields": (
                "icon",
                "category",
                ("tag_ru", "tag_kg"),
                ("name_ru", "name_kg"),
            ),
        }),
        ("Описание", {"fields": ("description_ru", "description_kg")}),
        ("Длительность и размер класса", {"fields": (("duration_ru", "duration_kg"), ("class_size_ru", "class_size_kg"))}),
        ("Порядок и видимость", {"fields": (("order", "is_active"),)}),
    )

    def cat_badge(self, obj):
        if obj.category:
            colors = {"basic": "#0EA5E9", "extra": "#10B981", "optional": "#8B5CF6"}
            color = colors.get(obj.category.name_ru.lower() if obj.category.name_ru else "", "#888")
            return format_html(
                '<span style="background:{};color:#fff;padding:2px 10px;border-radius:20px;'
                'font-size:.78em;font-weight:600;white-space:nowrap">{}</span>',
                color, obj.category.name_ru
            )
        return format_html('<span style="background:#888;color:#fff;padding:2px 10px;border-radius:20px;">Без категории</span>')
    cat_badge.short_description = "Категория"


# ── Настройки школы ─────────────────────────────────────────────────────
@admin.register(SchoolSettings)
class SchoolSettingsAdmin(SchoolAdminBase):
    fieldsets = (
        ("Название и город", {
            "description": "Эти данные отображаются в шапке и подвале сайта.",
            "fields": (("name_ru", "name_kg"), ("city_ru", "city_kg"), "number"),
        }),
        ("Логотип", {"description": "Логотип PNG 200×200px", "fields": ("logo",)}),
        ("SEO — поисковая оптимизация", {
            "classes": ("collapse",),
            "description": "Заголовок и описание страницы для Google.",
            "fields": (("seo_title_ru", "seo_title_kg"), ("seo_description_ru", "seo_description_kg")),
        }),
    )
    def has_add_permission(self, request):
        return not SchoolSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


# ── Hero Section ───────────────────────────────────────────────────────
@admin.register(HeroSection)
class HeroSectionAdmin(SchoolAdminBase):
    fieldsets = (
        ("Бейдж над заголовком", {"fields": (("badge_ru", "badge_kg"),)}),
        ("Заголовок", {"fields": (("title_ru", "title_kg"), ("title_accent_ru", "title_accent_kg"))}),
        ("Описание", {"fields": (("description_ru", "description_kg"),)}),
        ("Текст кнопки «Записаться»", {"fields": (("btn_apply_ru", "btn_apply_kg"),)}),
    )
    # Временно отключено: prepopulated_fields = {"slug": ("title_ru",)}
    def has_add_permission(self, request):
        return not HeroSection.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


# ── Статистика ─────────────────────────────────────────────────────────
@admin.register(Statistic)
class StatisticAdmin(SchoolAdminBase):
    list_display = ("num_display", "label_ru", "label_kg", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
    # Временно отключено: prepopulated_fields = {"slug": ("label_ru",)}
    fieldsets = (
        ("Цифра и подпись", {"fields": (("number", "suffix"), ("label_ru", "label_kg"), "icon")}),
        ("Порядок и видимость", {"fields": (("order", "is_active"),)}),
    )
    def num_display(self, obj):
        return format_html('<b style="color:#0EA5E9;font-size:1.1em">{}{}</b>', obj.number, obj.suffix)
    num_display.short_description = "Число"


# ── О школе ─────────────────────────────────────────────────────────────
@admin.register(AboutSection)
class AboutSectionAdmin(SchoolAdminBase):
    fieldsets = (
        ("Заголовок и текст", {"fields": (("title_ru", "title_kg"), "text_ru", "text_kg")}),
        ("Фото", {"fields": ("photo",)}),
        ("Бейдж аккредитации", {"fields": (("accreditation_badge_ru","accreditation_badge_kg"), ("accreditation_org_ru","accreditation_org_kg"))}),
    )
    # Временно отключено: prepopulated_fields = {"slug": ("title_ru",)}
    def has_add_permission(self, request):
        return not AboutSection.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


# ── Преимущества ───────────────────────────────────────────────────────
@admin.register(AboutFeature)
class AboutFeatureAdmin(SchoolAdminBase):
    list_display = ("icon_prev", "title_ru", "title_kg", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
    # Временно отключено: prepopulated_fields = {"slug": ("title_ru",)}
    fieldsets = (
        ("Преимущество", {"fields": ("icon", ("title_ru", "title_kg"), "text_ru", "text_kg")}),
        ("Порядок и видимость", {"fields": (("order", "is_active"),)}),
    )
    def icon_prev(self, obj):
        return format_html('<i class="{}" style="font-size:1.3em;color:#0EA5E9"></i>', obj.icon)
    icon_prev.short_description = "Иконка"


# ── Педагоги ──────────────────────────────────────────────────────────
@admin.register(Teacher)
class TeacherAdmin(SchoolAdminBase):
    list_display = ("photo_thumb", "full_name", "subject_ru", "subject_kg", "cat_display", "experience_years", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
    # Временно отключено: prepopulated_fields = {"slug": ("full_name",)}
    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:38px;height:38px;border-radius:50%;object-fit:cover;border:2px solid #e2e8f0" />', obj.photo.url)
        return "—"
    photo_thumb.short_description = "Фото"
    def cat_display(self, obj):
        colors = {"highest": "#F59E0B", "first": "#0EA5E9", "second": "#6B7280"}
        return format_html('<span style="color:{};font-weight:600;font-size:.82em">{}</span>', colors.get(obj.category, "#888"), obj.get_category_display())
    cat_display.short_description = "Категория"


# ── Достижения ──────────────────────────────────────────────────────────
@admin.register(Achievement)
class AchievementAdmin(SchoolAdminBase):
    list_display = ("color_dot", "title_ru", "year", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
    # Временно отключено: prepopulated_fields = {"slug": ("title_ru",)}
    def color_dot(self, obj):
        colors = {"gold":"#F59E0B","blue":"#3B82F6","green":"#10B981","red":"#EF4444"}
        return format_html('<span style="color:{};font-size:1.4em;line-height:1">●</span>', colors.get(obj.color,"#888"))
    color_dot.short_description = "Цвет"


# ── Галерея ───────────────────────────────────────────────────────────
@admin.register(GalleryImage)
class GalleryImageAdmin(SchoolAdminBase):
    list_display = ("img_thumb", "caption_ru", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
    # Временно отключено: prepopulated_fields = {"slug": ("caption_ru",)}
    def img_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:48px;width:86px;object-fit:cover;border-radius:6px;border:1px solid #e2e8f0" />', obj.image.url)
        return "—"
    img_thumb.short_description = "Фото"


# ── Контакты ──────────────────────────────────────────────────────────
@admin.register(ContactInfo)
class ContactInfoAdmin(SchoolAdminBase):
    # Временно отключено: prepopulated_fields = {"slug": ("name",)}
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


# ── Заявки ───────────────────────────────────────────────────────────
@admin.register(ApplicationRequest)
class ApplicationRequestAdmin(SchoolAdminBase):
    list_display = ("name", "phone", "grade", "lang_display", "status_badge", "created_at")
    readonly_fields = ("name", "phone", "grade", "language", "message", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_filter = ("status", "language")
    search_fields = ("name", "phone")
    def status_badge(self, obj):
        colors = {"new":"#F59E0B","contacted":"#3B82F6","enrolled":"#10B981","declined":"#EF4444"}
        return format_html('<span style="background:{};color:#fff;padding:3px 12px;border-radius:20px;font-size:.78em;font-weight:600;white-space:nowrap">{}</span>', colors.get(obj.status,"#888"), obj.get_status_display())
    status_badge.short_description = "Статус"
    def lang_display(self, obj):
        return obj.get_language_display() if obj.language else "—"
    lang_display.short_description = "Язык"
    def has_add_permission(self, request):
        return False