from django.views.generic import ListView, DetailView, View, TemplateView, FormView
from django.shortcuts import render
from slowveld_old.transactions.models import SaleOrder
from .models import Blog
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageListView(ListView):
    model = SaleOrder
    template_name = 'home/home_page_list_view.html'


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog/blog_list_view.html'

    def get_context_data(self, **kwargs):
        '''
        Blog is filtered into 2 sections - Wildlife and Coding
        '''
        context = super().get_context_data(**kwargs)
        context["posts_wildlife"] = Blog.objects.filter(category__category="Wildlife")
        context["posts_coding"] = Blog.objects.filter(category__category="Coding") 
        return context


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_detail_view.html'
    context_object_name = "post"
    