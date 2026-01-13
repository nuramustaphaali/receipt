from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Receipt
from .forms import ReceiptForm, PassengerFormSet, ItemFormSet

@login_required
def receipt_create(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        passenger_formset = PassengerFormSet(request.POST)
        item_formset = ItemFormSet(request.POST)

        if form.is_valid() and passenger_formset.is_valid() and item_formset.is_valid():
            # 1. Save Parent (Receipt)
            receipt = form.save()
            
            # 2. Link Children to Parent and Save
            passenger_formset.instance = receipt
            passenger_formset.save()
            
            item_formset.instance = receipt
            item_formset.save()
            
            # 3. Redirect to the detail page we made in Phase 4
            return redirect('receipt_detail', pk=receipt.pk)
    else:
        form = ReceiptForm()
        passenger_formset = PassengerFormSet()
        item_formset = ItemFormSet()

    context = {
        'form': form,
        'passenger_formset': passenger_formset,
        'item_formset': item_formset,
    }
    return render(request, 'receipt_form.html', context)

# ... keep your existing receipt_detail view below ...
@login_required
def receipt_detail(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, 'receipt_detail.html', {'receipt': receipt})

# Add this import at the top if not there
from django.contrib.auth import logout 

@login_required
def receipt_list(request):
    # Get all receipts, newest first
    receipts = Receipt.objects.all().order_by('-created_at')
    return render(request, 'receipt_list.html', {'receipts': receipts})

import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from .models import Receipt

# Helper for images (Logo)
def link_callback(uri, rel):
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path

@login_required
def receipt_pdf(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    
    # We don't need font_path or base64 anymore.
    context = {'receipt': receipt}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Receipt_{receipt.invoice_number}.pdf"'

    template = get_template('receipt_pdf_template.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback
    )

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response