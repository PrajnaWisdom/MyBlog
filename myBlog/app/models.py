from django.db import models

# Create your models here.

post_status_choices = ((0, 'publish'), (1, 'auto-draft'), (2, 'inherit'))
comment_status_choices = ((0, 'open'), (1, 'closed'))
post_type_choices = ((0, '原创'), (1, '转载'))

class User(models.Model):
    '''
        用户表
    '''
    login = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    nicename = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=32)
    registered = models.DateTimeField(auto_now_add=True)
    activation_key = models.CharField(max_length=128)
    display_name = models.CharField(max_length=32, unique=True) 

class Terms(models.Model):
    '''
        分类表
    '''
    name = models.CharField(max_length=32, unique=True)
    slug = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey('Terms', on_delete=models.CASCADE)


class Posts(models.Model):
    '''
        文章表
    '''
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    post_data = models.DateTimeField(auto_now=True)
    post_content = models.TextField()
    post_title = models.CharField(max_length=128)
    post_excerpt = models.TextField()
    post_status = models.SmallIntegerField(choices=post_status_choices)
    comment_status = models.SmallIntegerField(choices=comment_status_choices)
    post_modified = models.DateTimeField(auto_now_add=True)
    post_type = models.SmallIntegerField(choices=post_type_choices)
    menu_order = models.SmallIntegerField()
    comment_count = models.IntegerField()
    terms = models.ManyToManyField('Terms')


class Comments(models.Model):
    '''
        评论表
    '''
    comment_post_ID = models.ForeignKey('Posts', on_delete=models.CASCADE)
    comment_author = models.CharField(max_length=32)
    comment_author_email = models.EmailField(max_length=32)
    comment_author_IP = models.CharField(max_length=32)
    comment_date = models.DateTimeField(auto_now=True)
    comment_content = models.TextField()
    comment_approved = models.BooleanField(default=False)
    comment_parent = models.ForeignKey('Comments', on_delete=models.CASCADE)

class Links(models.Model):
    '''
        链接表
    '''
    link_url = models.CharField(max_length=128)
    link_name = models.CharField(max_length=128)
    link_description = models.CharField(max_length=1024)
    link_visible = models.BooleanField(default=True)