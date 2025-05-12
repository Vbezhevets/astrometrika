from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils import translation
from django.conf import settings
import json

def index(request):
    lang = request.GET.get('lang')
    if lang:
        translation.activate(lang)
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang
    return render(request, 'core/index.html')


def notify_admin(full_name, email, birth_date, birth_time, birth_place, focus_area):
    message = (
        f"New astrology booking:\n\n"
        f"Name: {full_name}\n"
        f"Email: {email}\n"
        f"Birth Date: {birth_date}\n"
        f"Birth Time: {birth_time}\n"
        f"Birth Place: {birth_place}\n"
        f"Focus Area: {focus_area}"
    )
    send_mail(
        subject=f'New Booking from {full_name}',
        message=message,
        from_email='astrometrika@gmail.com',
        recipient_list=['astrometrika@gmail.com'],
        fail_silently=False,
    )

def notify_user(email, full_name):
    message = f"Thank you {full_name}, we received your astrology request!"
    send_mail(
        subject='Your astrology request was received',
        message=message,
        from_email='astrometrika@gmail.com',
        recipient_list=[email],
        fail_silently=True,
    )


@csrf_exempt
def send_booking_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        full_name = data.get('fullName')
        email = data.get('email')
        birth_date = data.get('birthDate')
        birth_time = data.get('birthTime')
        birth_place = data.get('birthPlace')
        focus_area = data.get('focusArea', 'Not specified')

        # Send notifications
        notify_admin(full_name, email, birth_date, birth_time, birth_place, focus_area)
        notify_user(email, full_name)

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'invalid request'}, status=400)