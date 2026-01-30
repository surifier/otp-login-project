from django.shortcuts import render, redirect
from .models import UserOTP
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        otp = str(random.randint(100000, 999999))

        user, created = UserOTP.objects.get_or_create(email=email)
        user.name = name
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # SEND OTP EMAIL (SAFE)
        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp}. It is valid for 5 minutes.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=True,
            )
        except Exception as e:
            print("Email sending failed:", e)

        request.session['email'] = email
        return redirect('verify_otp')

    return render(request, "signup.html")



def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        email = request.session.get('email')

        try:
            user = UserOTP.objects.get(email=email)
            if user.otp == entered_otp:
                user.is_verified = True
                user.otp = None
                user.save()
                return redirect('dashboard')
            else:
                return render(request, "verify_otp.html", {"error": "Invalid OTP"})
        except UserOTP.DoesNotExist:
            return redirect('signup')

    return render(request, "verify_otp.html")

def dashboard(request):
    email = request.session.get('email')
    if not email:
        return redirect('signup')

    user = UserOTP.objects.get(email=email)
    return render(request, "dashboard.html", {"user": user})
