
from django.shortcuts import render,redirect # type: ignore
from django.http import HttpResponse # type: ignore
from .forms import UserRegistrationForm,LoginForm,IdentifyUser
from django.core.mail import send_mail # type: ignore
from urllib.parse import quote, unquote
from django.contrib.auth import authenticate, login # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import logout,login, authenticate # type: ignore
from django.contrib import messages # type: ignore
from .models import User
from django.utils.encoding import force_bytes,force_str # type: ignore
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode # type: ignore
import datetime
from .utils import get_otp,enc_uname,dec_uname
from django.utils import timezone # type: ignore
from django.contrib.auth.forms import SetPasswordForm # type: ignore
from book.models import Book
from django.urls import reverse # type: ignore


# Create your views here.


def register(request):
    if request.method=='POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            send_mail(
                'Welcome to Movie Ticket Booking',
                f'Hello {fname} {lname},\n\nThank you for registering with us. We are excited to have you on board!\n\nBest regards,\nMovie Ticket Booking Team',
                'pvinu3835@gmail.com',
                [email],
                fail_silently=True
            )
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
            context = {'form': form}
            return render(request, 'accounts/register.html', context)
    else:
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)
    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect(reverse('details'))
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                return render(request, 'accounts/login.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})   
    

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('homeview')

@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/home.html')
    


def identifyview(request):
    if request.method == 'POST':
        form = IdentifyUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists(): 
                user = User.objects.get(username=username)

                otp = get_otp()
                expiry_time = timezone.now() + datetime.timedelta(minutes=1)

                user.otp = otp
                user.otp_expired = expiry_time  # ✅ corrected field name
                user.otp_verified = False        # ✅ reset verified flag
                user.save()

                # Send OTP email
                email = user.email
                send_mail(
                    'OTP Verification',
                    f'Your OTP is {otp}. Enter this OTP to reset your password.',
                    'pvinu3835@gmail.com', 
                    [email],
                    fail_silently=True,
                )

                messages.success(request, 'User found. OTP has been sent to your email.')

                # Encrypt and URL-encode the username
                en_uname = enc_uname(user.username)
                safe_en_uname = quote(en_uname)

                return redirect(f'/accounts/otp/{safe_en_uname}/')
            else:
                messages.error(request, "User not found.")
    else:
        form = IdentifyUser()

    return render(request, 'accounts/identify.html', {'form': form})


def otpview(request, en_uname):
    decoded_en_uname = unquote(en_uname)
    username = dec_uname(decoded_en_uname)

    if not User.objects.filter(username=username).exists():
        messages.error(request, 'Invalid request')
        return redirect('login')

    user = User.objects.get(username=username)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')  # ✅ Safe way to fetch form data
        if not otp_input:
            messages.error(request, 'OTP is required')
            return redirect(request.path)

        if not otp_input.isdigit():
            messages.error(request, 'OTP must be numeric')
            return redirect(request.path)

        otp = int(otp_input)

        if timezone.now() > user.otp_expired:
            messages.error(request, 'OTP expired')
            return redirect('identifyview')

        if user.otp_verified:
            messages.error(request, 'OTP already used')
            return redirect('identifyview')

        if otp == user.otp:
            user.otp_verified = True
            user.save()
            messages.success(request, 'OTP verified successfully')
            return redirect('resetpassword')
        else:
            messages.error(request, 'Invalid OTP')
            return redirect(request.path)

    return render(request, 'accounts/otp.html', {'username': username})

def otpview(request, en_uname):
    decoded_en_uname = unquote(en_uname)

    # Decode username safely
    username = dec_uname(decoded_en_uname)

    # Check if user exists
    if not User.objects.filter(username=username).exists():
        messages.error(request, 'Invalid user.')
        return redirect('identifyview')

    user = User.objects.get(username=username)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')

        if not otp_input:
            messages.error(request, 'OTP is required.')
            return redirect(request.path)

        if not otp_input.isdigit():
            messages.error(request, 'OTP must be numeric.')
            return redirect(request.path)

        otp = int(otp_input)

        if timezone.now() < user.otp_expried:
            messages.error(request, 'OTP has expired.')
            return redirect('identifyview')

        if user.otp_verified:
            messages.error(request, 'OTP already used.')
            return redirect('identifyview')

        if otp == user.otp:
            user.otp_verified = True
            user.save()
            messages.success(request, 'OTP verified successfully.')
            url=f'/accounts/resetpassword/{en_uname}/'
            return redirect(url)
        else:
            messages.error(request, 'Invalid OTP.')
            return redirect(request.path)

    return render(request, 'accounts/otp.html', {'username': username})



def resetpassword(request, en_uname):
    try:
        username = dec_uname(en_uname)
    except Exception:
        messages.error(request, 'Invalid username.')
        return redirect('login')

    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)  

        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('login')
            messages.error(request, 'Please correct the errors below.')

        context = {
            'form': SetPasswordForm(user=user)
        }
        return render(request, 'accounts/resetpassword.html', context)

    messages.error(request, 'Invalid request.')
    return redirect('login')