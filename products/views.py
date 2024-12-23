from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from store.models import Product, Collection
from account.models import Account
from review.models import Review
from django.db.models import Q
from django.db.models import Avg, Sum, Count
from django.template.loader import render_to_string

# Create your views here.
import json


@csrf_exempt
def products(request):
    if request.method == "GET":
        filter_products = request.GET.get("filter", "")

        products_with_avg_rating = Product.objects.annotate(
            avg_rating=Sum("reviews__rating") / Count("reviews"),
            reviews_count=Count("reviews"),
        )

        if filter_products != "":
            filtered_products = None
            if filter_products == "recommended":
                filtered_products = products_with_avg_rating.order_by("-view_count")
            elif filter_products == "best-selling":
                filtered_products = products_with_avg_rating.order_by("avg_rating","-reviews")
            elif filter_products == "price-ascending":
                filtered_products = products_with_avg_rating.order_by("price")
            elif filter_products == "price-descending":
                filtered_products = products_with_avg_rating.order_by("-price")
            elif filter_products == "created-descending":
                filtered_products = products_with_avg_rating.order_by("-id")
            context = {"products": filtered_products}
            content_html = render_to_string(
                "renderer/products.html", context, request=request
            )
            return JsonResponse({"content": content_html})

        products = products_with_avg_rating.order_by("-id")
        context = {
            "products": products
        }
        return render(request, "products.html", context)
    if request.method == "POST":
        try:
            user = request.user
            if not user.is_authenticated:
                raise Exception("User is not authenticated")

            product = Product.objects.create(
                product_name=request.POST.get("name"),
                price=request.POST.get("price"),
                description=request.POST.get("description"),
                image=request.FILES.get("image"),
                details=request.POST.get("details"),
                created_by=user,
            )

            # Return a success response
            return JsonResponse({"message": "Product added successfully"})
        except KeyError:
            # Return error response if required fields are missing
            return JsonResponse({"error": "Invalid data format"}, status=400)
        except Exception as e:
           
            # Return error response for other exceptions
            return JsonResponse({"error": str(e)}, status=500)


def get_product(request, product_name):
    if request.method == "GET":
        try:
            product = Product.objects.get(slug=product_name)
            product.view_count = product.view_count + 1
            product.save()
            reviews = Review.objects.filter(product=product).order_by("-id")
            total_rating = 0
            for review in reviews:
                total_rating += review.rating
            if reviews.count() > 0:
                average_rating = total_rating / reviews.count()
            else:
                average_rating = 0

           
            similar_products = Product.objects.filter(~Q(id=product.id)).order_by("?")[
                :4
            ]
            context = {
                "product": product,
                "reviews": reviews,
                "similar_products": similar_products,
                "average_rating": average_rating,
            }
            return render(request, "product.html", context)
        except Exception as e:
            error = str(e)
          
            context = {"error": error}
            return render(request, "product.html", context)


@csrf_exempt
def collection(request, collection_slug=None):
    if request.method == "GET":
        if collection_slug is None:
            collections = Collection.objects.all().order_by("-id")
            context = {"collections": collections}
            return render(request, "collections.html", context)
        else:
            try:
                filter_products = request.GET.get("filter", "")
                collection = Collection.objects.get(collection_slug=collection_slug)
               
                products = Product.objects.annotate(
                    avg_rating=Sum("reviews__rating") / Count("reviews"),
                    reviews_count=Count("reviews"),
                ).filter(collections=collection)

                if filter_products != "":
                    filtered_products = None

                    if filter_products == "recommended":
                        filtered_products = products.order_by("-avg_rating")
                    elif filter_products == "best-selling":
                        filtered_products = products.order_by("-view_count")
                    elif filter_products == "price-ascending":
                        filtered_products = products.order_by("price")
                    elif filter_products == "price-descending":
                        filtered_products = products.order_by("-price")
                    elif filter_products == "created-descending":
                        filtered_products = products.order_by("-id")
                    context1 = {"products": filtered_products}
                    content_html = render_to_string(
                        "renderer/products.html", context1, request=request
                    )
                   
                    return JsonResponse({"content": content_html})
                products = products.order_by("-id")
             
                context = {
                    "collection": collection,
                    "products": products,
                }
                
                return render(request, "products.html", context)
            except Exception as e:
                context = {"error": str(e)}
                return render(request, "collections.html", context)
    if request.method == "POST":
        try:
           
            # user=request.user
            # if not user.is_authenticated:
            #     raise Exception("user is not authenticated")
            data = json.loads(request.body)
            Collection.objects.create(collection=data.get("collection_name"))
            return JsonResponse({"message": "collection sucesfully added"})

        except Exception as e:
            return JsonResponse({"error": f"Unexpected error {str(e)}"}, status=400)


@csrf_exempt
def run_script(request):
    if request.method == "POST":
        try:
            user = Account.objects.get(email="san@gmail.com")
            data = json.loads(request.body)
            serialized_details = json.dumps(data.get("details"))
            product = Product.objects.create(
                product_name=data.get("name"),
                price=data.get("price"),
                description=data.get("description"),
                image=data.get("large_image"),
                details=serialized_details,
                created_by=user,
            )

            # Return a success response
            return JsonResponse({"message": "Product added successfully"})
        except KeyError:
            # Return error response if required fields are missing
            return JsonResponse({"error": "Invalid data format"}, status=400)
        except Exception as e:
        
            # Return error response for other exceptions
            return JsonResponse({"error": str(e)}, status=500)
