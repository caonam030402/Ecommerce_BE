from django.contrib import admin
from .models.purchase import Purchase
from .models.product import Product, Category
from .models.promotion import PromotionTimeSlots, Promotion

# Register your models here.
admin.site.register(Category)
admin.site.register(PromotionTimeSlots)
admin.site.register(Product)
admin.site.register(Purchase)
# admin.site.register(ProductImage)
admin.site.register(Promotion)
