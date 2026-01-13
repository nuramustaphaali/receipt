from django.contrib import admin
from .models import Receipt, Passenger, Item

# This allows you to edit Passengers INSIDE the Receipt page
class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 1

# This allows you to edit Items INSIDE the Receipt page
class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    inlines = [PassengerInline, ItemInline]
    list_display = ['invoice_number', 'client_name', 'invoice_date', 'total_amount_display', 'status']
    search_fields = ['invoice_number', 'client_name']
    
    # We display the calculated property in the list view
    def total_amount_display(self, obj):
        return f"₦{obj.total_amount:,.2f}"
    total_amount_display.short_description = "Total Amount"