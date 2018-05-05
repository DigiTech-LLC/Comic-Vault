from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.CharField(max_length=300)
    favorite_character = models.CharField(max_length=300)
    comic_type = models.CharField(max_length=300)
    comic_persona = models.CharField(max_length=30)
    profile_picture = models.URLField()
    email = models.EmailField()
    password = models.CharField(max_length=128)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        instance.userprofile.save()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Follow(models.Model):
    id_1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='id_1')
    id_2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='id_2')

    def __str__(self):
        return "%s follows %s" % (self.id_1.first_name, self.id_2.first_name)


class Comic(models.Model):
    series = models.CharField(max_length=200)
    volume = models.IntegerField()
    issue = models.IntegerField()
    writer = models.CharField(max_length=200)
    illustrator = models.CharField(max_length=200)
    colorist = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    cover_art = models.URLField()
    spoiler_free_synopsis = models.CharField(max_length=500)
    full_synopsis = models.CharField(max_length=500)
    characters = models.CharField(max_length=200)
    average_rating = models.IntegerField()

    def __str__(self):
        return "Series: %s Vol: %d Issue: %d" % (self.series, self.volume, self.issue)


class ComicComment(models.Model):
    timestamp = models.DateTimeField()
    user_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    comic_id = models.ForeignKey(Comic, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.user_profile_id.first_name + " " + self.user_profile_id.last_name, self.timestamp)


class Rating(models.Model):
    user_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comic_id = models.ForeignKey(Comic, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return "%s's rating for %s" % (self.user_profile_id, self.comic_id)


class TimelinePost(models.Model):
    timestamp = models.DateTimeField()
    content = models.CharField(max_length=500)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    user_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.user_profile_id.first_name + " " + self.user_profile_id.last_name, self.timestamp)


class TimelineComment(models.Model):
    timestamp = models.DateTimeField()
    user_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    timeline_post_id = models.ForeignKey(TimelinePost, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.user_profile_id.first_name + " " + self.user_profile_id.last_name, self.timestamp)


class GeneralNews(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class NewsfeedItem(models.Model):
    timestamp = models.DateTimeField()
    comic_id = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='comic_id', blank=True)
    general_news_id = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='general_news_id', blank=True)

    def __str__(self):
        return self.timestamp


class NewsfeedComment(models.Model):
    timestamp = models.DateTimeField()
    user_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    newsfeed_item_id = models.ForeignKey(NewsfeedItem, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.user_profile_id.first_name + " " + self.user_profile_id.last_name, self.timestamp)
