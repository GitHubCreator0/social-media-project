from django import forms
from .models import Post, User, Comment, Message
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class ProfileEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'image']
        widgets = {'image': forms.FileInput()}


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
        widgets = {'image': forms.FileInput(attrs={'id': 'file'}),
                   'title': forms.TextInput(attrs={'id': 'title'}),
                   'text': forms.TextInput(attrs={'id': 'text'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'image', 'bio']


class SearchForm(forms.Form):
    search = forms.CharField(label='', max_length=100,
                            widget=forms.TextInput(attrs={'style': 'width: 300px;'
                                                                   ' border: 1px solid #51414F;'
                                                                        ' border-radius: 5px;'
                                                                        ' background-color: #AA98A9;'}))


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {'content': forms.TextInput(attrs={
                                                     'style': 'width: 980px;'
                                                              'height: 35px;'
                                                 ' border: 1px solid #51414F;'
                                                 ' border-radius: 5px;'
                                                 ' background-color: #AA98A9;'
                                    })
            }


class ChatCreateForm(forms.Form):
    chat_name = forms.CharField(max_length=100, label='Chat Name')

