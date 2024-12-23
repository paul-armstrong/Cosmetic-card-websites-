from django.shortcuts import render,redirect
from store.models import Collection,Product
from django. contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from account.models import Account
from cart.models import Payment,Order,Order_Product,Personalization
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum,Count
import json
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


def is_superadmin(user):
    return user.is_authenticated and user.is_superadmin

@user_passes_test(is_superadmin)

def dashboard(request):
    latest_users = Account.objects.order_by('-id')[:5]
    latest_product = Product.objects.order_by('-id')[:5]
    top_five_products = Product.objects.order_by('-view_count')[:5]
    get_data=Product.objects.all().count()
    total_price =Payment.objects.aggregate(total_price=Sum('amount_paid'))
    sum_of_prices = total_price['total_price']
    if sum_of_prices is None:
        sum_of_prices=0
    context={
        'latest_users':latest_users,
        'latest_product':latest_product,
        'top_products':top_five_products,
        'get_data':get_data,
        'total':sum_of_prices
    }
    
    return render(request,'owner/index.html',context)


@user_passes_test(is_superadmin)
@csrf_exempt
def add_item(request):
    if request.method == 'POST' and request.FILES.get('form__img-upload'):
        large_image=request.FILES['form__img-upload']
        product_name=request.POST['product_name']
        descriptions=request.POST['descriptions']
        price=request.POST['price']
        details=request.POST['details']
        category=request.POST.getlist('category')
        details_array = details.split('\n')
        
        product=Product(
            product_name=product_name,
            description=descriptions,
            details=json.dumps(details_array),
            price=price,
            image=large_image,
           
            
        )
        product.save()
        categories = Collection.objects.filter(pk__in=category)
        for category in categories:
            product.collections.add(category)
        
        
        messages.success(request,'Item has been added sucessfully')
        return redirect('add_item')
        
        
    else:
        collection=Collection.objects.all()
       
        context={
            'collections':collection
        }
            
       

    return render(request,'owner/add-item.html',context)

@user_passes_test(is_superadmin)
@csrf_exempt
def catalog(request):
    context = {}
    keyword=''
    products = Product.objects.all().order_by('-id')
    
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        if keyword:
            products = products.filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
    
    count = products.count()
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context['products'] = paged_products
    context['all_products']=paged_products
    context['count'] = count
    context['keyword'] = keyword

    return render(request, 'owner/catalog.html', context)


@user_passes_test(is_superadmin)
def remove_product(request,id):
  product=Product.objects.get(id=id)
  product.delete()
  messages.success(request,'Item has been sucessfully deleted')
  return redirect('catalog')


@user_passes_test(is_superadmin)
@csrf_exempt
def edit_product(request,id):
    product=Product.objects.get(id=id)
    if request.method=="POST":
        large_image = request.FILES.get('form__img-upload')
        product_name = request.POST['product_name']
        descriptions = request.POST['descriptions']
        details = request.POST['details']
        price = request.POST['price']
        category=request.POST.getlist('category')  
        
        if large_image: 
            product.image = large_image        
        if product_name:
            product.product_name = product_name
      
        if descriptions:
            product.description = descriptions
        if details:
            product.details = details
        if price:
            product.price = price
        
        # Clear existing collections and add selected ones if new categories are provided
        if category:
            product.collections.clear()
            categories = Collection.objects.filter(pk__in=category)
            for category in categories:
               product.collections.add(category)
        product.save()
       
        return redirect('catalog')
        
    else:
        context={
            'product':product,
            'collections':Collection.objects.all(),
            "description":product.description,
            'id':id,
           
        }
    return render(request,'owner/edit_product.html',context)



@user_passes_test(is_superadmin)
def user_list(request):
    if request.method == "POST":
        toSearch = request.POST['user_name']
        userlist = Account.objects.filter(
            Q(first_name__icontains=toSearch) | Q(email__icontains=toSearch) | Q(last_name__icontains=toSearch)
        ).order_by('-id')
    else:
        userlist = Account.objects.all().order_by('-id')

    payment = Payment.objects.all().order_by('-id')
    count = userlist.count()
    paginator = Paginator(userlist, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    # Initialize user_totals dictionary to store total paid amount for each user
    user_totals = {}

     # Calculate the total amount paid by each user
    for payment_record in payment:
        user = payment_record.user
        amount_paid = payment_record.amount_paid
        if user in user_totals:
            user_totals[user]['total_paid'] += amount_paid
        else:
            user_totals[user] = {'user': user, 'total_paid': amount_paid}
    # Update user_totals_list with calculated totals
    user_totals_list = user_totals.values()
   

    context = {
        'users': paged_products,
        'count': count,
        'user_totals_list': user_totals_list,
        'all_products': paged_products
    }

    return render(request, 'owner/users.html', context)


@user_passes_test(is_superadmin)
def suspended_user(request,id):

  user=Account.objects.get(id=id)
  if user is not None:
    user.is_active=False
    user.save()
    return redirect('user_list')


@user_passes_test(is_superadmin)
def delete_user(request,id):
  user=Account.objects.get(id=id)
  user.delete()
  return redirect('user_list')


@user_passes_test(is_superadmin)
def active_user(request,id):

  user=Account.objects.get(id=id)
  if user is not None:
    user.is_active=True
    user.save()
    return redirect('user_list')
    
    
@user_passes_test(is_superadmin)  
def add_collection(request):
    if request.method=='POST':
        category=request.POST['category_name']
        descriptions=request.POST['descriptions']
        large_image=request.FILES['image']
        collection=Collection.objects.create(collection=category,description=descriptions,image=large_image)
        messages.success(request,'Collection has been added!')
        return redirect('add_collection')
        
        
    return render(request,'owner/add_collection.html')    

@user_passes_test(is_superadmin)
def show_collection(request):
    collection=Collection.objects.all()
    context={}
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        if keyword:
            collection = collection.filter(
                Q(description__icontains=keyword) | Q(collection__icontains=keyword)
            )
    else:  
        pass
        
    count=collection.count()
    paginator = Paginator(collection, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context={
        'collection':paged_products,
        'count':count,
        'all_products':paged_products
    }
    
    return render(request,'owner/show_collection.html',context)

@user_passes_test(is_superadmin)
def delete_collection(request,id):
    category=Collection.objects.get(id=id)
    category.delete()
    messages.success(request,'collection has been deleted')
    return redirect('show_collection')


@user_passes_test(is_superadmin)
def edit_collection(request,id):
    collection=Collection.objects.get(id=id)
    if request.method=="POST":
        large_image = request.FILES.get('image')
        category_name = request.POST['category_name']
        descriptions = request.POST['descriptions']
        if large_image: 
            collection.image = large_image        
        if category_name:
            collection.collection =category_name
      
        if descriptions:
            collection.description = descriptions
        collection.save()
        messages.success(request,'item has been edited')
        return redirect('show_collection')
    
    else:
        context={
            'collection':collection,
            'id':id
        }
        
    return render(request,'owner/edit_collection.html',context)    
from django.db.models import F, FloatField
from django.db.models.functions import Cast
from django.shortcuts import redirect
@user_passes_test(is_superadmin)
def completed_orders(request):
    try:
        orders = Order_Product.objects.exclude(status="New").annotate(
        total_price=Cast(F('quantity'), FloatField()) * Cast(F('product__price'), FloatField())
            ).order_by('-id')
        if request.method == 'POST':
            keyword = request.POST.get('keyword', '')
            if keyword!="":
                orders = orders.filter(
                    Q(product__product_name__icontains=keyword) | Q(order__email__icontains=keyword) | Q(order__first_name__icontains=keyword) |Q(order__last_name__icontains=keyword) |
                    Q(order__address_line_1__icontains=keyword)|
                    Q(order__country__icontains=keyword)|
                    Q(order__state__icontains=keyword)
                )

        count=orders.count()
        paginator = Paginator(orders, 10)
        page = request.GET.get('page')
        paged_orders= paginator.get_page(page)


        context={
            'orders':paged_orders,
            'count':count}

        return render(request,'owner/completed_orders.html',context)
    except Exception as e:
     
        return

@user_passes_test(is_superadmin)
def pending_orders(request):
    try:
        orders = Order_Product.objects.filter(status="New").annotate(
            total_price=Cast(F('quantity'), FloatField()) * Cast(F('product__price'), FloatField())
            ).order_by('-id')
        if request.method == 'POST':
            keyword = request.POST.get('keyword', '')
            if keyword!="":
                orders = orders.filter(
                    Q(product__product_name__icontains=keyword) | Q(order__email__icontains=keyword) | Q(order__first_name__icontains=keyword) |Q(order__last_name__icontains=keyword) |
                    Q(order__address_line_1__icontains=keyword)|
                    Q(order__country__icontains=keyword)|
                    Q(order__state__icontains=keyword)
                )

        for order in orders:
            personalize=Personalization.objects.filter(order=order)
            if len(personalize)>0:
                order.personalize=personalize[0].message

        count=orders.count()
        paginator = Paginator(orders, 10)
        page = request.GET.get('page')
        paged_orders= paginator.get_page(page)

        context={
            'orders':paged_orders,
            'count':count
            }
        return render(request,'owner/pending_orders.html',context)
    except Exception as e:
        
        return

@user_passes_test(is_superadmin)
def accept_product_order(request,order_product_id):
    try:

        
        product=Order_Product.objects.get(id=order_product_id)
       
        product.status="Accepted"
        product.save()
        return redirect('pending_orders')

    except Exception as e:
   
        context={
            'error':str(e)
            }
        return render(request,'owner/pending_orders.html',context)

@user_passes_test(is_superadmin)
def cancel_product_order(request,order_product_id):
    try:
        product=Order_Product.objects.get(id=order_product_id)
        product.status="Cancelled"
        product.save()
        return redirect('pending_orders')
    except Exception as e:
    
        context={
            'error':str(e)
            }
        return render(request,'owner/pending_orders.html',context)
