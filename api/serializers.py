from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post,Tag,Comment

# Serializer is used to convert other type into python native datatypes that can then be easily rendered into JSON, XML
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']
        extra_kwargs = {'password': {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']
    
        def create(self,validated_data):
            tag = Tag.objects.create(**validated_data)
            return tag

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Post
        # fields = ['id','title','summary','content','date','cover','tags']
        fields = ['id','title','summary','content','date','cover','tags']

    def create(self,validated_data):
        print("Validated data:", validated_data)  # 打印验证后的数据
        tags_data = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            tag,create = Tag.objects.get_or_create(name=tag_data['name'])
            print(create)
            post.tags.add(tag)
        return post

    def update(self,instance,validated_data):
        print("Validated data:", validated_data)  # 打印验证后的数据
        tags_data = validated_data.pop('tags', [])
        instance.title = validated_data.get('title', instance.title)  # 参数：instance.title是获取不到数据的fallback
        instance.summary = validated_data.get('summary', instance.summary)
        instance.content = validated_data.get('content', instance.content)
        instance.cover = validated_data.get('cover', instance.cover)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            print(created)
            instance.tags.add(tag)
        return instance

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','summary','date','cover','tags']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','comment','date','name','site','post']
        extra_kwargs = {"user": {"read_only": True}}

# class PostInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['id','title','summary','date']

# class PostContentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PostContent
#         fields = ['id','content']

#     # def create(self, validated_data):
#     #     content = PostContent.objects.create(**validated_data)
#     #     return content

# class PostCreateSerializer(serializers.ModelSerializer):
#     content = PostContentSerializer()  # 定义嵌套serializer，在处理post的同时处理PostContentSerializer

#     class Meta:
#         model = Post
#         fields = '__all__'

#     def create(self,validated_data):
#         content_data = validated_data.pop('content')
#         post = Post.objects.create(**validated_data)
#         post_content = PostContent.objects.create(post=post,content=content_data['content'])
#         return post
