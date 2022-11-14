from email.message import EmailMessage
from random import choices

from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
import razorpay
from rest_framework.response import Response
from account.models import User
from .models import Feedback, Order
from rest_framework.decorators import api_view, permission_classes
from .serializer import FeedbackSerializer, PaymentSerializer
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from jobportal import settings
from rest_framework.permissions import IsAdminUser, IsAuthenticated


# Create your views here.

@api_view(['POST'])
def payment(request, pk):
    print("hii")
    User=get_user_model()
    dat = User.objects.filter(pk=pk).values()
    for time_period in dat:
        num=time_period['time_period']
    print(num)
    user_det=User.objects.get(pk=pk)
    # print(user_det.time_period)
    print(user_det)
    grand_total = 1000 * num
    if request.method == 'POST':
        # amount = request.POST.get('amount')
        amount = 1000 * num
        name = request.POST.get('name')
        # request.session['key'] = name
        user = user_det
        print(name)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({"amount": int(amount) * 100,
                                       "currency": "INR",
                                       "payment_capture": "1"})
        print(payment)


        order = Order.objects.create(order_amount=amount,
                                     user=user,
                                     order_id=payment['id'])
        payment['name'] = name
        print(order)
        print(order.isPaid,"Hahaha")

    return render(request, 'razorpay/razorpay.html', {'payment': payment, 'grand_total': grand_total})


def payment_status(request):
    status = None
    response = request.POST

    print("ddd", response)

    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    status = client.utility.verify_payment_signature(params_dict)
    print(status, 'ghg')
    try:
        order = Order.objects.get(order_id=response['razorpay_order_id'])
        order.order_payment_id = response['razorpay_order_id']
        order.razorpay_payment_id = response['razorpay_payment_id']

        order.isPaid = True
        # order.order_status = 'Approved'
        order.save()

        name = request.user


        current_site = 'http://localhost:8000'
        mail_subject = "your payment has been successful"
        message = render_to_string('razorpay/success-email.html', {
            'user': request.user,
            'current_site': current_site
        })
        print(message)


        to_email = request.user
        print(to_email)
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=False)
        print(send_mail, 'kkkkkk')

        return render(request, 'razorpay/payment-status.html', {'status': True})
    except:
        return render(request, 'razorpay/payment-status.html', {'status': False})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def success_payments(request):
    order = Order.objects.filter(isPaid=True)
    serializer = PaymentSerializer(order, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def feedback(request, pk):
    data = request.data
    print(data, 'ddddddddddddddddddddddddddddddd')
    user = request.user
    order = Order.objects.get(pk=pk)
    print(order, 'kkkkkkkkkk')
    print(user)
    ispaid = order.isPaid
    print('paid')
    if ispaid == True:
        select = Feedback.objects.create(
            user=user,
            feedback=data['feedback'],
            order=order,

        )
    else:
        return Response('you are not paid')
    serializer = FeedbackSerializer(select)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def display_feedback(request):
    feedback = Feedback.objects.all()
    serializer = FeedbackSerializer(feedback, many=True)
    return Response(serializer.data)






