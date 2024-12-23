from django.db import models
from category.models import Category
from  django.urls import reverse
from account.models import Account
from django.utils.text import slugify

class Collection(models.Model):
    collection=models.CharField(max_length=500)
    collection_slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to="collection/",blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def save(self,*args,**kwargs):
        self.collection_slug=slugify(self.collection)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.collection


class Product(models.Model):
    product_name=models.CharField(max_length=500)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='products/')
    price=models.DecimalField(max_digits=10,decimal_places=2)
    is_available=models.BooleanField(default=True)
    details=models.TextField(blank=True,null=True)
    collections=models.ManyToManyField(Collection,related_name="product_collections")
    created_date=models.DateTimeField(auto_now_add=True)
    view_count=models.IntegerField(default=0)
    modified_at=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
        # Generate slug from name
            self.slug = slugify(self.product_name)

        # Check if the slug already exists
            if Product.objects.filter(slug=self.slug).exists():
            # If slug already exists, add a counter to make it unique
                counter = 1
                while True:
                    new_slug = f"{self.slug}-{counter}"
                    if not Product.objects.filter(slug=new_slug).exists():
                        self.slug = new_slug
                        break
                    counter += 1

        super().save(*args, **kwargs)


    def get_url(self):
        return reverse('product_details',args=[ self.slug])
    
    def __str__(self):
        return self.product_name


class ReviewRating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=500,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    status=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)





    def __str__(self):
        return self.subject






        
