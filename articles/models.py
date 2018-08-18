from django.conf import settings
from django.db import models
from django.urls import reverse



class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)

    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete = models.CASCADE,
        related_name='comments', # new lets us explicitly set the name of this reverse relationship instead
    )
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    

    def __str__(self):
        return self.comment[0:40]

    def get_absolute_url(self):
        return reverse('article_list')


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete = models.CASCADE,
        related_name = 'replies'
    )
    reply = models.CharField(max_length = 140)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)

    def __str__(self):
        return self.reply[0:40]

    def get_absolute_url(self):
        return reverse('article_list')

# if you need to add like button
#and the same for dislike if wanted

class Like(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'autor_likes'
    )
    article = models.ForeignKey(
        Article,
        on_delete = models.CASCADE,
        related_name = 'article_likes'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete = models.CASCADE,
        related_name = 'comment_likes'
    )
    reply = models.ForeignKey(
        Reply,
        on_delete = models.CASCADE,
        related_name = 'reply_likes'
    )

    def __str__(self):
        return '{x} likes \'{y}\''.format(x=self.user.username,y=self.post.text)
