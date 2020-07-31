from django.urls import path
from . import views
from .feeds import LatestPostsFeed, AtomSiteNewsFeed



urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path('', views.index, name = 'kolture'),
    path('about/', views.about, name = 'about'),
    path('home/', views.PostList.as_view(), name='blog-home'),
    path('home/drafts/', views.post_draft_list, name='draft-post'),
    path('home/posts/', views.all_post, name='all-post'),
    path('home/add_post/', views.AddPostView.as_view(), name='add_post'),
    path('home/add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
    path('home/<slug:slug>/', views.PostDetail.as_view(), name='post-detail'),
    path('like/<slug:slug>', views.like_post, name='like_post'),
    path('home/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    # path('home/<slug:slug>/', views.post_detail, name='post_detail'),
    path('home/edit/<slug:slug>/', views.UpdatePostView.as_view(), name='update_post'),
    path('home/<slug:slug>/remove', views.DeletePostView.as_view(), name='delete_post'),
    path('home/category/<str:cats>/', views.CategoryView, name='category'),
    path('categorylist/', views.CategoryListView, name='category-list'),
    path('home/search/results/', views.search, name='search'),
    path('<int:year>/<int:month>/',
         views.ArticleMonthArchiveView.as_view(month_format='%m'),
         name="post_archive_month"),
    

]


