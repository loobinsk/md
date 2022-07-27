from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserRegistrSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validate(request.data), status=status.HTTP_200_OK)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response({'first_name':request.user.first_name})
        except:
            return Response({'error':'Такого пользователя не существует.'}, status=status.HTTP_400_BAD_REQUEST)