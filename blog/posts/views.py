from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Post,Comment, Message, UserProfile
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from .forms import CommentForm , MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import PostForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def index(request):
    post = Post.objects.all()
    return render(request, 'index.html', {'post':post})

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user 
            new_comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    show_comment_form = request.user.is_authenticated
    image_url = post.image.url if post.image else None

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form, 'show_comment_form': show_comment_form, 'image_url': image_url})


def my_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtelo de nuevo.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirigir al usuario al inicio de sesión después del registro exitoso
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})


@login_required
def message_list(request):
    unique_senders = Message.objects.filter(sender=request.user).values_list('recipient', flat=True).distinct()
    unique_recipients = Message.objects.filter(recipient=request.user).values_list('sender', flat=True).distinct()
    
    conversations = []
    
    for sender_id in unique_senders:
        sender = User.objects.get(id=sender_id)
        conversation = Message.objects.filter(sender=request.user, recipient=sender) | Message.objects.filter(sender=sender, recipient=request.user)
        conversation = conversation.order_by('timestamp')
        conversations.append({'recipient': sender, 'messages': conversation})
    
    for recipient_id in unique_recipients:
        recipient = User.objects.get(id=recipient_id)
        if recipient not in [conversation['recipient'] for conversation in conversations]:
            conversation = Message.objects.filter(sender=request.user, recipient=recipient) | Message.objects.filter(sender=recipient, recipient=request.user)
            conversation = conversation.order_by('timestamp')
            conversations.append({'recipient': recipient, 'messages': conversation})
    
    return render(request, 'messages/message_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)

    messages_sent_by_user_to_recipient = Message.objects.filter(sender=request.user, recipient=recipient)
    messages_received_by_user_from_recipient = Message.objects.filter(sender=recipient, recipient=request.user)

    all_messages = messages_sent_by_user_to_recipient | messages_received_by_user_from_recipient

    messages = all_messages.order_by('timestamp')
    
    form = MessageForm()  
    
    return render(request, 'messages/conversation_detail.html', {'messages': messages, 'recipient': recipient, 'form': form})

@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            messages.success(request, 'Mensaje enviado exitosamente.')
            return redirect('message_list')  
    else:
        form = MessageForm()
    return render(request, 'send_message_to_user.html', {'form': form, 'recipient': recipient})


@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este post.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'post_update.html', {'form': form})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este post.")
    
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    
    return render(request, 'post_delete.html', {'post': post})



def library(request):
    user_posts = request.user.post_set.all()
    return render(request, 'library.html', {'user_posts': user_posts})



@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este comentario.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'comment_update.html', {'form': form})

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")
    
    if request.method == 'POST':
        post_id = comment.post.id 
        comment.delete()
        return redirect('post_detail', post_id=post_id)
    
    return render(request, 'comment_delete.html', {'comment': comment})



def acerca(request):
    return render(request, 'acerca.html')


@login_required
def profile(request):
    try:
        user_profile = request.user.userprofile 
    except UserProfile.DoesNotExist:
        user_profile = None  

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            if user_profile is None:
                user_profile = form.save(commit=False)
                user_profile.user = request.user
                user_profile.save()
            else:
                form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form})



@login_required
def profile_view(request):
    user_profile = request.user.profile  
    context = {
        'user_profile': user_profile,
    }

    return render(request, 'profile.html', context)


def serve_image(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    image_path = post.image.path

    with open(image_path, 'rb') as image_file:
        return HttpResponse(image_file.read(), content_type='image/jpeg')
    


def serve_profile_image(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)
    if profile.image:
        image_path = profile.image.path
        with open(image_path, 'rb') as image_file:
            return HttpResponse(image_file.read(), content_type='image/jpeg')