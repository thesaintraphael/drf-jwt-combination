from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from .forms import Register

from .serializers import UserSerializer, UserSerializerWithToken

from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


def index(request):
    return render(request, 'index.html')


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


# logs user in --> generates token to the user to access  his/her data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register_user(request):
    data = request.data
    form = Register(request.POST)   # signals.py sets username for user same as user's email
    if form.is_valid():
        form.save()
        email = data['email']
        user = User.objects.get(email=email)

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)

    s = str(form.errors).split('li>')  # removing html tags and access only text data
    return Response({'detail': 'Form error', 'error': s[2][:-3]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile_pk(request, pk):
    if request.user.is_staff or pk == request.user.id:
        try:

            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)

        except:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'detail': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)
