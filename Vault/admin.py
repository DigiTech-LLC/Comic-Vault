from django.contrib import admin

from .models import UserProfile, Follow, Comic, TimelinePost, TimelineComment, NewsfeedItem, NewsComment, Rating, GeneralNews, ComicComment


admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Comic)
admin.site.register(TimelinePost)
admin.site.register(TimelineComment)
admin.site.register(NewsfeedItem)
admin.site.register(NewsComment)
admin.site.register(Rating)
admin.site.register(GeneralNews)
admin.site.register(ComicComment)
