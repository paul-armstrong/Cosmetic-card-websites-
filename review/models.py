from django.db import models
from store.models import Product
# Create your models here.

class Review(models.Model):
    name=models.TextField()
    email=models.TextField()
    review_title=models.TextField(blank=True,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    review_content=models.TextField()
    rating=models.IntegerField()
    created_at=models.DateField(auto_now_add=True)



