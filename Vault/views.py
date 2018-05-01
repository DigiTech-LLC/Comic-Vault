from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the ComicVault Homepage. Test upload during host")
