from django.contrib import admin
from .models import CarModel, CarMake


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3


# CarModelAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]


# Register your models here.
admin.site.register(CarModel)
admin.site.register(CarMake, CarMakeAdmin)

