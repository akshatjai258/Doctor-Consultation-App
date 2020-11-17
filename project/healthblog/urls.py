from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView,ArticleDetailView,AddPostView,UpdatePostView,DeletePostView

urlpatterns = [
    path('', HomeView.as_view(),name="BlogHome"),
    path('article/<int:pk>', ArticleDetailView.as_view(),name="BlogDetail"),
    path('add_post/', AddPostView.as_view(),name="AddPost"),
    path('article/edit_post/<int:pk>', UpdatePostView.as_view(),name="UpdatePost"),
    path('article/delete_post/<int:pk>', DeletePostView.as_view(),name="DeletePost"),

]