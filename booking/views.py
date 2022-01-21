
from django.shortcuts import render
# from keyring import set_password
from rest_framework import generics, mixins, authentication, permissions, status
from .models import Users, Movies
from .serializer import UserSerializer, MovieSerializer
from rest_framework.response import Response
from random import randrange
from twilio.rest import Client
from final import settings
from django.contrib.auth.models import User

# Create your views here.

class UserLevel1API(generics.GenericAPIView, mixins.ListModelMixin):
    # queryset = Movies.objects.all()
    # serializer_class = MovieSerializer
    # authentication_classes = [authentication.BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        all_movies = Movies.objects.all()
        serialized_data = MovieSerializer(all_movies, many=True)
        print(serialized_data)
        if serialized_data != None:
            return Response(serialized_data.data)
        data = {"msg":"No movies available right now"}
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        otp = request.data.get("otp")
        if otp is None:
            otp = randrange(1000,9999)
            request.data["otp"] = str(otp)
            serialized_data = UserSerializer(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                client = Client(settings.account_sid, settings.auth_token)

                message = client.messages \
                                .create(
                                    body="Your OTP is : "+str(otp),
                                    from_='+19378836196',
                                    to='+91'+request.data["phone"]
                                )
                return Response("Please verify yourself with the otp recieved")
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_name = request.data.get("user_name")
            if user_name is not None and Users.objects.filter(user_name = user_name).exists():
                user = Users.objects.get(user_name = user_name)
                if user.otp == str(otp):
                    user.verified = True
                    user.otp = "----"
                    
                    user.save()
                    User.objects.create_user(username=user.user_name,password=user.password,is_active = True)
                    return Response({"msg":"OTP Verified Successfully"}, status=status.HTTP_200_OK)
                user.delete()
                return Response({"msg":"OTP mismatched please register again"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg":"Data Insufficient"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        movie_name = request.data.get("movie_name")
        required_seats = request.data.get("seats")
        username = request.data.get("user_name")
        if movie_name is not None and required_seats is not None and username is not None:
            user = Users.objects.get(user_name = username)
            movie = Movies.objects.get(movie_name = movie_name)
            if required_seats > movie.seats:
                return Response('Seats are less than needed seats', status= status.HTTP_400_BAD_REQUEST)
            else:
                client = Client(settings.account_sid, settings.auth_token)

                message = client.messages \
                                .create(
                                    body="Your {} seats for {} movie booked successfully. Thank You for booking with us".format(required_seats,movie_name),
                                    from_='+19378836196',
                                    to='+91'+user.phone
                                )
                
                movie.seats -= required_seats
                movie.save()
                return Response('Seats booked successfully', status=status.HTTP_201_CREATED)
        return Response("unexpected error occured please try again", status=status.HTTP_400_BAD_REQUEST)

class MovieManagerAPI(generics.GenericAPIView, mixins.ListModelMixin):
    
    # queryset = Movies.objects.all()
    # serializer_class = MovieSerializer
    # authentication_classes = [authentication.BaseAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = Users.objects.get(user_name = request.user.username)
        movies = Movies.objects.filter(user_name = user)
        serialized_data = MovieSerializer(movies, many=True)
        if serialized_data is None:
            data = {"msg":"No movies available right now"}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
                
    def post(self, request, *args, **kwargs):
        otp = request.data.get("otp")
        if otp is None:
            otp = randrange(1000,9999)
            request.data["otp"] = str(otp)
            request.data["user_level"] = 2
            serialized_data = UserSerializer(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                client = Client(settings.account_sid, settings.auth_token)
                message = client.messages \
                                .create(
                                    body="Your OTP is : "+str(otp),
                                    from_='+19378836196',
                                    to='+91'+request.data["phone"]
                                )
                return Response("Please verify yourself with the otp recieved")
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_name = request.data.get("user_name")
            if user_name is not None and Users.objects.filter(user_name = user_name).exists():
                user = Users.objects.get(user_name = user_name)
                if user.otp == str(otp):
                    user.verified = True
                    user.otp = "----"
                    user.save()
                    User.objects.create_user(username=user.user_name,password=user.password,is_active = True, is_staff = True)
                    return Response({"msg":"OTP Verified Successfully"}, status=status.HTTP_200_OK)
                user.delete()
                return Response({"msg":"OTP mismatched please register again"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg":"Data Insufficient"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user_name = request.data.get("user_name")
        movie_name = request.data.get("movie_name")
        if user_name is not None and Users.objects.filter(user_name = user_name).exists() and movie_name is not None:
            user = Users.objects.get(user_name = user_name)
            if user.verified == True and user.user_level == 2:
                request.data["user_name"] = user
                serialized_data = MovieSerializer(data=request.data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return Response({"msg":"Movie updated"}, status=status.HTTP_200_OK)
            return Response({"msg":"Unauthorized access"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({"msg":"Data Insufficient"}, status=status.HTTP_400_BAD_REQUEST)