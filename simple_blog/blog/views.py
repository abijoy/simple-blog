
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
import datetime
from django import template
from .models import Author, Tag, Post, Category
from django.contrib import messages
from .forms import FeedbackForm, SignUpForm
from django.core.mail import mail_admins
from django_project import helpers
from django.contrib import auth


def index(request):
	return HttpResponse('Hello Django!')

# view function to display a list of all posts
def post_list(request):
	posts = Post.objects.order_by('-id').all()
	posts = helpers.pg_records(request, posts, 10)
	return render(request, 'blog/post_list.html', {'posts': posts})

# view function to diaplay a single post
def post_detail(request, pk, post_slug):

	# post = Post.objects.get(pk=pk)
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

# view function to display posts under a specific Category
def posts_by_category(request, category_slug):
	category = get_object_or_404(Category, slug=category_slug)
	posts = get_list_or_404(Post.objects.order_by('-id'), category=category)
	posts = helpers.pg_records(request, posts, 10)
	context = {
		'category': category,
		'posts': posts,
	}

	return render(request, 'blog/posts_by_category.html', context)

# view function to display posts under a specific Tag
def posts_by_tag(request, tag_slug):
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = get_list_or_404(Post.objects.order_by('-id'), tags=tag)
	posts = helpers.pg_records(request, posts, 10)
	context = {
		'tag': tag,
		'posts': posts,
	}
	
	return render(request, 'blog/posts_by_tag.html', context)

# view function to display posts under a specific Author
def posts_by_author(request, author_slug):
	author = get_object_or_404(Author, name=author_slug)
	posts = get_list_or_404(Post.objects.order_by('-id'), author=author)
	posts = helpers.pg_records(request, posts, 10)
	context = {
		'author': author,
		'posts': posts
	}

	return render(request, 'blog/posts_by_author.html', context)


def test_redirect(request):
	c = Category.objects.get(slug='python')
	return redirect(c, permanent=True)

def feedback(request):
	if request.method == 'POST':
		f = FeedbackForm(request.POST)
		if f.is_valid():
			name = f.cleaned_data['name']
			email = f.cleaned_data['email']
			subject = "You have a new Feedback from {}:{}".format(name, email)
			message = "Subject: {}\n\nMessage: {}\n\n".format(f.cleaned_data['subject'], f.cleaned_data['message'])
			f.save()
			mail_admins(subject, message)
			
			
			messages.add_message(request, messages.INFO, 'Feedback Submitted')
			return redirect('blog:feedback')

	else:
		f = FeedbackForm()
	return render(request, 'blog/feedback.html', {'form': f})


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if f.is_valid():
			f.save()
			messages.add_message(request, messages.INFO, 'Account Created')
			return redirect('blog:signup')
	else:
		form = SignUpForm()
	return render(request, 'blog/signup.html', {'form': form})


def track_user(request):
	response = render(request, 'blog/track_user.html')
	if not request.COOKIES.get('count'):
		response.set_cookie('count', '1', 3600 * 24 * 365 * 2)
	else:
		count = str(int(request.COOKIES.get('count')) + 1)
		response.set_cookie('count', count, 3600 * 24 * 365 * 2)
	return response

def stop_tracking(request):
	if request.COOKIES.get('count'):
		response = HttpResponse('Cookies cleared')
		response.delete_cookie('count')
	else:
		response = HttpResponse('We are no longer tracking you')
	return response

def test_session(request):
	request.session.set_test_cookie()
	return HttpResponse('Testing session cookie')

def test_delete(request):
	if request.session.test_cookie_worked():
		request.session.delete_test_cookie()
		response = HttpResponse('Cookie test passed')
	else:
		response = HttpResponse('Cookie test failed !')
	return response

def save_session_data(request):
	request.session['id'] = 1
	request.session['name'] = 'Bijoy'
	request.session['password'] = 'hotpass'
	return HttpResponse("Session data saved")

def access_session_data(request):
	response = ''

	if request.session.get('id'):
		response += 'Id: {0} <br>'.format(request.session.get('id'))

	if request.session.get('name'):
		response += 'Name: {0} <br>'.format(request.session.get('name'))

	if request.session.get('password'):
		response += 'password: {0} <br>'.format(request.session.get('password'))

	if not response:
		return HttpResponse('No session data')
	else:
		return HttpResponse(response)

def delete_session_data(request):
	try:
		del request.session['id']
		del request.session['name']		
		del request.session['password']
	except KeyError:
		pass

	return HttpResponse("session data cleared")

def lousy_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username == 'root' and password == 'pass':
			request.session['logged_in'] = True
			return redirect('blog:lousy_logged_in')
		else:
			messages.error(request, 'Wrong username/password')
			return redirect('blog:lousy_logged_in')
	else:
		if request.session.get('logged_in'):
			return redirect('blog:lousy_logged_in')
		return render(request, 'blog/lousy_login.html')

def lousy_logged_in(request):
	if not request.session.get('logged_in'):
		return redirect('blog:lousy_login')
	return render(request, 'blog/lousy_logged_in.html')

def lousy_logout(request):
	if request.session['logged_in']:
		request.session['logged_in'] = False
		return render(request, 'blog/lousy_logout.html')
	return redirect('blog:lousy_login')

def login(request):
	if request.user.is_authenticated:
		return redirect('blog:admin_page')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)

		if user:
			auth.login(request, user)
			return redirect('blog:admin_page')
		else:
			messages.error(request, 'Error wrong username/password')
	return render(request, 'blog/login.html')

def admin_page(request):
	if not request.user.is_authenticated:
		return redirect('blog:login')
	return render(request, 'blog/admin_page.html')

def logout(request):
	auth.logout(request)
	return render(request, 'blog/logout.html')




