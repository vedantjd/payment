
from random import sample
from django.shortcuts import render
from django.http import HttpResponse, request
import razorpay
from .models import Product,Profile
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


def login_attempt(request):
     if request.method=='POST':
         username=request.POST.get('username')
         password=request.POST.get('password')
         user_object=User.objects.filter(username=username).first()
         if user_object is None:
             messages.success(request,"User not found!")
             return redirect('/')
         
         profile_obj=Profile.objects.filter(user=user_object).first()
         
         if not profile_obj.is_verified:
             messages.success(request,"Your email is not verified, check your mail!")
             return redirect('/')
         user=authenticate(username=username,password=password)

         if user is None:
             messages.success(request,"Invalid Credentials")
             return redirect('/')

         login(request,user)
         return redirect('/home')



     return render(request,"login.html")


    


def register_attempt(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:

            if User.objects.filter(username=username).first():
                messages.success(request, 'User is Taken.')
                return redirect('/register')
            if User.objects.filter(email=email).first():
                messages.success(request, 'email is taken.')
                return redirect('/register')

            user_obj=User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token=str(uuid.uuid4())
            profile_obj=Profile.objects.create(user= user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)
    return render(request,'register.html')

def token_send(request):
    return render(request,'token_send.html')


def login_success(request):
    return render(request,'login_success.html')


def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
               messages.success(request,"Your account is already Verified!")
               return redirect('/')
            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request,"Your account has been Verified!")
            return redirect('/login_success')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
    

def error_page(request):
    return render(request,'error.html')



def send_mail_after_registration(email,token):
    subject="Your account needs to be verified"
    message=f'Paste the link the to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from= settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)


def logout_user(request):
    logout(request)
    messages.success(request,"You were Logged out! Please Login Again.")
    return redirect("login_attempt")




# payment integration logic
@login_required(login_url='/')
def home(request):
    if request.method=="POST":
      
        name=request.POST.get("productName")
        amount=int(request.POST.get("amount1")) 
        email=request.POST.get('email')
     
        # creating client and verifying the funct 
        client=razorpay.Client(auth=("rzp_test_7ZsayQMDmFJ9oH","8RZo8RztQczZnlbW5ESQzZh4"))
        # generating payment_id and order
        payment=client.order.create({'amount':amount * 100,'currency':'INR','payment_capture':'1'})
      

        # saving the payment id 
        product=Product(product_name=name,product_price=amount, email=email,payment_id=payment['id'])
        product.save()
        return render(request,"index.html",{'payment':payment})
    return render(request, "index.html")


@csrf_exempt
def success(request):
    if request.method =="POST":
        user_data={}
        sample_data=request.POST
        order_id=""
        for key, value in sample_data.items():
            if key=="razorpay_order_id":
                user_data['razorpay_order_id']= value
                order_id = value
            elif key== 'razorpay_payment_id':
                user_data['razorpay_payment_id']= value
            elif key== 'razorpay_signature':
                user_data['razorpay_signature']=value
        user=Product.objects.filter(payment_id=order_id).first()
        client=razorpay.Client(auth=("rzp_test_7ZsayQMDmFJ9oH","8RZo8RztQczZnlbW5ESQzZh4"))
        check=client.utility.verify_payment_signature(user_data)
      

        if not check:
            return render(request,"error.html")
        user.paid= True
        user.save()
        amount = user.product_price
        message_plain=render_to_string('email.txt')
        message_html=render_to_string('email.html')
        print(sample_data)
        print(amount)
        

        send_mail("Your Transaction of was successfully completed!",message_plain, settings.EMAIL_HOST_USER,
        [user.email],html_message=message_html)


    return render(request,"success.html",{"amount":amount})


def about(request):
    return render(request,"about.html")



def members(request):
    return render(request,"members.html")



def ratings(request):
    return render(request,"ratings.html")
