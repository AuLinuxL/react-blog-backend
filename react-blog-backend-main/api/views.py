from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from django.http import HttpResponse
from .serializers import PostSerializer,PostListSerializer,TagSerializer,CommentSerializer
from .models import Post,Tag,Comment
from rest_framework.decorators import api_view
from django.http import HttpResponse,Http404
from django.conf import settings
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os,io
from rest_framework.parsers import MultiPartParser, FormParser
import json
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination

class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'p'

class CreateUserView(generics.CreateAPIView):
    querryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class GetPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        tag_id = self.request.query_params.get('tag',None)
        year = self.request.query_params.get('year',None)
        print(tag_id)
        if tag_id:
            return Post.objects.filter(tags__pk=tag_id)
        elif year:
            return Post.objects.filter(date__year=int(year))
        else:
            return Post.objects.all()

# class GetPostView(generics.RetrieveAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         id = self.kwargs['pk']  # 获取url后的参数
#         return Post.objects.filter(id=id)

class GetPostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        id = self.kwargs['pk']
        return Post.objects.prefetch_related('tags').get(id=id)

class CreatePostView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.dict()  # Make a copy of request data and ensure it is a dict
        tags_data = data.get("tags")
        cover = data.get('cover')
        print(cover)
        
        if tags_data:
            try:
                tags_data = json.loads(tags_data)  # Parse JSON string into Python list
                data['tags'] = tags_data  # Replace JSON string with list of dictionaries
                print("Parsed tags data:", tags_data)
            except json.JSONDecodeError as e:
                return Response({"message": "Invalid tags format.", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if cover == 'null':  # fix cover not set
            data.pop('cover')

        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UpdatePostView(generics.UpdateAPIView):
#     # queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         id = self.kwargs['pk']
#         return Post.objects.filter(id=id)

class UpdatePostView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    # def get_object(self,pk):
    #     return Post.objects.get(pk)

    def put(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        print(post)
        data = request.data.dict()  # Make a copy of request data and ensure it is a dict
        tags_data = data.get("tags")
        
        if tags_data:
            try:
                tags_data = json.loads(tags_data)  # Parse JSON string into Python list
                data['tags'] = tags_data  # Replace JSON string with list of dictionaries
                print("Parsed tags data:", tags_data)
            except json.JSONDecodeError as e:
                return Response({"message": "Invalid tags format.", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PostSerializer(post,data=data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class GetCoverView(View):
    def get(self,request,name):
        file_path = os.path.join(settings.MEDIA_ROOT,"covers",name)
        if os.path.exists(file_path):
            with open(file_path,"rb") as f:
                byte = f.read()
                return HttpResponse(byte,content_type="image/jpeg")
        else:
            raise Http404


class GetTagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

class DeleteTagView(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 获取所有与该标签相关的Post
        related_posts = Post.objects.filter(tags=instance)

        # 解除与该标签的关系
        for post in related_posts:
            post.tags.remove(instance)
        
        # 删除标签
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class CommentView(generics.ListCreateAPIView):
# class CommentView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        post = self.request.query_params.get('id',None)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        if serializer.is_valid:
            serializer.save()
        else:
            print(serializer.errors)

    # def post(self, request, format=None):
    #     print(request.data)
    #     serializer = CommentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         print(serializer.errors)
    #         print('test')
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteView(APIView):
    querryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

# class GetPostView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [AllowAny]

#     def get_object(self):
#         id = self.kwargs['pk']
#         return Post.objects.get(id=id)

    # def get_object(self):
    #     return Tag.objects.all()

