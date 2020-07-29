from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog-home") 

from .models import Category
choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile')
    website_url = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    whatsapp_url = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("blog-home")


STATUS = (
    (0, "Draft"),
    (1, "Publish"),
    (2, "Featured Post"),
    
)


class Post (models.Model):
    title = models.CharField(max_length=200, unique=True)
    header_image = models.ImageField(null=True, blank=True, upload_to='images/')
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField(blank=True, null=True)
    # content = models.TextField()
    category = models.CharField(max_length=200, choices=choice_list, default='uncategorized')
    snippet = models.CharField(max_length=200)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS,default = 0)
    tags = TaggableManager()
    
    
    class Meta:
        ordering = ['-created_on']
     
        
    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug":str(self.slug)})


class Comment (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)



# Create your models here.
