import re
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.shortcuts import render,redirect
import stripe
from rest_framework import status

# Create your views here.
# ===============================--basic--==================================
class RegisterView(APIView):

    def post(self, request):
        user = UserModel.objects.filter(username = request.data['username'])
        # validation 
        if user.exists():
            return Response({'msg': 'Registration already exists'}, status= 404)
        else:
            reg_errors = []
            if not re.match(r'^(?![._])[a-zA-Z0-9_.]{5,20}$', request.data['username']):
                reg_errors.append({'username': [
                "1)Username must be 5-20 characters long",
                                                \
				"2) Username may only contain:", "- Uppercase and lowercase letters", "- Numbers from 0-9 and",\
				"- Special characters _.",
                "3) Username may not:Begin or finish with _ ,."]})
                
            else:
                if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-] +\. [A-Z|a-z] {2,} \b', request.data['email']):
                    pass
                else:
                    reg_errors.append({'email': 'Invalid Email'})
                if re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$", request.data['password']):
                    pass
                else:
                    reg_errors.append({'password': ["at least one digit", "at least one uppercase letter", "at least one lowercase letter", "at least one special character[$@#]"]})
                if len(reg_errors)== 0:
                    serializer = RegistrationSerializer(data= request.data, many= False)
                    if serializer.is_valid():
                        serializer
                        serializer.save()
                        return Response({'msg': 'User has been registered Successfully'}, status= 201)
                    else:
                        return Response(serializer.errors)
                else:
                    return Response({'msg': reg_errors})
            return Response({'msg': reg_errors})

class LoginView(APIView):

    def post(self, request):
        try: 
            user = UserModel.objects.filter(username= request.data['username']).first()
            if check_password(request.data['password'], user.password):
                # user = UserModel.objects.filter(username=request.data['username']).first()
                return Response( status = 201)
            else:
                return Response({'msg': 'Invalid credentials','status':'warning'}, status= 404)
        except Exception as e:
            return Response({'msg': 'You are not registered user!','status':'error'}, status= 404)
# =============================---basic---====================================
# now here i want to implement ---cronjob--- and ---coustome token--- also include ---paymentgateway----
# =================================================================================================

stripe.api_key = 'STRIPE_secretkey'

class WalletInfoAPIView(APIView):

    def get(self, request):
        check, obj = token_auth(self.request)

        if not check:
            return Response({'msg': obj}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            try:
                customer_id = request.user.profile.stripe_customer_id
                customer = stripe.Customer.retrieve(customer_id)
                payment_methods = stripe.PaymentMethod.list(customer=customer_id, type="card")
                transactions = stripe.PaymentIntent.list(customer=customer_id)

                context = {
                    'customer': customer,
                    'payment_methods': payment_methods,
                    'transactions': transactions,
                }

                return render(request, 'wallet_info.html', context)
            except stripe.error.StripeError as e:
                return render(request, 'error.html', {'error_message': str(e)})

class CreatePaymentIntentAPIView(APIView):

    def post(self, request):
        check, obj = token_auth(self.request)

        if not check:
            return Response({'msg': obj}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            amount = int(request.data.get('amount', 0))  # Amount in cents
            currency = 'usd'
            description = 'Example payment'

            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency=currency,
                    description=description,
                    payment_method_types=['card'],
                )

                context = {
                    'client_secret': payment_intent.client_secret,
                    'amount': amount,
                    'currency': currency,
                }

                return render(request, 'payment.html', context)
            except stripe.error.StripeError as e:
                return render(request, 'error.html', {'error_message': str(e)})

class SavePaymentMethodAPIView(APIView):

    def post(self, request):
        check, obj = token_auth(self.request)

        if not check:
            return Response({'msg': obj}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            payment_method_id = request.data.get('payment_method_id')  
            try:
                customer_id = request.user.profile.stripe_customer_id

                # Attach the payment method to the customer
                stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)

                # Set it as the default payment method
                stripe.Customer.modify(
                    customer_id,
                    invoice_settings={'default_payment_method': payment_method_id}
                )
                return redirect('wallet_info')  # Redirect to wallet info page
            except stripe.error.StripeError as e:
                return render(request, 'error.html', {'error_message': str(e)})

def token_auth(request):
    token = request.headers.get('token',None)

    if token is None:
        return False,"please provide a token"
    try:
        user = CustomToken.objects.get(key=token)
        return True,user
    except CustomToken.DoesNotExist:
        return False,"token does not valid"