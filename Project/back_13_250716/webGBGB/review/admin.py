from django.contrib import admin
from review.models import Review
from review.models import ReviewImage
# Register your models here.
admin.site.register(Review)
admin.site.register(ReviewImage)