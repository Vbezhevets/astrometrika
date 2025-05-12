from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils import translation
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import activate, get_language
import json

def index(request):
    lang = request.GET.get('lang')
    if lang:
        translation.activate(lang)
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang
    return render(request, 'core/index.html')

def privacy_policy(request):
    return render(request, 'core/privacy-policy.html')

def terms_of_service(request):
    return render(request, 'core/terms-of-service.html')

def notify_admin(full_name, email, birth_date, birth_time, birth_place, focus_area):
    context = {
        'full_name': full_name,
        'email': email,
        'birth_date': birth_date,
        'birth_time': birth_time,
        'birth_place': birth_place,
        'focus_area': focus_area,
    }

    subject = _('New Booking from %(name)s') % {'name': full_name}
    html_message = render_to_string('core/emails/booking_admin.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        html_message=html_message,
        from_email='astrometrika@gmail.com',
        recipient_list=['astrometrika@gmail.com'],
        fail_silently=False,
    )

def notify_user(email, full_name):


    subject = _('Your astrology request was received')
    context = {'full_name': full_name}
    html_message = render_to_string('core/emails/booking_user.html', context)
    plain_message = _('Thank you %(name)s! We have received your astrology request and will contact you shortly.') % {'name': full_name}

    send_mail(
        subject=subject,
        message=plain_message,
        from_email='astrometrika@gmail.com',
        recipient_list=[email],
        html_message=html_message,
        fail_silently=True,
    )



@csrf_exempt
def send_booking_request(request):
    if request.method == 'POST':

        activate(request.LANGUAGE_CODE)

        data = json.loads(request.body)
        full_name = data.get('fullName')
        email = data.get('email')
        birth_date = data.get('birthDate')
        birth_time = data.get('birthTime')
        birth_place = data.get('birthPlace')
        focus_area = data.get('focusArea', 'Not specified')

        notify_admin(full_name, email, birth_date, birth_time, birth_place, focus_area)
        notify_user(email, full_name)

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'invalid request'}, status=400)