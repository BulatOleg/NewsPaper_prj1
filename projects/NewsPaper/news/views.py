from django.views.generic import ListView, DetailView
from django.shortcuts import render
import datetime
from django.http import HttpResponse
from .models import Post, PostCategory, Category, Comment


# Create your views here.
def news(request):
    post = Post.objects.order_by('-dateCreation')[:6]
    cat = Category.objects.all ()
    pc = PostCategory.objects.all ()

    return render ( request, 'news.html', context={'post': post, 'cat': cat, 'pc': pc} )


def detail(request, slug):
    new = Post.objects.get(slug__iexact=slug)
    return render (request, 'detail.html', context={'new': new} )

def commentary(request):
    comm = Comment.objects.all()
    return render(request, 'detail,html', context={'comm': comm})

def news_home(request):
    return render(request, 'home.html')


class PostList ( ListView ):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'newsall'
    queryset = Post.objects.order_by ( '-id' )

    def get_context_data(self, **kwargs):
        context = super ().get_context_data ( **kwargs )
        context['time_now'] = datetime.utcnow ()  # добавим переменную текущей даты time_now
        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context


class PostDetail ( DetailView ):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно
    template_name = 'news.html'  # название шаблона будет news.html
    context_object_name = 'news'  # название объекта. в нём будет
