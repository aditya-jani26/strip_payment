import re
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

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
                reg_errors.append({'username': ["1)Username must be 5-20 characters long",
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
# now here i want to implement ---cronjob--- and ---coustome token--- method also include ---paymentgateway----


# =================================================================================================
