from django.urls import path
from . import views

urlpatterns = [
    path('user/register/', views.userRegister, name='userregister'),
    path('user/login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('users/', views.getUsers, name='users'),
    path('user/profile/', views.getUserProfile, name='userprofile'),
    path('blogs/', views.getBlogs, name='blogs'),
    path('blog/add/', views.postBlog, name='blogadd'),
    path('blog/edit/<str:pk>', views.editBlog, name='blogedit'),
    path('blog/delete/<str:pk>', views.deleteBlog, name='blogdelete'),
    path('account/delete/', views.deleteAccount, name='accountdelete')
]
