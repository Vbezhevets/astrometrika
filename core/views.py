from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.conf import settings
from datetime import datetime
import stripe
import json
from .stripe_config import READING_TOPIC_TO_PRICE


def index(request):
    context = {
        'timestamp': datetime.now().timestamp()
    }
    return render(request, 'core/index.html', context)

def privacy_policy(request):
    return render(request, 'core/privacy-policy.html')

def terms_of_service(request):
    return render(request, 'core/terms-of-service.html')

def success_page(request):
    return render(request, 'core/success.html')

def cancel_page(request):
    return render(request, 'core/payment-cancel.html')


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
        from_email='astrometrika@gmail.com',
        recipient_list=['astrometrika@gmail.com'],
        html_message=html_message,
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

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
from .stripe_config import READING_TOPIC_TO_PRICE

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
from .stripe_config import READING_TOPIC_TO_PRICE

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        birth_date = request.POST.get("birth_date")
        birth_time = request.POST.get("birth_time")
        birth_place = request.POST.get("birth_place")
        reading_topic = request.POST.get("readingTopic")
        focus_area = request.POST.get("focus_area", "")

        price_id = READING_TOPIC_TO_PRICE.get(reading_topic)
        if not price_id:
            return JsonResponse({'error': 'Invalid topic'}, status=400)
        if reading_topic not in READING_TOPIC_TO_PRICE:
            return JsonResponse({'error': f'Invalid topic: {reading_topic}'}, status=400)
        try:

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='payment',
                customer_email=email,
                metadata={
                    'full_name': full_name or '',
                    'birth_date': birth_date or '',
                    'birth_time': birth_time or '',
                    'birth_place': birth_place or '',
                    'focus_area': focus_area or '',
                },
                success_url='https://www.astrometrika.com/success/',
                cancel_url='https://www.astrometrika.com/cancel/',
            )
            return JsonResponse({'checkout_url': session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=400)
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        full_name = session['metadata']['full_name']
        email = session['customer_email']
        birth_date = session['metadata']['birth_date']
        birth_time = session['metadata']['birth_time']
        birth_place = session['metadata']['birth_place']
        focus_area = session['metadata']['focus_area']

        notify_admin(full_name, email, birth_date, birth_time, birth_place, focus_area)
        notify_user(email, full_name)

    return HttpResponse(status=200)


def test_mail(request):
    try:
        send_mail(
            'Django Test',
            'Это тестовое письмо от Django.',
            'astrometrika@gmail.com',
            ['astrometrika@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse("✅ Письмо отправлено успешно.")
    except Exception as e:
        return HttpResponse(f"❌ Ошибка: {e}")