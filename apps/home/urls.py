from django.urls import path
from .views import BlogListView, BlogDetailView, HomePageListView


app_name = 'home'

urlpatterns = [

    # Homepage
    path('', HomePageListView.as_view(),name='home-page-list-view'),

    # Blog
    path('blog/', BlogListView.as_view(),name='blog-list-view'),
    path('blog/<int:pk>', BlogDetailView.as_view(),name='blog-detail-view'),


]