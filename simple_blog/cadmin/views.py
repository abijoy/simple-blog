from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from blog.forms import PostForm
from django.contrib import messages
from django.template.defaultfilters import slugify
from blog.models import Author, Tag, Category, Post
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def post_add(request):
	if request== 'POST':
		f = PostForm(request.POST)
		slug = slugify(request.POST['title'])
		if f.is_valid():
			r = f.save(commit=False)
			r.slug = slug
			l = len(Post.objects.filter(slug__startswith=slug))
			if l:
				slug = slugify(slug + ' ' + str(l))
				r.slug = slug
				r.save()
			else:
				r.save()
			f.save_m2m()
			messages.add_message(request, messages.INFO, 'Post added.')
			print()
			p = Post.objects.get(slug=slug)
			return redirect(reverse('blog:post_detail', args=[p.id, p.slug]))

	else:
		f = PostForm()
	return render(request, 'cadmin/post_add.html', {'form': f})


def post_update(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		f = PostForm(request.POST, instance=post)
		slug = slugify(request.POST['title'])
		if f.is_valid():
			r = f.save(commit=False)
			p = Post.objects.filter(slug__startswith=slug)
			if post not in p:
				if not len(p):
					r.slug = slug
				else:
					r.slug = slug + '-{}'.format(len(p))
			r.save()
			f.save_m2m()
			messages.add_message(request, messages.INFO, 'Post updated.')
			return redirect(reverse('blog:post_detail', kwargs={'pk':post.id, 'post_slug': post.slug}))

	else:
		f = PostForm(instance=post)
	return render(request, 'cadmin/post_update.html', {'form': f, 'post': post})


def home(request):
	return render(request, 'cadmin/admin_page.html')

def login(request, **kwargs):
	if request.user.is_authenticated:
		return redirect('cadmin:home')
	return auth_views.login(request, **kwargs)

def logout(request, **kwargs):
	return auth_views.logout(request, **kwargs)

def register(request):
	if request.method == 'POST':
		f = UserCreationForm(request.POST)
		if f.is_valid():
			f.save()
			messages.success(request, "Account created successfully")
			return redirect('cadmin:register')
	else:
		f = UserCreationForm()
	return render(request, 'cadmin/register.html', {'form': f})
















