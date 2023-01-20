from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from cart.models import Order, OrderItem
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,
                              id=order_id)
    template = render_to_string('payment/payment_done_email.html',
                                {'order': order})
    email = EmailMessage(
        'SHADOK | Dziękujemy za zakupy w naszym sklepie',
        template,
        settings.EMAIL_HOST_USER,
        [order.email],
    )

    email.fail_silently=False
    email.send()

    return render(request,
                  'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,
                              id=order_id)
    template = render_to_string('payment/payment_done_email.html',
                                {'order': order})
    email = EmailMessage(
        'SHADOK | Twoje zamówienie nie powiodło się',
        template,
        settings.EMAIL_HOST_USER,
        [order.email],
    )

    email.fail_silently=False
    email.send()

    return render(request,
                  'payment/canceled.html')


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,
                              id=order_id)

    host = request.get_host()
    cart = Cart(request)

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': order.get_total_cost(),
        'shipping': 8.99,
        'item_name': order.id,
        'invoice': str(order.id),
        'currency_code': 'PLN',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment:canceled')),

    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html',
                  {'order': order,
                   'form': form,
                   'cart': cart, })

