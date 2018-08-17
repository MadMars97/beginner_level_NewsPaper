from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models


class ArticleListView(LoginRequiredMixin,ListView):
    model = models.Article
    template_name = 'article_list.html'
    login_url = 'login' #new from LoginRequiredMixin

class ArticleDetailView(LoginRequiredMixin,DetailView):
    model = models.Article
    template_name = 'article_detail.html'
    login_url = 'login' #new from LoginRequiredMixin

class ArticleUpdateView(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
     model = models.Article
     fields = ['title', 'body', ]
     success_url = reverse_lazy('article_list')
     template_name = 'article_edit.html'
     login_url = 'login' #new from LoginRequiredMixin


    
class ArticleDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login' #new from LoginRequiredMixin


#LoginRequiredMixin should be at the left to make it know we intend to restrict access.
class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = models.Article
    template_name = 'article_new.html'
    fields = ['title','body',]
    login_url = 'login' #new from LoginRequiredMixin

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)