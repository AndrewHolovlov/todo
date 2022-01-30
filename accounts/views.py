from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

from .serializers import LoginSerializer, SignUpSerializer, UserSerializer
from .models import User


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_id="login",
        request_body=LoginSerializer,
        responses={201: TokenRefreshSerializer, 400: "Bad request"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SignUpView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    @swagger_auto_schema(
        operation_id="sign_up",
        request_body=SignUpSerializer,
        responses={201: TokenRefreshSerializer, 400: "Bad request"},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = User.get_tokens_for_user(user)
            return Response(token, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id="user_list",
        operation_description="Get list of all users except admins",
        responses={200: UserSerializer, 401: "Unauthorized"},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

