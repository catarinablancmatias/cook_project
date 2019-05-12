from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import(
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from .models import Post


def home(request):
	context = {
		'posts': Post.objects.all(),
	}

	return render(request, 'blog/home.html', context)


def search(request):
	queryset = Post.objects.all()
	query = request.GET.get('q')
	if query:
		queryset = queryset.filter(
				Q(title__icontains=query) | 
				Q(content__icontains=query)
			).distinct() #icontains é para pesquisar tanto maiusculas como minusculas
		#q = query, informação, etc
		#o distinct é um filter para distinguir valores únicos
	context = {
		'queryset': queryset
	}
	return render(request, 'blog/search_results.html', context)	



class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 4


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		#se o user exister aparece os posts por user, se nao exister aparece um erro 404
		#o username=... esta a tentar e ver o username nos urls
		return Post.objects.filter(author=user).order_by('-date_posted') #menos é para aparecer as publicações do ultimo para o primeiro


class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView): 
#o mixin é para só se puder fazer novas publicações com o login feito
	class Meta:
		model = Post
		fields = ['image']

	model = Post
	fields = ['title', 'content', 'image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
#o user mixin serve para que so o utilizador que fez a publicação a possa atualizar
	class Meta:
		model = Post
		fields = ['image']

	model = Post
	fields = ['title', 'content', 'image']


	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

# serve para que apenas o utilizador que fez a publicação a possa atualizar
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/' 
	#para o sistema saber para onde nos redirecionar caso o user elimine uma publicação

# serve para que apenas o utilizador que fez a publicação a possa eliminar
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



def about(request):
	return render(request, 'blog/about.html', {'title': 'Sobre'})	
