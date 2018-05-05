from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import login, authenticate

from .models import TimelinePost, TimelineComment, Comic, ComicComment, UserProfile, Rating, Follow
from .forms import SignUpForm


def index(request):
    return render(request, 'Vault/home.html')


@login_required
def comicpage(request, id):
    user = request.user
    comic_entry = Comic.objects.filter(id=id).first()
    comic_comment_list = ComicComment.objects.all().filter(comic_id=id)
    user_rating = Rating.objects.filter(user_profile_id=user.userprofile.id, comic_id=id).first()
    context = {
        'comic_id': id,
        'comic_entry': comic_entry,
        'comic_comment_list': comic_comment_list,
        'user_rating': user_rating
    }
    return render(request, 'Vault/comic-page.html', context)


@login_required
def timeline(request):
    user = request.user
    following = Follow.objects.filter(id_1__user=user)
    follow_id_2_list = []
    for follow_entity in following:
        follow_id_2_list.append(follow_entity.id_2)
    timeline_post_list = TimelinePost.objects.all().order_by('-timestamp')
    timeline_comment_list = TimelineComment.objects.all()
    template = loader.get_template('Vault/timeline.html')
    context = {
        'following_list' : follow_id_2_list,
        'timeline_post_list': timeline_post_list,
        'timeline_comment_list': timeline_comment_list
    }
    return HttpResponse(template.render(context, request))


@login_required
def search(request):
    comic_list = Comic.objects.all()
    template = loader.get_template('Vault/search.html')
    context = {
        'comic_list': comic_list
    }
    return HttpResponse(template.render(context, request))


@login_required
def profile(request, id):
    user = request.user
    user_profile = UserProfile.objects.get(id=user.userprofile.id)
    template = loader.get_template('Vault/profile.html')
    context = {
        'user_profile': user_profile,
    }
    return HttpResponse(template.render(context, request))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.userprofile.first_name = form.cleaned_data.get('first_name')
            user.userprofile.last_name = form.cleaned_data.get('last_name')
            user.userprofile.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'Vault/signup.html', {'form': form})
