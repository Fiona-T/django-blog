from django.shortcuts import render, get_object_or_404
# generic for generic views - part of class based views
from django.views import generic, View
from .models import Post

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
                'liked': liked
            }
        )
