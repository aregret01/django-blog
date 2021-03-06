from django.db import models
from django.utils import timezone
from django.urls import reverse
# from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager



class PostManager(models.Manager):
    def like_toggle(self, user, post_obj):
        if user in post_obj.liked.all():
            is_liked = False
            post_obj.liked.remove(user)
        else:
            is_liked = True
            post_obj.liked.add(user)
        return is_liked


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # content = models.TextField()
    content = RichTextField(blank = True,null = True)
    liked = models.ManyToManyField(User, blank=True, related_name='liked')
    date_posted = models.DateTimeField(default=timezone.now)
    header_image = models.ImageField(null=True,blank = True,upload_to = "images")
    header_image2 = models.ImageField(null=True,blank = True,upload_to = "images")
    header_image3 = models.ImageField(null=True,blank = True,upload_to = "images")
    # header_image = models.FileField(null=True,blank = True)
    objects = PostManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-date_posted', )

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})




class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return str(self.author)
