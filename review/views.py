from django.shortcuts import render
from review.models import Review
from django.http import JsonResponse
import json
from store.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

@csrf_exempt
def add_review(request):
    if request.method=="POST":
        try:
            data=json.loads(request.body)
            name=data.get('name')
            email=data.get('email')
            review_title=data.get('review_title')
            rating=int(data.get('rating'))
            review_content=data.get('review_content')
            product_id=data.get('product_id')
            product=Product.objects.get(id=product_id)
            review=Review.objects.create(name=name,email=email,review_title=review_title,rating=rating,review_content=review_content,product=product)

            return JsonResponse({'review':model_to_dict(review),'created_at':review.created_at},status=200)
        except Exception as e:
            error=str(e)
          
            return JsonResponse({'error':f"Unexpected error occured {error}"},status=400)
