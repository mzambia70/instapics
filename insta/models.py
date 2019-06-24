from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Profile(models.Model):
    main_user = models.ForeignKey(User, on_delete = models.CASCADE)
    bio = models.TextField(max_length = 300, blank = True, default = '')
    profile_pic = models.ImageField(upload_to = 'images/', null =True, blank = True, default = '')
    followers = models.CharField(max_length = 30, blank = True, default = 0)
    following = models.CharField(max_length = 30, blank = True, default = 0)

    def __str__(self):
        return self.main_user.username

    def save_profile(self):
        self.save()

    def delete_profile(profile_id):
        Profile.objects.filter(id = profile_id).delete()

    def update_profile(profile_id, xbio):
        Profile.objects.filter(id = profile_id).update(bio = xbio)

    @classmethod
    def search_users(cls,name):
        users=cls.objects.filter(main_user__username__icontains=name)
        return users

    @classmethod
    def get_profile(cls,user):
        profile=cls.objects.get(main_user=user)
        return profile

class Comment(models.Model):
    picture = models.CharField(max_length = 30, default = '')
    comment = models.TextField(max_length = 30)
    main_user = models.ForeignKey(User,on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Like(models.Model):
    picture = models.CharField(max_length = 30, default = '')
    main_user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.main_user.username

class Image(models.Model):
    image_path = models.ImageField(upload_to = 'images/')
    main_user = models.ForeignKey(User, on_delete = models.CASCADE)
    caption = models.TextField(blank = True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    likes = models.CharField(max_length = 30, blank = True, default = 0)
    comments = models.CharField(max_length = 30, blank = True, default = 0)

    def __str__(self):
        return self.caption

    def save_image(self):
        self.save()

    def delete_image(image_id):
        Image.objects.filter(id = image_id).delete()

    def update_image(image_id, xcaption):
        Image.objects.filter(id = image_id).update(caption = xcaption)

    def get_image_by_id(image_id):
        image = Image.objects.get(pk = image_id)
        return image

    @classmethod
    def search_image(cls, search_category):
        images = cls.objects.filter(category__category_name__icontains=search_category)
        return images

class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to )