from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
# Create your models here.


class Author(models.Model):
	name = models.CharField(max_length=50, unique=True, verbose_name='Author Name')
	# slug = models.SlugField(max_length=100, default='author_slug', unique=False)
	email = models.EmailField(unique=True, verbose_name='Author Email')
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(auto_now_add=True)
	last_logged_in = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name + ' : ' + self.email

	def get_absolute_url(self):
		# return '/author/{0}/'.format(self.name)
		return reverse('blog:posts_by_author', args=[self.name])


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		# return '/category/{0}/'.format(self.slug)
		return reverse('blog:posts_by_category', args=[self.slug])

	class Meta:
		verbose_name_plural = 'Categories'


class Tag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		# return '/tag/{0}/'.format(self.slug)
		return reverse('blog:posts_by_tag', args=[self.slug])


class Post(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True, help_text='Slug field will be generated automatically from the title of the post')
	content = models.TextField()
	pub_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.title

	# def save(self, *args, **kwargs):
	# 	self.slug = slugify(self.title)
	# 	super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		# return '/post/{0}/'.format(self.id)
		return reverse('blog:post_detail', args=[self.id, self.slug,])


class Feedback(models.Model):
	name = models.CharField(max_length=200, help_text='Name of the sender')
	email = models.EmailField(max_length=200)
	subject = models.CharField(max_length=200)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name + ' -> ' + self.email





