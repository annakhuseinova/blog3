from django.shortcuts import redirect, render
from .models import Article
from django.shortcuts import render
from django.http import Http404

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404
    

def create_post(request):
    #if not request.user.is_authenticated:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
            'text': request.POST["text"], 'title': request.POST["title"]
        }
        # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"] and Article.objects.filter(title=form["title"]).exists():
                # если поля заполнены без ошибок
                created_article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=created_article.id)
                # перейти на страницу поста
            elif Article.objects.filter(title=form["title"]).exists():
                form["errors"] = u"Название статьи не уникально!"
            else:
                # если введенные данные некорректны
                form["errors"] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    #else:
      #  raise Http404
    
    
        
