from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from .models import Blogpost
# index page function
def index(request):
    # return HttpResponse('Blog home page...')
    allposts = Blogpost.objects.all()
    return render(request, 'blog/index.html', {'allposts':allposts})

# blog post function
def blogpost(request, id):
    post = Blogpost.objects.filter(post_id=id)[0]
    return render(request, 'blog/blogpost.html', {'post':post})