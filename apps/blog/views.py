from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Category, Tag
from .forms import PostForm


def post_list_view(request):
    posts_list = Post.objects.filter(
        status='published'
    ).select_related('author', 'category').prefetch_related('tags')
    
    # Search
    query = request.GET.get('q')
    if query:
        posts_list = posts_list.filter(title__icontains=query)

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts_list = posts_list.filter(category__slug=category_slug)

    # Pagination
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
    })


def post_detail_view(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags'),
        slug=slug,
        status='published'
    )
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_create_view(request):
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to create posts.')
        return redirect('blog')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully.')
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_edit_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to edit posts.')
        return redirect('blog')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Edit'})


@login_required
def post_delete_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to delete posts.')
        return redirect('blog')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('blog')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})