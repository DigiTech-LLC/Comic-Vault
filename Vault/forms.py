from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TimelinePost, TimelineComment, Comic


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class TimelinePostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Share something on ComicVault', 'rows': '4'}), label='')

    class Meta:
        model = TimelinePost
        fields = ('content', )


class TimelineCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Comment on this post', 'rows': '2'}), label='')

    class Meta:
        model = TimelineComment
        fields = ('content', )
        widgets = {'timeline_post_id': forms.HiddenInput()}


class TimelineVoteForm(forms.ModelForm):
    class Meta:
        model = TimelinePost
        fields = {'id', }
        widgets = {'id': forms.HiddenInput, }

class SearchForm(forms.ModelForm):
	class Meta:
		model = Comic
		fields = {'series', 'volume', 'issue', 'publisher', 'writer', 'illustrator', 'colorist'}
	