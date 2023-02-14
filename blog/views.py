from django.http import HttpResponseRedirect, JsonResponse, QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms.BlogCreateForm import BlogCreateForm
from .models import Blog, Comment, Like
from .forms.CommentForm import CommentForm


def handle_like_post_request(self):
    blog_id = self.request.POST.get('blog_id')
    blog = Blog.objects.get(id=blog_id)
    user = self.request.user
    user_likes_on_blog = blog.like_set.filter(user=user.id)
    if user_likes_on_blog.count() == 1:
        user_likes_on_blog[0].delete()
    else:
        blog.like_set.create(user=user)


def assign_liked_blogs_to_context(self, context):
    liked_blogs = []
    if self.request.user.is_authenticated:
        liked_blogs = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
    context['liked_blogs'] = liked_blogs


class BaseBlogView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog/blogs.html'
    context_object_name = 'blogs'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        assign_liked_blogs_to_context(self, context)
        return context

    def post(self, request, *args, **kwargs):
        handle_like_post_request(self)
        return HttpResponseRedirect(self.request.path_info)


class BlogView(BaseBlogView):
    def get_queryset(self):
        return Blog.objects.all()


class UserRelatedBlogsView(BaseBlogView):
    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        blog_id = QueryDict(self.request.body)['blog_id']
        blog = Blog.objects.get(id=blog_id)
        blog.delete()
        return JsonResponse({'success': True, 'message': 'Deleted'})


class UserLikedBlogsView(BaseBlogView):
    def get_queryset(self):
        return Blog.objects.filter(like__user=self.request.user.id)


class BlogDetailView(LoginRequiredMixin, generic.FormView):
    template_name = 'blog/blog.html'
    form_class = CommentForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['pk']
        blog = Blog.objects.get(id=post_id)
        context['blog'] = blog
        context['comments'] = Comment.objects.filter(post__id=post_id)
        context['likes'] = blog.like_set.all()
        return context

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        user = self.request.user
        post = Blog.objects.get(id=post_id)
        form_data = form.cleaned_data
        post.comment_set.create(user=user, post=post, content=form_data['content'])
        return super().form_valid(form)


class BlogCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'blog/blog_creation.html'
    form_class = BlogCreateForm
    success_url = '/blog/'

    def form_valid(self, form):
        user = self.request.user
        form_data = form.cleaned_data
        user.blog_set.create(title=form_data['title'], content=form_data['content'])
        return super().form_valid(form)
