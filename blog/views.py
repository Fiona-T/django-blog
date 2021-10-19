from django.shortcuts import render
# for generic views - part of class based views
from django.views import generic
from .models import Post

# Create your views here.

class PostList(generic.ListView):
    # use the Post class as the model
    model = Post
    # get the data from table, filtered by published status, descending order
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6
