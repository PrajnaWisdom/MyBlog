# from django.shortcuts import render
from app import models
from app import serializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from app import pagination

# Create your views here.

class UserViews(APIView):
    def get(self, request, format=None):
        users = models.User.objects.all()
        userSerializer = serializer.UserSerializer(users, many=True)
        return Response(userSerializer.data)
    
    def post(self, request, format=None):
        responData = {"code": 0, "msg": ""}
        request.data['password'] = make_password(request.data['password'])
        userSerializer = serializer.UserSerializer(data=request.data)
        if userSerializer.is_valid():
            userSerializer.save()
            responData['code'] = 0
            responData['msg'] = "添加成功"
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['code'] = -1
        responData['msg'] = "添加失败"
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)


class adminlogin(APIView):
    respData = {"msg": '用户名或密码错误', 'code': -1 }
    def get(self, request, format=None):
        request.session['is_login'] = False
        request.session['adminuser'] = ''
        self.respData['msg'] = '退出登录成功'
        self.respData['code'] = 0
        return Response(self.respData, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        username = request.data['username']
        passwd = request.data['passwd']
        user = models.User.objects.filter(login=username).first()
        if user:
            if check_password(passwd, user.password):
                self.respData['msg'] = '登陆成功'
                self.respData['code'] = 0
                request.session['is_login'] = True
                del user.password
                request.session['adminuser'] = user
                return Response(self.respData, status=status.HTTP_201_CREATED)
        self.respData['msg'] = '用户名或密码错误'
        self.respData['code'] = -1
        return Response(self.respData, status=status.HTTP_400_BAD_REQUEST)

class Posts(APIView):
    def get(self, request, format=None):
        responData = {"code": 0, "msg": "", "count": 0, "data": []}
        posts = models.Posts.objects.all()
        myPagination = pagination.MyPageNumberPagination()
        try:
            page_posts = myPagination.paginate_queryset(queryset=posts, request=request, view=self)
            postsSerializer = serializer.PostsSerializer(data=page_posts, many=True)
            responData['data'] = postsSerializer.data
            responData['count'] = len(page_posts)
            responData['code'] = 0
            responData['msg'] = '成功'
        except NotFound:
            responData['code'] = -1
            responData['msg'] = '已经达到最大页'
        return Response(responData)

    def post(self, request, format=None):
        responData = {"code": 0, "msg": ""}
        request.data['author'] = request.session['adminuser'].id
        posts = serializer.PostsSerializer(data=request.data)
        if posts.is_valid():
            posts.save()
            responData['msg'] = '发布成功'
            responData['code'] = 0
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['msg'] = '发布失败'
        responData['code'] = -1
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)

class PostsDetail(APIView):
    def get_object(self, id):
        try:
            return models.Posts.objects.get(id=id)
        except models.Posts.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        posts = self.get_object(id)
        postsSerializer = serializer.PostsSerializer(posts)
        return Response(postsSerializer.data)
    
    def put(self, request, id, format=None):
        responData = {"code": 0, "msg": ""}
        request.data['author'] = request.session['adminuser'].id
        posts = self.get_object(id)
        postsSerializer = serializer.PostsSerializer(posts, data=request.data)
        if postsSerializer.is_valid():
            postsSerializer.save()
            responData['msg'] = '修改成功'
            responData['code'] = 0
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['msg'] = '修改失败'
        responData['code'] = -1
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        posts = self.get_object(id)
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Terms(APIView):
    def get(self, request, format=None):
        terms = models.Terms.objects.all()
        termsSerializer = serializer.TermsSerializer(terms, many=True)
        return Response(termsSerializer.data)
    
    def post(self, request, format=None):
        responData = {"code": 0, "msg": ""}
        termsSerializer = serializer.TermsSerializer(data=request.data)
        if termsSerializer.is_valid():
            termsSerializer.save()
            responData['msg'] = '添加成功'
            responData['code'] = 0
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['msg'] = '添加失败'
        responData['code'] = -1
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)

class TermsDetail(APIView):
    def get_objects(self, id):
        try:
            return models.Terms.objects.get(id=id)
        except models.Terms.DoesNotExist:
            raise Http404
    
    def put(self, request, id, format=None):
        responData = {"code": 0, "msg": ""}
        terms = self.get_objects(id)
        termsSerializer = serializer.TermsSerializer(terms, data=request.data)
        if termsSerializer.is_valid():
            termsSerializer.save()
            responData['msg'] = '修改成功'
            responData['code'] = 0
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['msg'] = '修改失败'
        responData['code'] = -1
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        terms = self.get_object(id)
        terms.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)