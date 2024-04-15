from django.db import models
from user_auth.models import User
from datetime import timezone
# Create your models here.

# added_by = created_by

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='product_created_by', null=True,
                                   blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_updated_by', null=True,
                                   blank=True)

class Order(models.Model):

    status_choices = (
            ("booked", "booked"),
            ("in_process", "in_process"),
            ("delivered", "delivered")
        )

    bill = models.PositiveBigIntegerField(null=True, blank=True)
    delivery_address = models.TextField()
    status = models.CharField(max_length=50, choices = status_choices, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_rider', null=True,blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_customer', null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderDetail(models.Model):
    unit_price = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveBigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_detail_product')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_detail_order')

# class rider(models.Model):
#     name = models.CharField(max_length=50)
#     vehicle_type = models.CharField(max_length=50)
#     contact_number = models.PositiveIntegerField()