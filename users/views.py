from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.contrib.auth.hashers import check_password, make_password

from rest_framework.decorators import api_view

from .serializers import UserSerializers,UserSerializersAfterJWT
from .jwtauthentication import generating_jwt_token,decoding_jwt_token
# Create your views here.

# User Registration
@api_view(http_method_names=['POST'])
def register(request):
    if request.method == "POST":
        try:
            data = request.data

            if 'email' not in data:
                return Response(({'message': "Please provide email"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)

            if 'password' in data:
                if not data['password']:  #Cross checking in case of empty string
                    return Response(({'message': "Password is empty"}, 400),
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(({'message': "Please provide password"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)

            if 'username' not in data: 
                return Response(({'message': "Please provide username"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)
            if 'firstname' not in data: 
                return Response(({'message': "Please provide firstname"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)
            if 'lastname' not in data:  
                return Response(({'message': "Please provide lastname"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)
            if 'confirmpassword' not in data: 
                return Response(({'message': "Please provide confirm password"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)
            if data['password'] != data['confirmpassword']:
                return Response(({'message': "Password and confirm password is not equal"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)
            data['email'] = data['email'].strip() #Removing white spaces

            data['password'] = make_password(data['password']) #Encrypting password

            user = User.objects.filter(email__iexact=data['email'])
            if user.exists() == False:
                serialized_data = UserSerializers(data=data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    user = User.objects.get(
                        id=serialized_data.data['id'])

                    payload = {
                        'id': user.id,
                    }
                    token = generating_jwt_token(payload)

                    user_serialized_data = UserSerializersAfterJWT(user).data
    
                    return Response(({'message': 'Successfully registered.',
                        'token': token,
                        'UserDetails': user_serialized_data}), status=status.HTTP_201_CREATED)
            else:
                return Response(({'message': "Email already registered"}),
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(({'message': "User not created! Exception found"}),
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(({'message': "Invalid Request"}), status=status.HTTP_400_BAD_REQUEST)


#User Login
@api_view(http_method_names=['POST'])
def login(request):
    if request.method == "POST":
        try:
            data = request.data
            if 'email' not in data:
                return Response(({'message': "Please provide the email-id"}),
                                status=status.HTTP_400_BAD_REQUEST)

            if 'password' not in data:
                return Response(({'message': "Please provide the password"}),
                                status=status.HTTP_400_BAD_REQUEST)

            data['email'] = data['email'].strip()

            if User.objects.filter(email__iexact=data['email']).exists() == True:
                user = User.objects.get(email__iexact=data['email'])
                if check_password(data['password'], user.password):
                    payload = {
                        'id': user.id,
                    }
                    token = generating_jwt_token(payload)

                    serialized_data = UserSerializersAfterJWT(user).data
                    return Response(({'message': 'Successfully Logged in!',
                        'token': token,
                        'UserDetails': serialized_data}), status=status.HTTP_201_CREATED)
                else:
                    return Response(({
                        'message': 'Login failed',
                    }), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(({
                    'message': 'Email does not exist!',
                }), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(({'message': "Exception found while user login"}),
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(({'message': "Request is Invalid"}), status=status.HTTP_400_BAD_REQUEST)

#Return user if user is successfully authenticated
def isAuthenticated(request):
    try:
        user_id = decoding_jwt_token(
            request.META['HTTP_AUTHORIZATION']
        )['id']
        user = User.objects.get(id=user_id, )
        return user

    except Exception as e:
        return None
