from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from core.views import receipt_detail, receipt_create, receipt_list # Import new view
from core.views import receipt_detail, receipt_create, receipt_list, receipt_pdf # Import receipt_pdf
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('receipt_list') # <--- Redirects to Dashboard now
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # Handles logout routing automatically
    path('', root_redirect, name='root'),
    
    # App URLs
    path('receipts/', receipt_list, name='receipt_list'), # The Dashboard
    path('receipts/create/', receipt_create, name='receipt_create'),
    path('receipts/<int:pk>/', receipt_detail, name='receipt_detail'),
    path('receipts/<int:pk>/pdf/', receipt_pdf, name='receipt_pdf'),
]
