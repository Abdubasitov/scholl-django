from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from school_site import views

admin.site.site_title = "SchoolAdmin"
admin.site.site_header = "🏫 Управление сайтом школы"
admin.site.index_title = "Панель управления"

urlpatterns = [
    path('', views.index, name='index'),
    path('apply/', views.apply, name='apply'),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
