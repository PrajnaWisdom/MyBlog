from django.shortcuts import render, render_to_response
from app import models
from app import serializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from app import pagination
from rest_framework.exceptions import NotFound
from django.views.generic.base import View
import math

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
        responData = {"code": 0, "msg": "", "pages": 0, "data": []}
        posts = models.Posts.objects.all()
        myPagination = pagination.MyPageNumberPagination()
        try:
            page_posts = myPagination.paginate_queryset(queryset=posts, request=request, view=self)
            postsSerializer = serializer.PostsSerializer(page_posts, many=True)
            responData['data'] = postsSerializer.data
            responData['pages'] = math.ceil(len(posts) / 5)
            responData['code'] = 0
            responData['msg'] = '成功'
        except Exception as e:
            responData['code'] = -1
            responData['msg'] = '没有更多数据了'
        return Response(responData)

    def post(self, request):
        responData = {"code": 0, "msg": ""}
        posts = serializer.PostsSerializer(data=request.data)
        if posts.is_valid():
            posts.save()
            responData['msg'] = '发布成功'
            responData['code'] = 0
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['msg'] = '发布失败'
        responData['code'] = -1
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)

class AddPosts(APIView):
    def get(self, request):
        return render_to_response('admin/addposts.html')

class PostsDetail(APIView):
    def get_object(self, id):
        try:
            return models.Posts.objects.get(id=id)
        except models.Posts.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        posts = self.get_object(id)
        postsSerializer = serializer.PostsSerializer(posts)
        return render_to_response('article.html',postsSerializer.data)
        # Response(postsSerializer.data)
        
    
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
    
class Comments(APIView):
    def get(self, request, format=None):
        comment_post_ID = request.data['post_id']
        comments = models.Comments.objects.filter(comment_post_ID=comment_post_ID)
        myPagination = pagination.MyPageNumberPagination()
        try:
            page_comments = myPagination.paginate_queryset(queryset=comments, request=request, view=self)
            commentsSerializer = serializer.CommentsSerializer(data=page_comments, many=True)
            responData['data'] = commentsSerializer.data
            responData['count'] = len(page_comments)
            responData['code'] = 0
            responData['msg'] = '成功'
        except NotFound:
            responData['code'] = -1
            responData['msg'] = '已经达到最后页'
        return Response(responData)
    
    def post(self, request, format=None):
        responData = {"code": 0, "msg": ""}
        commentSerializer = serializer.CommentsSerializer(data=request.data)
        if commentSerializer.is_valid():
            commentSerializer.save()
            responData['msg'] = '评论成功'
            responData['code'] = 0
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['msg'] = '评论失败'
        responData['code'] = -1
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)

class CommentsDetail(APIView):
    def get_objects(self, id):
        try:
            return models.Comments.objects.get(id=id)
        except models.Comments.DoesNotExist:
            raise Http404 
    
    def put(self, request, id, format=None):
        responData = {"code": 0, "msg": ""}
        comment = self.get_objects(id)
        commentSerializer = serializer.CommentsSerializer(comment, data=request.data)
        if commentSerializer.is_valid():
            commentSerializer.save()
            responData['msg'] = '修改成功'
            responData['code'] = 0
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['msg'] = '修改失败'
        responData['code'] = -1
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        comment = self.get_object(id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class Links(APIView):
    def get(self, request, format=None):
        responData = {"code": 0, "msg": "", "count": 0, "data": []}
        links = models.Links.objects.filter(comment_post_ID=id)
        myPagination = pagination.MyPageNumberPagination()
        try:
            page_links = myPagination.paginate_queryset(queryset=links, request=request, view=self)
            linksSerializer = serializer.LinksSerializer(data=page_links, many=True)
            responData['data'] = linksSerializer.data
            responData['count'] = len(page_links)
            responData['code'] = 0
            responData['msg'] = '成功'
        except NotFound:
            responData['code'] = -1
            responData['msg'] = '已经达到最大页'
        return Response(responData)
    
    def post(self, request, format=None):
        responData = {"code": 0, "msg": ""}
        linkSerializer = serializer.LinksSerializer(data=request.data)
        if linkSerializer.is_valid():
            linkSerializer.save()
            responData['msg'] = '添加成功'
            responData['code'] = 0
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['msg'] = '添加失败'
        responData['code'] = -1
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)
    
class LinksDetail(APIView):
    def get_objects(self, id):
        try:
            return models.Links.objects.get(id=id)
        except models.Links.DoesNotExist:
            raise Http404 
    
    def put(self, request, id, format=None):
        responData = {"code": 0, "msg": ""}
        link = self.get_objects(id)
        linkSerializer = serializer.LinksSerializer(link, data=request.data)
        if linkSerializer.is_valid():
            linkSerializer.save()
            responData['msg'] = '修改成功'
            responData['code'] = 0
            return Response(responData, status=status.HTTP_201_CREATED)
        responData['msg'] = '修改失败'
        responData['code'] = -1
        return Response(responData, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        link = self.get_object(id)
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class index(View):
    def get(self, request):
        return render_to_response('index.html')

class tags(View):
    def get(self, request):
        return render_to_response('tags.html')

class archives(View):
    def get(self, request):
        return render_to_response('archives.html')

class article(View):
    def get(self, request):
        return render_to_response('article.html')

class projects(View):
    def get(self, request):
        return render_to_response('projects.html')

# def index(request):
#     return render_to_response('index.html')

