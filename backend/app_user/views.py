from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone

from .models import User, Profile, LimitAction, RequestUpgrate
from .serializers import UserRegisterSerializers, ProfileSerializers, LimitActionSerializers, RequestUpgrateSerializers
from manage_file.function import check_validate

# Create your views here.


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        username_email = request.data.get('username_email')
        password = request.data.get('password')

        user = None
        try:
            user = User.objects.get(username=username_email)
            username = username_email
        except:
            try:
                user = User.objects.get(email=username_email)
                username = user.username
            except:
                return Response("Username or Email don't exist", status=400)

        if not user.check_password(password):
            return Response("Password incorect", status=400)

        refresh = TokenObtainPairSerializer.get_token(user)
        user.last_login = timezone.now()
        user.save()
        response = {
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return Response(response, status=200)


@permission_classes([permissions.IsAuthenticated])
class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(Response("All refresh tokens blacklisted"), status=200)
        refresh_token = self.request.data.get('refresh_token')
        try:
            token = RefreshToken(token=refresh_token)
            token.blacklist()
        except:
            return Response("Token is blacklisted", status=400)
        return Response("Logout successful", status=200)


@permission_classes([permissions.IsAuthenticated])
class MyProfileView(APIView):
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializers(profile)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)

    def put(self, request):
        fullname = request.data.get('fullname')
        avatar = request.FILES.get('avatar')

        profile = Profile.objects.get(user=request.user)
        if fullname:
            if check_validate(fullname):
                return Response("Enter a valid fullname", status=400)
            profile.fullname = fullname
        if avatar:
            profile.avatar = avatar
        profile.save()

        serializer = ProfileSerializers(profile)
        return Response(serializer.data, status=200)

    def patch(self, request):
        try:
            RequestUpgrate.objects.get(user=request.user, status='0')
            return Response("Request already exist", status=400)
        except:
            RequestUpgrate.objects.create(user=request.user)
            return Response("Request sended", status=200)


@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def ProfileView(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializers(profile)
    return Response(serializer.data, status=200)


@permission_classes([permissions.IsAuthenticated])
class RequestView(APIView):
    def get(self, request):
        requests = RequestUpgrate.objects.all()
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(requests, request)
        serializer = RequestUpgrateSerializers(page, many=True)
        return Response(serializer.data, status=200)

    def patch(self, request, id):
        r = RequestUpgrate.objects.get(id=id)
        profile = Profile.objects.get(user=r.user)
        my_profile = Profile.objects.get(user=request.user)

        if my_profile.type != '0':
            return Response("You don't have permission", status=400)

        if profile.type != '1':
            return Response("This user was prenium", status=400)

        if r.status == '0':
            r.status = '1'
            profile.type = '2'
            profile.store += 10000
            profile.limit_upload += 10
            profile.limit_download += 10
            r.save()
            profile.save()
            return Response("Upgrate successful", status=200)
        return Response("Request out of date", status=400)

    def delete(self, request, id):
        r = RequestUpgrate.objects.get(id=id)
        my_profile = Profile.objects.get(user=request.user)

        if my_profile.type != '0':
            return Response("You don't have permission", status=400)

        if r.status == '0':
            r.status = '2'
            r.save()
            return Response("Rejected", status=200)
        return Response("Request out of date", status=400)


@permission_classes([permissions.IsAuthenticated])
class LimitView(APIView):
    def get(self, request):
        limit = LimitAction.objects.get(user=request.user)
        serializer = LimitActionSerializers(limit)
        return Response(serializer.data, status=200)

    def delete(self, request):
        limit = LimitAction.objects.get(user=request.user)
        limit.upload = 0
        limit.download = 0
        limit.save()
        return Response("Reset successful", status=200)


class EmailView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        try:
            User.objects.get(email=email + '@gmail.com')
            return Response("Email đã tồn tại", status=400)
        except:
            if check_validate(email):
                return Response("Email không hợp lệ", status=400)
            return Response("Email hợp lệ", status=200)
            