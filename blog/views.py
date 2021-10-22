from django.shortcuts import render, get_object_or_404, reverse
# generic for generic views - part of class based views
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm

# Create your views here.


class PostList(generic.ListView):
    # use the Post class as the model
    model = Post
    # get the data from table, filtered by published status, descending order
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        # first get the objects from the table that are published
        queryset = Post.objects.filter(status=1)
        # from this, get the post whose slug matches the slug passed in above
        post = get_object_or_404(queryset, slug=slug)
        # post now contains the info we need
        # get the comments for the post, if they are approved
        comments = post.comments.filter(approved=True).order_by('created_on')
        # liked is whether this user liked the post
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        # render the html template, passing back the context dictionary
        return render(
            request,
            "post_detail.html",
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm(),
            }
        )

    def post(self, request, slug, *args, **kwargs):
        # first get the objects from the table that are published
        queryset = Post.objects.filter(status=1)
        # from this, get the post whose slug matches the slug passed in above
        post = get_object_or_404(queryset, slug=slug)
        # post now contains the info we need
        # get the comments for the post, if they are approved
        comments = post.comments.filter(approved=True).order_by('created_on')
        # liked is whether this user liked the post
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # get the data posted from the form
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # set email and username automatically from logged in user
            # these are passed in as part of the request
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            # call the save method on the form, but don't commit it yet
            comment = comment_form.save(commit=False)
            # assign a post to it, then save it
            comment.post = post
            comment.save()
        else:
            # if form wasn't valid then return an empty form
            comment_form = CommentForm()

        # render the html template, passing back the context dictionary
        return render(
            request,
            "post_detail.html",
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm(),
            }
        )


class PostLike(View):
    def post(self, request, slug):
        # get the post whose slug matches the slug passed in above
        post = get_object_or_404(Post, slug=slug)
        # if the post is liked, remove the like, otherwise add like
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        # reload the page
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
