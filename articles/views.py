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
    
 
def already_liked_article(author, article_id):

    article= Article.objects.get(id=article_id)
    return Like.objects.filter(author=author, article=article).exists()

def like_button_clicked_article(request, article_id):

    if request.user.is_authenticated():
        article = Article.objects.get(id=article_id)

        if not already_liked_article(request.user, article_id):
            Like.objects.create(author=request.user, article=article)
        else:
            Like.objects.filter(author=request.user, article=article).delete()

        return HttpResponseRedirect(reverse('article_list'))
    else:
        return HttpResponseRedirect(reverse('login'))

def already_liked_comment(author, comment_id):

    comment= Comment.objects.get(id=comment_id)
    return Like.objects.filter(user=author, comment=comment).exists()

def like_button_clicked_comment(request, comment_id):

    if request.user.is_authenticated():
        comment = Comment.objects.get(id=comment_id)

        if not already_liked_comment(request.user, comment_id):
            Like.objects.create(author=request.user, comment=comment)
        else:
            Like.objects.filter(author=request.user, comment=comment).delete()

        return HttpResponseRedirect(reverse('article_list'))
    else:
        return HttpResponseRedirect(reverse('login'))

def already_liked_reply(author, reply_id):

    reply= reply.objects.get(id=reply_id)
    return Like.objects.filter(author=author, reply=reply).exists()

def like_button_clicked_reply(request, reply_id):

    if request.user.is_authenticated():
        reply = Reply.objects.get(id=reply_id)

        if not already_liked_reply(request.user, reply_id):
            Like.objects.create(author=request.user, reply=reply)
            reply['likes']+=1
        else:
            Like.objects.filter(author=request.user, reply=reply).delete()
            reply['likes']-=1

        return HttpResponseRedirect(reverse('article_list'))
    else:
        return HttpResponseRedirect(reverse('login'))


def request_like(request):
    if(request.GET.post('reply_like_btn')):
        like_button_clicked_reply(request,int(request.POST['objectid']))
    elif(request.GET.post('comment_like_btn')):
        like_button_clicked_comment(request,int(request.POST['objectid']))
    elif(request.GET.post('comment_like_btn')):
        like_button_clicked_article(request,int(request.POST['objectid']))
        
