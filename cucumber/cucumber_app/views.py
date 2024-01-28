from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .forms import PostForm, RegistrationForm, LoginForm, CommentForm, ProfileForm, ChatCreateForm, SearchForm, ProfileEditForm, MessageForm
from .models import Post, Comment, Like, User, Subscribe, Chat, Message
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from pathlib import Path
from django.core.files import File
from django.urls import reverse_lazy


def home(request):
    posts = Post.objects.order_by('-created_at')
    user = request.user
    available_users = User.objects.exclude(id=user.id).exclude(subscribers__subscriber=user)[:3]
    return render(request, 'home.html', {'posts': posts, 'user': user, 'available_users': available_users})


def subs(request):
    subscribed_users = Subscribe.objects.filter(subscriber=request.user).values_list('subscribed_to', flat=True)
    posts = Post.objects.filter(user__in=subscribed_users).order_by('-created_at')
    return render(request, 'subscribed.html', {'posts': posts, 'user': request.user})


def logout_1(request):
    logout(request)
    return redirect('/login')


class RegistrationView(View):
    template_name = 'registration.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, {'form': form})


class LoginPage(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user = True


# reduct PostCreate
class PostCreate(TemplateView):
    template_name = 'post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def post(self, request):
        data = request.POST
        files = request.FILES
        print(data)
        print(files)
        with open('static/images/image.png', 'wb') as file:
            file.write(files['file'].read())
        path = Path('static/images/image.png')
        with path.open(mode='rb') as file:
            user = request.user
            image = File(file, name=file.name)
            post = Post(title=data['title'], text=data['text'], image=image, user=user)
            post.save()
            redirect('/')
        return JsonResponse({'resp': data}, safe=False)


class PostView(TemplateView):
    template_name = 'post.html'
    form = CommentForm

    def get_context_data(self, post_id, **kwargs):
        post = Post.objects.get(id=post_id)
        form = CommentForm()
        current_user = self.request.user.id
        comments = Comment.objects.filter(post=post)
        likes = Like.objects.filter(post=post, user=self.request.user).exists()
        like_count = Like.objects.filter(post=post).count()
        context = {
            'current_user': current_user,
            'post': post,
            'comments': comments,
            'form': form,
            'likes': likes,
            'like_count': like_count,
        }

        return context

    def post(self, request, post_id, **kwargs):
        post = Post.objects.get(id=post_id)
        form = CommentForm(request.POST)
        likes = Like.objects.filter(post=post, user=request.user).exists()

        if 'like' in request.POST:
            if not likes:
                Like.objects.create(post=post, user=request.user)
            else:
                Like.objects.filter(post=post, user=request.user).delete()
            return redirect('post_view', post_id=post.id)
        if form.is_valid():
            Comment.objects.create(user=request.user, post=post, text=form.cleaned_data['text'])
            comments = Comment.objects.filter(post=post)
            likes = Like.objects.filter(post=post, user=self.request.user).exists()
            like_count = Like.objects.filter(post=post).count()

            context = {
                'post': post,
                'comments': comments,
                'form': form,
                'likes': likes,
                'like_count': like_count,
            }
            return render(request, 'post.html', context)

        context = {
            'like': likes
        }
        return render(request, 'post.html', context)


class ProfileView(TemplateView):
    template_name = 'profile_view.html'
    form = ProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs.get('user_id'))
        current_user = self.request.user.id
        posts = Post.objects.filter(user=user)
        sub_count = Subscribe.objects.filter(subscribed_to=user).count()
        post_count = len(posts)
        context['user'] = user
        context['form'] = ProfileForm
        context['current_user'] = current_user
        context['posts'] = posts
        context['subscribed_user'] = User.objects.get(id=user.id)
        context['sub_count'] = sub_count
        context['post_count'] = post_count
        context['is_subscribed'] = Subscribe.objects.filter(subscriber=self.request.user,
                                                            subscribed_to=context['subscribed_user']).exists()
        return context

    def post(self, request, user_id, **kwargs):
        user = self.kwargs.get('user_id')
        subscribed_user = User.objects.get(id=user_id)

        subscription, created = Subscribe.objects.get_or_create(subscriber=request.user, subscribed_to=subscribed_user)

        if not created:
            subscription.delete()

        return redirect(f'/profile_view/{user}/', kwargs={'user_id': user_id})


class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm()
        context['results'] = None
        return context

    def post(self, request, **kwargs):
        form = SearchForm(request.POST)

        if form.is_valid():
            search = form.cleaned_data['search']
            results = User.objects.filter(username=search)
        else:
            results = None

        return render(request, 'search.html', {'form': form, 'results': results})


def profile_edit_view(request, user_id):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(f'/profile_view/{user_id}/')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'profile_edit.html', {'form': form})


class ChatView(TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        chat = Chat.objects.get(room_name=kwargs['room_name'])
        messages = Message.objects.filter(chat=chat)
        form = MessageForm()

        context = super().get_context_data(**kwargs)
        context['chat'] = chat
        context['messages'] = messages
        context['form'] = form
        return context

    def post(self, request, **kwargs):
        chat = Chat.objects.get(room_name=kwargs['room_name'])
        messages = Message.objects.filter(chat=chat)
        form = MessageForm(request.POST)

        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.chat = chat
            new_message.sender = request.user
            new_message.save()
            return redirect('chat_view', room_name=kwargs['room_name'])

        context = {
            'chat': chat,
            'messages': messages,
            'form': form,
        }
        return render(request, self.template_name, context)


class ChatCreate(TemplateView):
    template_name = 'chat_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        other_user_id = kwargs.get('user_id')

        current_user = self.request.user

        other_user = User.objects.get(id=other_user_id)

        context['form'] = ChatCreateForm()
        context['current_user'] = current_user
        context['other_user'] = other_user

        return context

    def post(self, request, user_id, **kwargs):
        form = ChatCreateForm(request.POST)

        if form.is_valid():
            current_user = request.user
            other_user = User.objects.get(id=user_id)
            chat_name = form.cleaned_data['chat_name']
            chat = Chat.objects.create(room_name=chat_name)
            chat.participants.add(current_user, other_user)

            return redirect(f'/chats/{ chat.room_name }', room_name=chat.room_name)

        return render(request, self.template_name, {'form': form})


class ChatListView(TemplateView):
    template_name = 'chat_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_chats = Chat.objects.filter(participants=self.request.user)
        context['user_chats'] = user_chats
        return context
