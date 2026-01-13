from django import forms
from django.forms import inlineformset_factory
from .models import Receipt, Passenger, Item

class DateInput(forms.DateInput):
    input_type = 'date'

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
        widgets = {
            'invoice_date': DateInput(),
            'departure_date': DateInput(),
            'return_date': DateInput(),
        }

# Inline Formsets
# These allow us to edit Passengers and Items attached to a specific Receipt
PassengerFormSet = inlineformset_factory(
    Receipt, Passenger, 
    fields=['full_name', 'dob', 'passport_number', 'gender'],
    widgets={'dob': DateInput()},
    extra=1,    # Start with 1 empty row
    can_delete=True
)

ItemFormSet = inlineformset_factory(
    Receipt, Item,
    fields=['description', 'quantity', 'quantity_unit', 'unit_price'],
    extra=1,    # Start with 1 empty row
    can_delete=True
)