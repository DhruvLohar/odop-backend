from django.db import models

ORDER_STATUS = [
    ('PEN', 'Pending'),
    ('CON', 'Confirmed'),
    ('SHP', 'Shipped'),
    ('DLV', 'Delivered'),
    
    ('RFI', 'Refund Initiated'),
    ('RFP', 'Refund In Process'),
    ('RFS', 'Refund Successs'),
    ('RFC', 'Refund Cancelled'),
    
    ('CAN', 'Cancelled'),
]

PAYMENT_MODE = [
    ('ONLINE', 'UPI / Gpay / Cards'),
    ('COD', 'Cash on Delivery'),
]

class Order(models.Model):
    
    user = models.ForeignKey('user.User', related_name='orders', on_delete=models.PROTECT)

    status = models.CharField(max_length=50, choices=ORDER_STATUS)
    shipping_address = models.TextField()
    estimate_delivery_time = models.PositiveIntegerField(null=True, blank=True) # in days

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user

class OrderLineItem(models.Model):
    order = models.ForeignKey("order.Order", related_name="related_line_items", on_delete=models.PROTECT)
    product = models.ForeignKey("user.User", related_name="related_order_lines", on_delete=models.PROTECT)
    
    buying_quantity = models.PositiveIntegerField()
    
    subtotal = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.product.title
    
    def calculateCosting(self):
        subtotal = self.product.price * self.product.quantity
        taxable_amount = subtotal * (self.product.tax_percent / 100)
        
        self.subtotal = subtotal
        self.total = subtotal + taxable_amount
        
        self.save()