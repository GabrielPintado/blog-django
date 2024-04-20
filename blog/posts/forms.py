from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Comment, Post, UserProfile




class UserProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Imagen de perfil')
    description = forms.CharField(max_length=200, required=False, label='Descripción')
    link = forms.URLField(required=False, label='Enlace')

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'image', 'description', 'link']
class UserCreationWithEmailForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo Electrónico')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': '',  
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','image', 'slug']




class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))