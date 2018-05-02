from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import TimelinePost, TimelineComment



def index(request):
    return HttpResponse("Hello, world. You're at the ComicVault Homepage. Test upload during host. Testing 1,2,3!!!")


def comicpage(request, id):
    comic_entry_list = Comics.objects.all().filter(id__in=id)
    comic_comment_list = ComicComment.object.all().filter(comic_id=id)
    context = {
        'comic_id': id,
        'comic_entry_list': comic_entry_list
        'comic_comment_list': comic_comment_list
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
