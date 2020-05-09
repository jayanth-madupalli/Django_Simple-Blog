from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment
from .forms import CommentPostForm
# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    ordering = ['-date_posted']
    template_name = 'blog/home.html'  # default = <app>/<model>_<view>.html
    context_object_name = 'posts'
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # default = <app>/<model>_<view>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['form'] = CommentPostForm
        context['comments'] = Comment.objects.filter(
            post=self.object).order_by('-date_posted')
        return context

    def post(self, request, **kwargs):
        form = CommentPostForm(request.POST)
        self.object = self.get_object()
        form.instance.post = self.object
        form.instance.author = self.request.user
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your comment is posted successfully.')
        else:
            messages.danger(
                request, f'Failed to post comment.')
        context = super().get_context_data(**kwargs)
        context['form'] = CommentPostForm
        context['comments'] = Comment.objects.filter(
            post=self.object).order_by('-date_posted')
        return self.render_to_response(context=context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
