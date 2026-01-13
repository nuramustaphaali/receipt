from django.db import models
from django.utils import timezone

class Receipt(models.Model):
    # --- TOP SECTION ---
    invoice_number = models.CharField(max_length=50, unique=True, help_text="e.g. #Niv-Bishbc")
    invoice_date = models.DateField(default=timezone.now)
    client_name = models.CharField(max_length=200, help_text="Client Name (Top Left)")
    invoice_to = models.CharField(max_length=200, help_text="To: (Top Right)")
    
    STATUS_CHOICES = [
        ('PAID', 'PAID'),
        ('UNPAID', 'UNPAID'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PAID')

    # --- FOOTER SECTION ---
    departure_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.client_name}"

    @property
    def total_amount(self):
        """Calculates the grand total of all items dynamically."""
        return sum(item.total_price for item in self.items.all())


class Passenger(models.Model):
    # The 'related_name' allows us to do receipt.passengers.all() later
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='passengers')
    
    full_name = models.CharField(max_length=200)
    dob = models.DateField(verbose_name="Date of Birth")
    passport_number = models.CharField(max_length=50)
    
    GENDER_CHOICES = [('MALE', 'MALE'), ('FEMALE', 'FEMALE')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.full_name


class Item(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')
    
    description = models.CharField(max_length=200, default="RAMADAN UMRAH FULL PACKAGE")
    quantity = models.PositiveIntegerField(default=1)
    quantity_unit = models.CharField(max_length=50, default="PERSONS", help_text="e.g. PERSONS, TICKETS")
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, help_text="Price per unit")

    @property
    def total_price(self):
        """Calculates line total: Qty * Price"""
        return self.quantity * self.unit_price

    def __str__(self):
        return self.description