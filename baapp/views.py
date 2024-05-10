from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserSerializerWithToken, BlogSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import Blog
from datetime import datetime


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def userRegister(request):
    data = request.data
    try:
        if data['email'] == '':
            message = {'detail': 'Enter valid email'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        if data['password'] == '' and len(data['password']) < 12:
            message = {
                'detail': 'Enter password & password length should greater than 12'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getBlogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response({'blogs': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postBlog(request):
    user = request.user
    data = request.data

    blog = Blog.objects.create(
        user=user,
        title=data['title'],
        article=data['article'],
        author=data['author']
    )

    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editBlog(request, pk):
    user = request.user
    data = request.data

    blog = Blog.objects.get(uid=pk)

    if user != blog.user:
        return Response({'detail': 'You are not authorized to this blog.'})

    serializer = BlogSerializer(blog, data=data, partial=True)

    if not serializer.is_valid():
        return Response({'detail': 'You are not authorized to this blog.'})

    serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteBlog(request, pk):
    user = request.user
    data = request.data

    blog = Blog.objects.get(uid=pk)

    if user != blog.user:
        return Response({'detail': 'You are not authorized to this blog.'})

    serializer = BlogSerializer(blog, data=data, partial=True)

    if not serializer.is_valid():
        return Response({'detail': 'You are not authorized to this blog.'})

    blog.delete()
    return Response({'detail': 'Blog deleted!'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteAccount(request):
    user = request.user
    serializer = UserSerializer(user, many=False)

    user.delete()
    return Response({'detail': 'Account deleted!'})
