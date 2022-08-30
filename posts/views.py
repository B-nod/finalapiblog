from django.http import HttpResponse
from turtle import pos, title
from django.shortcuts import render
from rest_framework import generics, permissions, mixins,status
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data=JSONParser().parse(request)
            User = get_user_model()
            user = User.objects.create_user(data['username'],password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=201)
        except IntegrityError:
            return JsonResponse({'error':'Username is already taken, please try another'},status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data=JSONParser().parse(request)
        
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error':'username or password doesnot match'}, status=400)
        else:
            try:
                token=Token.objects.get(user=user)
            except:
                token=Token.objects.create(user=user)
            return JsonResponse({"token":str(token)}, status=200)




@csrf_exempt
@api_view(['POST'])
def send_request(request, userID):
    if request.method == 'POST':
        # import pdb;
        # pdb.set_trace()
        from_user = request.user
        # import pdb;
        # pdb.set_trace()
        to_user = User.objects.get(id=userID)

        from_user = User.objects.get(id = request.user.id)
        # import pdb;
        # pdb.set_trace()
        if from_user != to_user:
            created = Friend_Request.objects.create(from_user = from_user, to_user=to_user)
            if created:
                return HttpResponse('Friend request sent')
            else:
                return HttpResponse('Friend request is already sent')
        else:
            return HttpResponse('Self')

@csrf_exempt
@api_view(['GET'])
def accept_request(request, requestID):
    login_user = request.user
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user.id == login_user.id:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('Friend request accepted.')
    else:
        return HttpResponse('Friend request not accepted')

class PostList(generics.CreateAPIView):
    queryset=Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

@method_decorator(cache_page(10), name='dispatch')
class PostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def get_queryset(self):
        print("Running without cache")
        return Post.objects.filter()

@method_decorator(cache_page(10), name='dispatch')
class EachPostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print("Running without cache")
        return Post.objects.filter(poster=self.request.user)



class PostUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset=Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def put(self,request,*args,**kwargs):
        post=Post.objects.filter(pk=kwargs['pk'],poster=self.request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError('You are not authorize to update this post.')


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self,request,*args,**kwargs):
        post=Post.objects.filter(pk=kwargs['pk'],poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('You are not authorize to delete this post.')

class CommentCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset= Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

@csrf_exempt
@api_view(['GET'])
def approve(request, postID):
    login_user = request.user
    post = Post.objects.get(id=postID)
    if login_user.is_staff == True:
        # import pdb;
        # pdb.set_trace()
        post.approved = True
        post.save()
        return HttpResponse('Aprroved Successful.')
    else:
        return HttpResponse('Aprroved is not successuful..')

