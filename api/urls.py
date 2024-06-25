from django.urls import path
from . import views

urlpatterns = [
    path('post/list/',views.GetPostListView.as_view()),
    path('post/create',views.CreatePostView.as_view()),
    path('post/update/<int:pk>/',views.UpdatePostView.as_view()),
    path('post/delete/<int:pk>/',views.DeletePostView.as_view()),
    path('post/<int:pk>/',views.GetPostView.as_view()),
    path('media/covers/<str:name>',views.GetCoverView.as_view()),
    path('tags',views.GetTagView.as_view()),
    path('tag/delete/<int:pk>',views.DeleteTagView.as_view()),
    path('comment/',views.CommentView.as_view()),
    path('comment/delete/<int:pk>/',views.CommentDeleteView.as_view())
]