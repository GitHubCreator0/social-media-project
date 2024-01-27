from . import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('', login_required(views.home), name='home'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('post_create/', login_required(views.PostCreate.as_view()), name='post_create'),
    path('profile_view/<int:user_id>/', views.ProfileView.as_view(), name='profile_view'),
    path('search/', login_required(views.SearchView.as_view()), name='search'),
    path('logout/', views.logout_1, name='logout'),
    path('post/<int:post_id>/', login_required(views.PostView.as_view()), name='post_view'),
    path('edit_profile/<int:user_id>/', login_required(views.profile_edit_view), name='profile_edit'),
    path('chats/<str:room_name>/', views.ChatView.as_view(), name='chat_view'),
    path('create_chat/<int:user_id>/', views.ChatCreate.as_view(), name='chat_create'),
    path('chats/', views.ChatListView.as_view(), name='chat_list_view'),
    path('subs/', views.subs, name='subs')
]
