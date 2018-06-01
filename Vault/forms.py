from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TimelinePost, TimelineComment, UserProfile, Comic, ComicComment, Rating, Follow, NewsComment


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class TimelinePostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Share something on ComicVault', 'rows': '4'}), label='')

    class Meta:
        model = TimelinePost
        fields = ('content',)


class TimelineCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Comment on this post', 'rows': '2'}),
                              label='')

    class Meta:
        model = TimelineComment
        fields = ('content',)
        widgets = {'timeline_post_id': forms.HiddenInput()}


class TimelineVoteForm(forms.ModelForm):
    class Meta:
        model = TimelinePost
        fields = {'id', }
        widgets = {'id': forms.HiddenInput, }


class SearchForm(forms.ModelForm):
    series = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Series'}),
        required=False)
    volume = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Volume'}),
        required=False)
    issue = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Issue'}),
        required=False)
    publisher = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Publisher'}),
        required=False)
    writer = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Writer'}),
        required=False)
    illustrator = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Illustrator'}),
        required=False)
    colorist = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Colorist'}),
        required=False)

    class Meta:
        model = Comic
        fields = {'series', 'volume', 'issue', 'publisher', 'writer', 'illustrator', 'colorist'}

class UserSearchForm(forms.ModelForm):
	first_name = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        required=False)
	last_name = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        required=False)

	class Meta:
		model = UserProfile
		fields = {'first_name', 'last_name'}

class BioForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your bio...', 'rows': '4'}), label='')

    class Meta:
        model = UserProfile
        fields = ('bio',)


class FavCharForm(forms.ModelForm):
    favorite_character = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your favorite comic book character...', 'rows': '2'}),
        label='')

    class Meta:
        model = UserProfile
        fields = ('favorite_character',)


class ComicTypeForm(forms.ModelForm):
    comic_type = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your comic type preference...', 'rows': '2'}), label='')

    class Meta:
        model = UserProfile
        fields = ('comic_type',)


class ComicPersonaForm(forms.ModelForm):
    comic_persona = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your comic persona...', 'rows': '1'}), label='')

    class Meta:
        model = UserProfile
        fields = ('comic_persona',)


class ProfilePictureForm(forms.ModelForm):
    profile_picture = forms.URLField(
        widget=forms.Textarea(attrs={'placeholder': 'Upload Profile Picture', 'rows': '4'}), label='')

    class Meta:
        model = UserProfile
        fields = ('profile_picture',)


class ComicCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your comment here', 'rows': '4'}), label='')

    class Meta:
        model = ComicComment
        fields = ('content',)


class ComicRatingForm(forms.Form):
    # (value, name in box)
    CHOICES = ((-1, "-"), (5, '5 (Excellent)',), (4, '4 (Good)',), (3, '3 (Average)',), (2, '2 (Bad)',), (1, '1 (Poor)',), )
    select = forms.CharField(widget=forms.Select(choices=CHOICES), label='')

    class Meta:
        model = Rating
        fields = ('rating',)


class FollowForm(forms.ModelForm):

    class Meta:
        model = Follow
        fields = ('id',)



class NewsItemCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add comment here', 'rows': '4'}), label='')

    class Meta:
        model = NewsComment
        fields = ('content',)
