from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Post
from .forms import CommentForm



def index(request):
    """ Returns index.html """
    return render(request, 'index.html')


def about(request):
    """ Returns about.html """
    return render(request, 'about.html')


class PostList(generic.ListView):
    """ Displays the PostList views """
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = 'post_list.html'
    paginate_by = 6


class PostDetail(View):
    """ Displays the PostDetail views """

    def get(self, request, slug, *args, **kwargs):
        """
        Render the posts with details according to their unique title
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CreatePost(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for creating a new post if the user is logged in
    """
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'featured_image', 'excerpt']
    success_url = reverse_lazy('home')
    success_message = ('New post successfully created ')

    def form_valid(self, form):
        """
        Sets the logged in user as author field in form
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(SuccessMessageMixin, LoginRequiredMixin,
                 UserPassesTestMixin, UpdateView):
    """
    View for updating/editing a post
    """

    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'featured_image', 'excerpt']
    success_url = reverse_lazy('home')
    success_message = "You have successfully updated the post"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DeletePost(LoginRequiredMixin, UserPassesTestMixin,
                 DeleteView, SuccessMessageMixin):
    """
    View for deleting a post
    """

    model = Post
    template_name = 'confirm_delete_post.html'
    success_url = reverse_lazy('home')
    success_message = "Post successfully deleted"

    def test_func(self):
        """ function to check if the user is the post author """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        """ function to display the message after the post is deleted """
        messages.success(self.request, self.success_message)
        return super(DeletePost, self).delete(request, *args, **kwargs)
