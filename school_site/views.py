from django.shortcuts import render
from django.http import JsonResponse
from .models import (
    SchoolSettings, HeroSection, Statistic, AboutSection, AboutFeature,
    Program, ProgramCategory, Teacher, Achievement, GalleryImage, ContactInfo, ApplicationRequest
)

def index(request):
    ctx = {
        'school':    SchoolSettings.objects.first(),
        'hero':      HeroSection.objects.first(),
        'stats':     Statistic.objects.filter(is_active=True),
        'about':     AboutSection.objects.first(),
        'features':  AboutFeature.objects.filter(is_active=True),
        'programs':  Program.objects.filter(is_active=True),
        'categories': ProgramCategory.objects.filter(is_active=True),
        'teachers':  Teacher.objects.filter(is_active=True),
        'achievements': Achievement.objects.filter(is_active=True),
        'gallery':   GalleryImage.objects.filter(is_active=True),
        'contacts':  ContactInfo.objects.first(),
    }
    return render(request, 'index.html', ctx)

def apply(request):
    if request.method == 'POST':
        ApplicationRequest.objects.create(
            name=request.POST.get('name', '').strip(),
            phone=request.POST.get('phone', '').strip(),
            grade=request.POST.get('grade', '').strip(),
            language=request.POST.get('language', '').strip(),
            message=request.POST.get('message', '').strip(),
        )
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)