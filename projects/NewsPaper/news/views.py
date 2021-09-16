from django.shortcuts import render
from django.http import HttpResponse
from .models import Post,PostCategory,Category,Comment

# Create your views here.
def home(request):
    post = Post.objects.all()
    cat = Category.objects.all()
    pc = PostCategory.objects.all()

    return render(request, 'home.html', {'post': post, 'cat': cat, 'pc': pc})