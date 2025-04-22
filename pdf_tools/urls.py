from django.urls import path
from . import views
from django.shortcuts import render
from .views import feedback_view

urlpatterns = [
    path('', views.login_view, name='login'),
    path("admin-only/", views.admin_only_page, name="admin_only"),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    # path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_acc, name='signup'),
    path("feedback/", views.feedback_view, name="feedback"),
    path('merge_pdf/',views.merge_pdf, name='merge_pdf'),
    path("split/", views.split_pdf, name="split"),
    path("faq/", views.faq, name="faq"),
    path("compress/", views.compress_pdf_view, name="compress_page"),
    path("compress-pdf/", views.compress_pdf, name="compress_pdf"),
    path('extract-text/', views.extract_text, name='extract_text'),
    path('rotate_pdf/', views.rotate_pdf, name='rotate_pdf'),
    path('edit_pdf/', views.edit_pdf, name='edit_pdf'),


    # File operations
    path("shared_files/", views.shared_files, name="shared_files"),
    path("recent_files/", views.recent_files, name="recent_files"),

    # PDF Tools
    path('merge_pdf/',views.merge_pdf, name='merge_pdf'),
    # path("split/", views.split, name="split"),
    # path("split_pdf/pdf/", views.split_pdf, name="split_pdf"),
    path('compress/', views.compress_pdf, name='compress_pdf'),
    path("extract_text/", views.extract_text, name="extract_text"),
    path('watermark_removal/', views.watermark_removal, name='watermark_removal'),
    path('add_annotations/', views.add_annotations, name='add_annotations'),
    # path('remove_pages/', views.remove_pages, name='remove_pages'),
    path('remove_pages', views.remove_pages, name='remove_pages'),
    path('remove_pages_ui', lambda request: render(request, 'remove_page.html'), name='remove_pages'),
    path('convert-word/', views.convert_pdf_to_word, name='convert_word'),
    path('support/', views.support, name='support'),
    path("convert_word_to_pdf/", views.convert_word_to_pdf, name="convert_word_to_pdf"),
    path("convert_pdf_to_word/", views.convert_pdf_to_word, name="convert_pdf_to_word"),
    path("convert_pdf_to_image/", views.convert_pdf_to_image, name="convert_pdf_to_image"),
    path('convert_pdf_to_excel/', views.convert_pdf_to_excel, name='convert_pdf_to_excel'),
    path("submit-support/", views.submit_support_request, name="submit-support"),




    path('rearrange-pages/', views.rearrange_pages, name='rearrange_pages'),
    path('sign_pdf/', views.sign_pdf, name='sign_pdf'),

    # PDF Conversion
    #
    # path('convert-excel/', views.convert_excel, name='convert_excel'),
    # path('convert-image/', views.convert_image, name='convert_image'),
    path('ocr/', views.ocr, name='ocr'),
]
