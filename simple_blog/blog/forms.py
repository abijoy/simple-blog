
from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from .models import Author, Category, Tag, Post, Feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = '__all__'

	def clean_name(self):
		name = self.cleaned_data['name'].lower()
		if name in ['author', 'admin']:
			raise ValidationError("Author name can't be 'author/admin' ")
		return name

	def clean_email(self):
		return self.cleaned_data['email'].lower()


class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = '__all__'

	def clean_name(self):
		t = self.cleaned_data['name'].lower()
		if t in ('tag', 'add', 'update'):
			raise ValidationError("Tag name can't be {0}".format(t))
		return t

	def clean_slug(self):
		return self.cleaned_data['slug'].lower()


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = '__all__'

	def clean_name(self):
		c = self.cleaned_data['name'].lower()
		if c in ('category', 'add', 'update'):
			raise ValidationError("Category name can't be {0}".format(c))
		return c

	def clean_slug(self):
		return self.cleaned_data['slug'].lower()


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'content', 'author', 'category', 'tags')

	def clean_title(self):
		t = self.cleaned_data['title'].lower()
		if t in ('post', 'add', 'update', 'remove'):
			raise ValidationError("Post title can't be \"{0}\"".format(t))
		return t

	# def clean(self):
	# 	cleaned_data = super(PostForm, self).clean()
	# 	title = cleaned_data.get('title')
	# 	l = len(Post.objects.filter(slug__startswith=slugify(title)))
	# 	if title:
	# 		if l:
	# 			cleaned_data['slug'] = slugify(title) + '-{}'.format(l+5)
	# 		else:
	# 			cleaned_data['slug'] = slugify(title)
	# 	return cleaned_data


class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = '__all__'


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

