from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the ComicVault Homepage. Test upload during host. Testing 1,2,3!!!")


def comicpage(request):
    return HttpResponse("pls work %s." % question_id)
