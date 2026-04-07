from django.db import models
from django.utils.text import slugify

# ----------------------------------------------------------------------
# Настройки школы (только одна запись)
# ----------------------------------------------------------------------
class SchoolSettings(models.Model):
    name_ru = models.CharField("Название школы (рус)", max_length=120, default="Школа №1")
    name_kg = models.CharField("Название школы (кырг)", max_length=120, default="№1 Мектеп")
    number = models.CharField("Номер школы", max_length=20, blank=True, help_text="Например: №1")
    city_ru = models.CharField("Город (рус)", max_length=80, default="г. Бишкек")
    city_kg = models.CharField("Город (кырг)", max_length=80, default="Бишкек ш.")
    logo = models.ImageField("Логотип", upload_to="logo/", blank=True, null=True,
                             help_text="PNG с прозрачным фоном, ~200×200px")
    seo_title_ru = models.CharField("SEO заголовок (рус)", max_length=160, blank=True)
    seo_description_ru = models.TextField("SEO описание (рус)", blank=True)
    seo_title_kg = models.CharField("SEO заголовок (кырг)", max_length=160, blank=True)
    seo_description_kg = models.TextField("SEO описание (кырг)", blank=True)

    class Meta:
        verbose_name = "Настройки школы"
        verbose_name_plural = "Настройки школы"

    def __str__(self):
        return f"{self.name_ru} — настройки"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Hero-секция (только одна запись)
# ----------------------------------------------------------------------
class HeroSection(models.Model):
    badge_ru = models.CharField("Бейдж (рус)", max_length=120,
                                default="Приём на 2025/2026 год открыт")
    badge_kg = models.CharField("Бейдж (кырг)", max_length=120,
                                default="2025/2026-окуу жылына кабыл алуу ачык")
    title_ru = models.CharField("Заголовок строка 1 (рус)", max_length=120,
                                default="Качественное образование")
    title_kg = models.CharField("Заголовок строка 1 (кырг)", max_length=120,
                                default="Сапаттуу билим")
    title_accent_ru = models.CharField("Заголовок строка 2 (рус)", max_length=120,
                                       default="для каждого ребёнка")
    title_accent_kg = models.CharField("Заголовок строка 2 (кырг)", max_length=120,
                                       default="ар бир бала үчүн")
    description_ru = models.TextField("Описание (рус)",
                                      default="Школа №1 — современное учебное заведение.")
    description_kg = models.TextField("Описание (кырг)",
                                      default="№1 мектеп — заманбап билим берүү мекемеси.")
    btn_apply_ru = models.CharField("Кнопка 'Записаться' (рус)", max_length=60,
                                    default="Оставить заявку")
    btn_apply_kg = models.CharField("Кнопка 'Записаться' (кырг)", max_length=60,
                                    default="Билдирме калтыруу")
    slug = models.SlugField("Слаг", max_length=120, unique=False, blank=True, null=True)

    class Meta:
        verbose_name = "Hero-секция (главный экран)"
        verbose_name_plural = "Hero-секция (главный экран)"

    def __str__(self):
        return f"Hero: {self.title_ru}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_ru)
            slug = base_slug
            counter = 1
            while HeroSection.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        self.pk = 1
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Категории программ (динамические)
# ----------------------------------------------------------------------
class ProgramCategory(models.Model):
    name_ru = models.CharField("Название (рус)", max_length=50)
    name_kg = models.CharField("Название (кырг)", max_length=50)
    slug = models.SlugField("Слаг", max_length=50, unique=False, blank=True, null=True)
    order = models.PositiveSmallIntegerField("Порядок", default=1)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Категория программы"
        verbose_name_plural = "Категории программ"
        ordering = ["order"]

    def __str__(self):
        return self.name_ru

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name_ru)
            slug = base_slug
            counter = 1
            while ProgramCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Программы обучения
# ----------------------------------------------------------------------
class Program(models.Model):
    icon = models.CharField("Иконка Bootstrap Icons", max_length=60, default="bi bi-book-fill")
    category = models.ForeignKey(ProgramCategory, verbose_name="Категория программы",
                                 on_delete=models.SET_NULL, null=True, blank=True)
    tag_ru = models.CharField("Тег / классы (рус)", max_length=40, help_text="Например: 1–4 классы")
    tag_kg = models.CharField("Тег / классы (кырг)", max_length=40)
    name_ru = models.CharField("Название программы (рус)", max_length=120)
    name_kg = models.CharField("Название программы (кырг)", max_length=120)
    description_ru = models.TextField("Описание (рус)")
    description_kg = models.TextField("Описание (кырг)")
    duration_ru = models.CharField("Длительность (рус)", max_length=30, help_text="Например: 4 года")
    duration_kg = models.CharField("Длительность (кырг)", max_length=30)
    class_size_ru = models.CharField("Кол-во учеников (рус)", max_length=30,
                                     help_text="Например: 25 чел/класс")
    class_size_kg = models.CharField("Кол-во учеников (кырг)", max_length=30)
    order = models.PositiveSmallIntegerField("Порядок", default=1)
    is_active = models.BooleanField("Показывать", default=True)
    slug = models.SlugField("Слаг", max_length=120, unique=False, blank=True, null=True)

    class Meta:
        verbose_name = "Программа обучения"
        verbose_name_plural = "Программы обучения"
        ordering = ["order"]

    def __str__(self):
        cat_name = self.category.name_ru if self.category else "Без категории"
        return f"[{cat_name}] {self.name_ru}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name_ru)
            slug = base_slug
            counter = 1
            while Program.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Статистика
# ----------------------------------------------------------------------
class Statistic(models.Model):
    number = models.PositiveIntegerField("Число", help_text="Например: 850")
    suffix = models.CharField("Суффикс", max_length=10, default="+", blank=True, help_text="+ или %")
    label_ru = models.CharField("Подпись (рус)", max_length=80)
    label_kg = models.CharField("Подпись (кырг)", max_length=80)
    icon = models.CharField("Иконка Bootstrap Icons", max_length=60, default="bi bi-people",
                            help_text="bi bi-people / bi bi-mortarboard / bi bi-clock-history / bi bi-person-workspace")
    order = models.PositiveSmallIntegerField("Порядок", default=1)
    is_active = models.BooleanField("Показывать", default=True)
    slug = models.SlugField("Слаг", max_length=80, unique=False, blank=True, null=True)

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"
        ordering = ["order"]

    def __str__(self):
        return f"{self.number}{self.suffix} — {self.label_ru}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.label_ru)
            slug = base_slug
            counter = 1
            while Statistic.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# О школе (только одна запись)
# ----------------------------------------------------------------------
class AboutSection(models.Model):
    title_ru = models.CharField("Заголовок (рус)", max_length=200,
                                default="Школа с богатой историей и современным подходом")
    title_kg = models.CharField("Заголовок (кырг)", max_length=200,
                                default="Бай тарыхы жана заманбап мамилеси бар мектеп")
    text_ru = models.TextField("Основной текст (рус)", help_text="Например: Основана в 1993 году...")
    text_kg = models.TextField("Основной текст (кырг)")
    photo = models.ImageField("Фото школы", upload_to="about/", blank=True, null=True,
                              help_text="Рекомендуется 800×600px")
    accreditation_badge_ru = models.CharField("Бейдж аккредитации (рус)", max_length=60, default="Аккредитована")
    accreditation_badge_kg = models.CharField("Бейдж аккредитации (кырг)", max_length=60, default="Аккредитацияланган")
    accreditation_org_ru = models.CharField("Орган аккредитации (рус)", max_length=60, default="МОиН КР")
    accreditation_org_kg = models.CharField("Орган аккредитации (кырг)", max_length=60, default="КР БИМ")
    slug = models.SlugField("Слаг", max_length=200, unique=False, blank=True, null=True)

    class Meta:
        verbose_name = "О школе (текст и фото)"
        verbose_name_plural = "О школе (текст и фото)"

    def __str__(self):
        return f"О школе: {self.title_ru}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_ru)
            slug = base_slug
            counter = 1
            while AboutSection.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        self.pk = 1
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Преимущества школы
# ----------------------------------------------------------------------
class AboutFeature(models.Model):
    icon = models.CharField("Иконка Bootstrap Icons", max_length=60, default="bi bi-mortarboard-fill",
                            help_text="bi bi-mortarboard-fill / bi bi-laptop / bi bi-translate / bi bi-shield-check")
    title_ru = models.CharField("Заголовок (рус)", max_length=120)
    title_kg = models.CharField("Заголовок (кырг)", max_length=120)
    text_ru = models.TextField("Текст (рус)")
    text_kg = models.TextField("Текст (кырг)")
    order = models.PositiveSmallIntegerField("Порядок", default=1)
    is_active = models.BooleanField("Показывать", default=True)
    slug = models.SlugField("Слаг", max_length=120, unique=False, blank=True, null=True)

    class Meta:
        verbose_name = "Преимущество школы"
        verbose_name_plural = "Преимущества школы"
        ordering = ["order"]

    def __str__(self):
        return self.title_ru

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_ru)
            slug = base_slug
            counter = 1
            while AboutFeature.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Педагоги
# ----------------------------------------------------------------------
class Teacher(models.Model):
    CAT = [
        ("highest", "Высшая категория"),
        ("first", "Первая категория"),
        ("second", "Вторая категория"),
    ]
    photo = models.ImageField("Фото педагога", upload_to="teachers/", blank=True, null=True,
                              help_text="Квадратное фото, ~400×400px")
    full_name = models.CharField("ФИО", max_length=120)
    subject_ru = models.CharField("Предмет (рус)", max_length=100)
    subject_kg = models.CharField("Предмет (кырг)", max_length=100)
    category = models.CharField("Квалификационная категория", max_length=20, choices=CAT, default="first")
    experience_years = models.PositiveSmallIntegerField("Стаж (лет)", default=5)
    order = models.PositiveSmallIntegerField("Порядок", default=1)
    is_active = models.BooleanField("Показывать", default=True)
    slug = models.SlugField("Слаг", max_length=120, unique=False, blank=True, null=True)

    class Meta:
        verbose_name = "Педагог"
        verbose_name_plural = "Педагоги"
        ordering = ["order"]

    def __str__(self):
        return f"{self.full_name} — {self.subject_ru}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.full_name)
            slug = base_slug
            counter = 1
            while Teacher.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Достижения школы
# ----------------------------------------------------------------------
class Achievement(models.Model):
    COLOR = [
        ("gold", "Золотой"),
        ("blue", "Синий"),
        ("green", "Зелёный"),
        ("red", "Красный"),
    ]
    icon = models.CharField("Иконка Bootstrap Icons", max_length=60, default="bi bi-trophy-fill")
    color = models.CharField("Цвет иконки", max_length=10, choices=COLOR, default="gold")
    title_ru = models.CharField("Заголовок (рус)", max_length=200)
    title_kg = models.CharField("Заголовок (кырг)", max_length=200)
    text_ru = models.TextField("Описание (рус)")
    text_kg = models.TextField("Описание (кырг)")
    year = models.CharField("Год", max_length=20, help_text="Например: 2024 или 2023–2024")
    order = models.PositiveSmallIntegerField("Порядок", default=1)
    is_active = models.BooleanField("Показывать", default=True)
    slug = models.SlugField("Слаг", max_length=200, unique=False, blank=True, null=True)

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"
        ordering = ["order"]

    def __str__(self):
        return f"{self.title_ru} ({self.year})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_ru)
            slug = base_slug
            counter = 1
            while Achievement.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Галерея изображений
# ----------------------------------------------------------------------
class GalleryImage(models.Model):
    image = models.ImageField("Фотография", upload_to="gallery/", help_text="Рекомендуется 1200×500px")
    caption_ru = models.CharField("Подпись (рус)", max_length=120, blank=True)
    caption_kg = models.CharField("Подпись (кырг)", max_length=120, blank=True)
    order = models.PositiveSmallIntegerField("Позиция в карусели", default=1)
    is_active = models.BooleanField("Показывать", default=True)
    slug = models.SlugField("Слаг", max_length=120, unique=False, blank=True, null=True)

    class Meta:
        verbose_name = "Фото галереи"
        verbose_name_plural = "Галерея"
        ordering = ["order"]

    def __str__(self):
        return f"Фото #{self.order} — {self.caption_ru or 'без подписи'}"

    def save(self, *args, **kwargs):
        if not self.slug and self.caption_ru:
            base_slug = slugify(self.caption_ru)
            slug = base_slug
            counter = 1
            while GalleryImage.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        elif not self.slug:
            # Если нет подписи, генерируем на основе order
            self.slug = f"image-{self.order}"
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Контактная информация (только одна запись)
# ----------------------------------------------------------------------
class ContactInfo(models.Model):
    name = models.CharField("Название (для слага)", max_length=60, default="contacts",
                            help_text="Используется для генерации ЧПУ, например 'contacts'")
    address_ru = models.CharField("Адрес (рус)", max_length=200, default="г. Бишкек, ул. Примерная, 1")
    address_kg = models.CharField("Адрес (кырг)", max_length=200, default="Бишкек ш., Үлгүлүү к., 1")
    phone = models.CharField("Телефон", max_length=30, default="+996 312 00-00-00")
    email = models.EmailField("Email", blank=True)
    working_hours_ru = models.CharField("Режим работы (рус)", max_length=80, default="Пн–Сб, 8:00 – 18:00")
    working_hours_kg = models.CharField("Режим работы (кырг)", max_length=80, default="Дш–Иш, 8:00 – 18:00")
    map_embed_url = models.URLField("Google Maps embed URL", max_length=1000, blank=True,
                                    help_text="URL из атрибута src= в коде вставки карты Google Maps")
    telegram_url = models.URLField("Telegram", blank=True, help_text="https://t.me/school_name")
    whatsapp_number = models.CharField("WhatsApp номер", max_length=20, blank=True,
                                       help_text="996312000000 — только цифры, без + и пробелов")
    instagram_url = models.URLField("Instagram", blank=True, help_text="https://instagram.com/school_name")
    slug = models.SlugField("Слаг", max_length=60, unique=False, blank=True, null=True)

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"Контакты: {self.phone}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while ContactInfo.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        self.pk = 1
        super().save(*args, **kwargs)


# ----------------------------------------------------------------------
# Заявки на запись (без слага)
# ----------------------------------------------------------------------
class ApplicationRequest(models.Model):
    STATUS = [
        ("new", "Новая"),
        ("contacted", "Связались"),
        ("enrolled", "Записан"),
        ("declined", "Отказ"),
    ]
    LANG = [
        ("ru", "Русский"),
        ("kg", "Кыргызский"),
    ]
    name = models.CharField("Имя родителя", max_length=120)
    phone = models.CharField("Телефон", max_length=30)
    grade = models.CharField("Класс / Возраст", max_length=30, blank=True)
    language = models.CharField("Язык обучения", max_length=5, choices=LANG, blank=True)
    message = models.TextField("Комментарий", blank=True)
    status = models.CharField("Статус заявки", max_length=15, choices=STATUS, default="new")
    created_at = models.DateTimeField("Дата и время заявки", auto_now_add=True)
    notes = models.TextField("Заметки администратора", blank=True, help_text="Видны только в панели управления")

    class Meta:
        verbose_name = "Заявка на запись"
        verbose_name_plural = "Заявки на запись"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.phone}) — {self.get_status_display()}"