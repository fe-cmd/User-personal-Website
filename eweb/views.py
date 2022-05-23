# Python SDK: https://github.com/sendinblue/APIv3-python-library
from __future__ import print_function
import requests
import json
from lib2to3.pgen2 import token
from sqlite3 import connect
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views import View
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import get_connection
from django.core import mail
from django.urls import reverse
import time
#import sib_api_v3_sdk
#from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError, force_str
from .utils import token_generator
from validate_email import validate_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import smtplib



# create an instance of the API class
#api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
""""subject = "ACTIVATE YOUR ACCOUNT!!!"
sender = {"name":"Engineer","email":"oluferonmijoshua@gmail.com"}
replyTo = {"name":"Whiteboy","email":"niwem77827@dmosoft.com"}
html_content = "<html><body><h1>Please kindly follow intructions to activate your</h1></body></html>"
to = [{"email":"whitetech60@gmail.com","name":"Jane Doe"}]
params = {"parameter":"My param value","subject":"New Subject"}
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=replyTo, params=params, html_content=html_content, sender=sender, subject=subject)

try:
    api_response = api_instance.send_transac_email(send_smtp_email)
    print(api_response)
except ApiException as e:
    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
# Create your views here.
    
"""""

def home(request):
    send_mail('ACTIVATE YOUR ACCOUNT!!!',
    'Hello there!',
    'oluferonmijoshua@gmail.com',
    ['whitetech60@gmail.com'],
    
    )
    return render(request, 'authentication/login.html')

def index(request):
    return render(request, 'index.html')

def tech(request):
    return render(request, 'tech.html')

def about(request):
    return render(request, 'about.html')

def product(request):
    return render(request, 'product.html')

def contact(request):
    return render(request, 'contact.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        context = {
            'fieldValues' : request.POST
        }

        if password == password2:
          if (len(password) and len(password2)) > 6:
            if User.objects.filter(email=email).exists():
               messages.info(request, 'Email already exist!')
               return redirect('signup')
            elif User.objects.filter(username=username).exists():
               messages.info(request, 'Username already exist!')
               return redirect('signup')

            else:
               connection = mail.get_connection()
               # Manually open the connection
               connection.open()
               user = User.objects.create_user(email=email, username=username, password=password)
               user.set_password(password)
               user.is_active = False
               user.save()
            # path_to_view
               # - getting domain we are on
               # - relative url to verification
               # - encode userid
               # - token

               uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

               domain = get_current_site(request).domain
               link = reverse('activate', kwargs={
                   'uidb64':uidb64, 'token': token_generator.make_token(user)})

               activate_url = 'http://'+domain+link    

               email_subject = 'ACTIVATE YOUR ACCOUNT!!!'
               email_body = 'Hi' +user.username+ \
               'please use this link to verify your account\n' +activate_url

               email = mail.EmailMessage(
                  email_subject,
                  email_body,
                  'oluferonmijoshua@gmail.com',
                  [email, 'oluferonmijoshua@gmail.com'],
                  connection=connection
               )

               email.send()
               messages.success(request, 'Account Successfully Created, \
               kindly check your email to activate your account')
               connection.close()
               return redirect('login')
          else:
              messages.error(request, 'Password too short!')
              return render(request, 'authentication/signup.html')
         
        
        else:
           messages.info(request, 'Password does not correspond!')

    else:
        messages.error( request, 'form needs to be filled up')
        return render(request, 'authentication/signup.html')

class VerificationView(View):
    def get(self,request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as ex:
            pass

        return redirect('login')

class LoginView(View):
    def get(self,request):
        return render(request, 'authentication/login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
          auth.login(request, user)
          messages.success(request, 'you are now logged in')
          return redirect('index')
        else:
            messages.info(request, 'Invalid credentials!!!')
            return redirect('login')
    else:
      messages.error( request, 'form needs to be filled up')
      return render(request, 'authentication/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'you are now logged out')
    return redirect('login')

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric symbols'}, status=400)
        if User.objects.filter( username = username ).exists():
            return JsonResponse({'username_error': 'sorry username is in use,choose another one'}, status=400)
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status=400)
        if User.objects.filter( email = email ).exists():
            return JsonResponse({'email_error': 'sorry email is in use,choose another one'}, status=400)
        return JsonResponse({'email_valid': True})




class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request, 'authentication/password_reset_form.html')

    def post(self,request):

        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'please supply a valid email')
            return render(request, 'authentication/password_reset_form.html')

        user = User.objects.filter(email=email)

        domain = get_current_site(request).domain
        uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))

       
        if user.exists():
            connection = mail.get_connection()
               # Manually open the connection
            connection.open()

            link = reverse('reset_user_password', kwargs={
                'uidb64':uidb64, 'token': PasswordResetTokenGenerator().make_token(user[0])})

            reset_url = 'http://'+domain+link 

            email_subject = 'Password reset Instruction'
            email_body = 'Hi there' \
            'please click the link below to reset your password \n' + reset_url

            email = mail.EmailMessage(
            email_subject,
            email_body,
            'oluferonmijoshua@gmail.com',
            [email,'oluferonmijoshua@gmail.com'],
            connection=connection
         )

            email.send()
            connection.close()
            messages.success(request, 'We have sent an email to you for your resseting password')
            return render(request, 'authentication/password_reset_form.html')



class CompletePasswordReset(View):
    def get(self,request,uidb64,token):

        context = {
            'uidb64':uidb64,
            'token': token
        }

        #code to prevent the user from using the same link to reset password
        try:
             user_id = force_str(urlsafe_base64_decode(uidb64))
             user = User.objects.get(pk=user_id)
             
             if not PasswordResetTokenGenerator().check_token(user, token):
                 messages.info(request, 'Password link is invalid, please request a new one')
                 return render(request, 'authentication/password_reset_form.html')

        except Exception as identifier:
            pass

        return render(request, 'authentication/set-new-password.html', context)

    def post(self,request,uidb64,token):

         context = {
            'uidb64':uidb64,
            'token': token,
            'has_error':False
        }

         password = request.POST.get('password', False)
         password2 = request.POST.get('password2', False)

         if password != password2:
             messages.error(request, 'Password does not correspond')
             context['has_error']=True
             return render(request, 'authentication/set-new-password.html', context)
        
         if len(password) < 6:
             messages.error(request, 'Password too short')
             context['has_error']=True
             return render(request, 'authentication/set-new-password.html', context)

         if  context['has_error'] == True:
             return render(request, 'authentication/set-new-password.html', context)


         try:
             user_id = force_str(urlsafe_base64_decode(uidb64))
             user = User.objects.get(pk=user_id)
             user.set_password(password)
             user.save()

             messages.success(request, 'Password reset successful, you can login now with your new password')
             return redirect('login')
         except DjangoUnicodeDecodeError as identifier:
             messages.info(request, 'Something went wrong, kindly try again')
             return render(request, 'authentication/set-new-password.html', context)

         #return render(request, 'authentication/set-new-password.html', context)

    