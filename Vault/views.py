from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import TimelinePost, TimelineComment


def index(request):
    return HttpResponse("Hello, world. You're at the ComicVault Homepage. Test upload during host. Testing 1,2,3!!!")


def comicpage(request, id):
    context = {
        'comic_id': id,
    }
    return render(request, 'Vault/comic-page.html', context)

    #return HttpResponse("IT WOROKRS %s." % id)


def timeline(request, id):
    timeline_post_list = TimelinePost.objects.all().filter(user_profile_id=id)
    timeline_comment_list = TimelineComment.objects.all()
    template = loader.get_template('Vault/timeline.html')
    context = {
        'timeline_post_list': timeline_post_list,
        'timeline_comment_list': timeline_comment_list
    }
    return HttpResponse(template.render(context, request))
