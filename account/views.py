from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from cart.models import Order_Product,Order
import requests

@csrf_exempt
def Register(request):
    try:
        if request.method == 'POST':
          
            form = RegistrationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
            # Check if there is already an email associated
                if Account.objects.filter(email=email).exists():
                    messages.error(request, f'{email} is already registered.')
                    return redirect('/register')
                    
                else:
                # Create the user account
                    user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
                # Send activation email
                    current_site = get_current_site(request)
                    mail_subject = 'Please activate your account'
                    message = render_to_string('account/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                    to_email = email
                    send_email = EmailMessage(mail_subject, message, to=[to_email])
                    send_email.content_subtype = 'html'
                    send_email.send()
                    
                    messages.success(request, f'Thank you for registering with us. We have sent you a verification email to your email address {to_email}. Please verify it.')
                    return redirect('/login/')
            else:
            # Form is invalid, display error messages
                messages.error(request, 'Please some Crenditials are incorrect')
        else:
            form = RegistrationForm()
        context = {'form': form}
        return render(request, 'account/register.html', context)
    except Exception as e:
        error=str(e)
       
        messages.error(request,f"{error}")
        return render(request,'account/register.html')






def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
       
        
        if user is not None:
            if Account.objects.filter(email=email, is_superadmin=True).exists():
                auth.login(request, user)
                return redirect('/')
            else:
                auth.login(request, user)
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    # next=/cart/checkout/
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                    return redirect('index')         
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('Login')
    
    return render(request, 'account/login.html')


@login_required(login_url = 'Login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('Login')


def activate(request, uidb64, token):
   
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('Login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')





def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('account/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = 'html'
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('Login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
       
    return render(request, 'account/forget.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('Login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('Login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'account/reset.html')





@login_required(login_url='Login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')










@login_required(login_url='Login')
def order_detail(request, order_id):
    order_detail = Order_Product.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    order_total=subtotal+0.11*subtotal    

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
        'order_total':order_total
    }
    return render(request, 'orders/order_details.html', context)



@login_required(login_url='Login')
def account(request):
    user=request.user
    orders=0
  
    orders = Order.objects.filter(user=user,is_ordered=True).order_by('-created_at')
   
   
    context = {
        'orders': orders,
        
    }

    return render(request, 'account/account.html', context)