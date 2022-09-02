"""post_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from posts import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup', views.signup),
    path('api/login',views.login),
    path('api/sendrequest/<int:userID>/', views.send_request),
    path('api/acceptrequest/<int:requestID>/', views.accept_request),
    path('api/post', views.PostList.as_view()),
    path('api/unapproved', views.PostUnapporved.as_view()),
    path('api/getall', views.PostView.as_view()),
    path('api/get', views.EachPostView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api/post/<int:pk>',views.PostUpdateAPIView.as_view()),
    path('api/post/delete/<int:pk>',views.PostRetrieveDestroy.as_view()),
    path('api/post/<int:pk>/comment', views.CommentCreate.as_view()),
    path('api/approve/<int:postID>/',views.approve),
    path('api/requestlist',views.RequestList.as_view()),
    path('api/sendlist',views.SendList.as_view()),

    path('api/deleterequest/<int:pk>',views.RequestDelete.as_view()),
    path('api/cancelrequest/<int:pk>',views.RequestSelfDecline.as_view()),
    
    # stripe integration
    path('', include('payments.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
