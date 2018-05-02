from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the ComicVault Homepage. Test upload during host. Testing 1,2,3!!!")


def comicpage(request, id):
    context = {
        'comic_id': id,
    }
    return render(request, 'Vault/comic-page.html', context)

    #return HttpResponse("IT WOROKRS %s." % id)
