# 🏫 SchoolAdmin — Django + Jazzmin CMS для школ КР

## 🚀 Быстрый старт

```bash
# 1. Установить зависимости
pip install django django-jazzmin pillow

# 2. Применить миграции
python manage.py migrate

# 3. Создать администратора
python manage.py createsuperuser

# 4. Запустить сервер
python manage.py runserver
```

Открыть: http://127.0.0.1:8000/admin/

---

## 👤 Демо-данные

Уже загружены тестовые данные. Логин: **admin** / Пароль: **admin123**

---

## 📋 Что можно настроить

| Раздел | Что меняется на сайте |
|--------|----------------------|
| ⚙️ Настройки школы | Название, город, цвета, логотип |
| 🌟 Hero-секция | Главный экран: заголовок, описание, бейдж |
| 📊 Статистика | Цифры (ученики, педагоги, лет опыта) |
| ℹ️ О школе | Текст, фото здания, бейдж аккредитации |
| ✅ Преимущества | Иконки в блоке «О школе» |
| 📚 Программы | Карточки учебных программ |
| 👨‍🏫 Педагоги | Список учителей с фото |
| 🏆 Достижения | Победы и награды |
| 🖼️ Галерея | Фотокарусель |
| 📞 Контакты | Адрес, телефон, карта, соцсети |
| 📩 Заявки | Входящие заявки с сайта |

---

## 🔧 Подключение к сайту

Используйте данные из моделей в шаблоне `index.html`:

```python
# views.py
from school_site.models import SchoolSettings, HeroSection, ...

def index(request):
    return render(request, 'index.html', {
        'school': SchoolSettings.objects.first(),
        'hero': HeroSection.objects.first(),
        'stats': Statistic.objects.filter(is_active=True),
        ...
    })
```
