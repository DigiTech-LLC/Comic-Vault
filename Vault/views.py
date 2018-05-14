from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import login, authenticate

from .models import TimelinePost, TimelineComment, Comic, ComicComment, UserProfile, Rating, Follow, NewsfeedItem, GeneralNews, NewsComment
from .forms import SignUpForm, TimelinePostForm, TimelineCommentForm, TimelineVoteForm, BioForm, FavCharForm, ComicTypeForm, ComicPersonaForm, ProfilePictureForm, SearchForm, ComicRatingForm, ComicCommentForm, FollowForm

import datetime

from django.db.models import Avg


def index(request):
    carousel_items = NewsfeedItem.objects.all()
    carousel_news = GeneralNews.objects.all()
    carousel_comic = Comic.objects.all()
    template = loader.get_template('Vault/home.html')
    context = {
        'carousel_items': carousel_items,
        'carousel_news': carousel_news,
        'carousel_comic': carousel_comic
    }
    return HttpResponse(template.render(context, request))


@login_required
def comicpage(request, id):
    if request.method == 'POST':
        comiccommentform = ComicCommentForm
        comicratingform = ComicRatingForm
        if 'ComicComment' in request.POST:
            comiccommentform = ComicCommentForm(request.POST)
            if comiccommentform.is_valid():
                post = comiccommentform.save(commit=False)
                post.content = comiccommentform.cleaned_data.get('content')
                post.timestamp = datetime.datetime.now()
                post.user_profile_id = request.user.userprofile
                post.comic_id = Comic.objects.filter(id=id).first()
                post.save()
                comiccommentform = ComicCommentForm
        elif 'ComicRating' in request.POST:
            comicratingform = ComicRatingForm(request.POST)
            if comicratingform.is_valid():
                post = Rating(user_profile_id_id = request.user.userprofile.id, comic_id_id = id)
                # print(comicratingform.cleaned_data['select'])
                post.rating = comicratingform.cleaned_data['select']
                post.save()
                comicratingform = ComicRatingForm
    else:
        comiccommentform = ComicCommentForm
        comicratingform = ComicRatingForm

    user = request.user
    comic_entry = Comic.objects.filter(id=id).first()
    comic_comment_list = ComicComment.objects.all().filter(comic_id=id).order_by("-timestamp")
    comic_rating_average = Rating.objects.filter(comic_id=id).aggregate(Avg('rating'))
    user_rating = Rating.objects.filter(user_profile_id=user.userprofile.id, comic_id=id).first()

    context = {
        'comic_id': id,
        'comic_entry': comic_entry,
        'comic_comment_list': comic_comment_list,
        'comic_rating_average': comic_rating_average,
        'comiccommentform': comiccommentform,
        'comicratingform': comicratingform,
        'user_rating': user_rating
    }
    return render(request, 'Vault/comic-page.html', context)


@login_required
def timeline(request):
    if request.method == 'POST':
        postform = TimelinePostForm
        commentform = TimelineCommentForm
        voteform = TimelineVoteForm()
        if 'Post' in request.POST:
            postform = TimelinePostForm(request.POST)
            if postform.is_valid():
                post = postform.save(commit=False)
                post.content = postform.cleaned_data.get('content')
                post.timestamp = datetime.datetime.now()
                post.likes = 0
                post.dislikes = 0
                post.user_profile_id = request.user.userprofile
                post.save()
                postform = TimelinePostForm
        elif 'Comment' in request.POST:
            commentform = TimelineCommentForm(request.POST)
            if commentform.is_valid():
                post = commentform.save(commit=False)
                post.content = commentform.cleaned_data.get('content')
                post.timestamp = datetime.datetime.now()
                post.timeline_post_id = TimelinePost.objects.get(id=request.POST['timeline_post_id'])
                post.user_profile_id = request.user.userprofile
                post.save()
                commentform = TimelineCommentForm
        elif 'Like' in request.POST:
            voteform = TimelineVoteForm(request.POST)
            if voteform.is_valid():
                post = TimelinePost.objects.get(id=request.POST['id'])
                post.likes = post.likes + 1
                post.save()
        elif 'Dislike' in request.POST:
            voteform = TimelineVoteForm(request.POST)
            if voteform.is_valid():
                post = TimelinePost.objects.get(id=request.POST['id'])
                post.dislikes = post.dislikes + 1
                post.save()
    else:
        postform = TimelinePostForm()
        commentform = TimelineCommentForm()
        voteform = TimelineVoteForm()

    user = request.user
    following = Follow.objects.filter(id_1__user=user)
    follow_id_2_list = []
    for follow_entity in following:
        follow_id_2_list.append(follow_entity.id_2)
    timeline_post_list = TimelinePost.objects.all().order_by('-timestamp')
    timeline_comment_list = TimelineComment.objects.all()
    context = {
        'following_list': follow_id_2_list,
        'timeline_post_list': timeline_post_list,
        'timeline_comment_list': timeline_comment_list,
        'postform': postform,
        'commentform': commentform,
        'voteform': voteform
    }
    return render(request, 'Vault/timeline.html', context)


@login_required
def search(request):
    comic_list = Comic.objects.all()
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['series']:
                comic_list = comic_list.filter(series__icontains=form.cleaned_data['series'])
            if form.cleaned_data['volume']:
                comic_list = comic_list.filter(volume=form.cleaned_data['volume'])
            if form.cleaned_data['issue']:
                comic_list = comic_list.filter(issue=form.cleaned_data['issue'])
            if form.cleaned_data['publisher']:
                comic_list = comic_list.filter(publisher__icontains=form.cleaned_data['publisher'])
            if form.cleaned_data['writer']:
                comic_list = comic_list.filter(writer__icontains=form.cleaned_data['writer'])
            if form.cleaned_data['illustrator']:
                comic_list = comic_list.filter(illustrator__icontains=form.cleaned_data['illustrator'])
            if form.cleaned_data['colorist']:
                comic_list = comic_list.filter(colorist__icontains=form.cleaned_data['colorist'])
    else:
        form = SearchForm()
    context = {
        'comic_list': comic_list,
        'form': form
    }
    return render(request, 'Vault/search.html', context)


@login_required
def profile(request, id):
    if request.method == 'POST':
        bioform = BioForm
        favcharform = FavCharForm
        comictypeform = ComicTypeForm
        comicpersonaform = ComicPersonaForm
        pictureform = ProfilePictureForm
        followform = FollowForm()

        if 'Bio' in request.POST:
            bioform = BioForm(request.POST)
            if bioform.is_valid():
                post = bioform.save(commit=False)
                post = request.user.userprofile
                post.bio = bioform.cleaned_data.get('bio')
                post.save()
                bioform = BioForm
        elif 'FavChar' in request.POST:
            favcharform = FavCharForm(request.POST)
            if favcharform.is_valid():
                post = favcharform.save(commit=False)
                post = request.user.userprofile
                post.favorite_character = favcharform.cleaned_data.get('favorite_character')
                post.save()
                favcharform = FavCharForm
        elif 'ComicType' in request.POST:
            comictypeform = ComicTypeForm(request.POST)
            if comictypeform.is_valid():
                post = comictypeform.save(commit=False)
                post = request.user.userprofile
                post.comic_type = comictypeform.cleaned_data.get('comic_type')
                post.save()
                comictypeform = ComicTypeForm
        elif 'ComicPersona' in request.POST:
            comicpersonaform = ComicPersonaForm(request.POST)
            if comicpersonaform.is_valid():
                post = comicpersonaform.save(commit=False)
                post = request.user.userprofile
                post.comic_persona = comicpersonaform.cleaned_data.get('comic_persona')
                post.save()
                comicpersonaform = ComicPersonaForm
        elif 'ProfilePic' in request.POST:
            pictureform = ProfilePictureForm(request.POST)
            if pictureform.is_valid():
                post = pictureform.save(commit=False)
                post = request.user.userprofile
                post.profile_picture = pictureform.cleaned_data.get('profile_picture')
                post.save()
                pictureform = ProfilePictureForm
        elif 'Follow' in request.POST:
            followform = FollowForm(request.POST)
            if followform.is_valid():
                follow = Follow(id_1_id = request.user.userprofile.id, id_2_id = id)
                follow.save()
        elif 'Unfollow' in request.POST:
            unfollowform = FollowForm(request.POST)
            if unfollowform.is_valid():
                Follow.objects.filter(id_1_id = request.user.userprofile.id).filter(id_2_id = id).delete()

    else:
        bioform = BioForm()
        favcharform = FavCharForm()
        comictypeform = ComicTypeForm()
        comicpersonaform = ComicPersonaForm()
        pictureform = ProfilePictureForm()
        followform = FollowForm()

    user = request.user
    user_profile = UserProfile.objects.get(id=id)
    logged_in_user = UserProfile.objects.get(id=user.userprofile.id)
    following = Follow.objects.filter(id_1_id=id)
    followers = Follow.objects.filter(id_2_id=id)
    following_count = Follow.objects.filter(id_1_id=id).count()
    follower_count = Follow.objects.filter(id_2_id=id).count()
    checkFollow = Follow.objects.filter(id_1_id=user.userprofile.id).filter(id_2_id=id).count()
    if user_profile.profile_picture == "":
        user_profile.profile_picture = 'http://www.personalbrandingblog.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640-300x300.png'
        user_profile.save()
    context = {
        'user_profile': user_profile,
        'following': following,
        'followers': followers,
        'following_count': following_count,
        'follower_count': follower_count,
        'logged_in_user': logged_in_user,
        'bioform': bioform,
        'favcharform': favcharform,
        'comictypeform': comictypeform,
        'comicpersonaform': comicpersonaform,
        'pictureform': pictureform,
        'followform': followform,
        'checkFollow': checkFollow,

    }
    return render(request, 'Vault/profile.html', context)


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
