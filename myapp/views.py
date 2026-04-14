from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
# Create your views here.

from django.views.generic import(
    DeleteView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# def home(request):
#     context={
#         'posts':Post.objects.all()
#     }
#     return render(request,'blog/home.html',context)


class PostListView(ListView):
    model = Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-created_at']


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_at')
    
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/posts_detail.html'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    template_name = 'blog/posts_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']
    template_name = 'blog/posts_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url = '/'
    template_name = 'blog/posts_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html',{'title':'About'})


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        Post.objects.create(title=title, content=content)
        return redirect('blog-home')

    return render(request, 'blog/create_post.html')