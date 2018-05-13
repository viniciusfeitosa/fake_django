from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'fakemodelapp/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'fakemodelapp/post_detail.html', {'post': post})


def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'fakemodelapp/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'fakemodelapp/post_edit.html', {'form': form})
