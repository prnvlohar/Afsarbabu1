import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET_KEY))

def initiate_payment(amount, currency='INR'):
   data = {
       'amount': amount * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
       'currency': currency,
       'payment_capture': '1'  # Auto capture the payment after successful authorization
   }
   response = client.order.create(data=data)
   return response['id']