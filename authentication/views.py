from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from .tokens import token_generator
from django.conf import settings
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login, logout


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
import threading
# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email_message):  
        self.email = email_message
        threading.Thread.__init__(self)

    def run(self):
        return self.email.send()


def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = form.save(commit=False)            
            user.is_active = False
            user.save()
            
            current_site = get_current_site(request).domain
            email_subject = 'Activation Link'
            email_body = render_to_string('mail/activate_account.html', {
                                                                            'user':user, 
                                                                            'domain': current_site,
                                                                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                                                            'token':token_generator.make_token(user)
                                                                        })
            email = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, to = [email])

            EmailThread(email).start()
            messages.success(request, 'Please check your email inbox for activate your account...')
            return redirect('register')
        
    context = {'form':form}
    return render(request, 'authentication/register.html', context)


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except:
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('login')

    return render(request, 'mail/activation-failed.html')


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                messages.success(request, 'Success!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid credentials!')
        else:
            messages.error(request, 'Invalid credentials!')
    else:
        form = AuthenticationForm()

    return render(request, 'authentication/login.html', {'form': form})



def logout_user(request):
    logout(request)
    return redirect('/')



def index_view(request):
    return render(request, 'authentication/index.html')