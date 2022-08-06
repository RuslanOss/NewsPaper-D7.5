from django.urls import path
from .views import (
   PostsList,
   PostDetail,
   PostCreate,
   PostUpdate,
   PostDelete,
   SearchListViews,
   subscribe_to_category,
   unsubscribe_from_category,
   PostTag,
   PostAuthor,
)



urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('posts/', PostsList.as_view(), name='post_list'),
    path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostUpdate.as_view(),name='post_update'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', SearchListViews.as_view(), name='post_search'),
    path('subscribe/category/<int:pk>', subscribe_to_category, name='sub_cat'),
    path('unsubscribe/category/<int:pk>', unsubscribe_from_category, name='unsub_cat'),
    path('tag/<int:pk>', PostTag.as_view(), name='post_tag'),
    path('author/<int:pk>', PostAuthor.as_view(), name='author_name')
]