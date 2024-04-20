"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts import views
from django.contrib.auth import views as auth_views
from posts.views import logout_view, register_view, profile, serve_image, serve_profile_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('posts/nuevo/', views.post_create, name='post_create'),
    path('conversation/<int:recipient_id>/', views.conversation_detail, name='conversation_detail'),
    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),
    path('messages/', views.message_list, name='message_list'),
    path('post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('library/', views.library, name='library'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('acerca/', views.acerca, name='acerca'),
    path('perfil/', profile, name='profile'),
    path('serve_image/<int:post_id>/', serve_image, name='serve_image'),
    path('serve_profile_image/<int:user_id>/', serve_profile_image, name='serve_profile_image'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
