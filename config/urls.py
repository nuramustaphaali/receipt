from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views  # <--- NEW IMPORT
from core.views import receipt_detail, receipt_create, receipt_list, receipt_pdf

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('receipt_list')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. ADD THIS LINE to create the actual /login/ page
    path('login/', auth_views.LoginView.as_view(), name='login'),

    # Keep this for other auth features (like logout default handling)
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', root_redirect, name='root'),
    
    # App URLs
    path('receipts/', receipt_list, name='receipt_list'),
    path('receipts/create/', receipt_create, name='receipt_create'),
    path('receipts/<int:pk>/', receipt_detail, name='receipt_detail'),
    path('receipts/<int:pk>/pdf/', receipt_pdf, name='receipt_pdf'),
]