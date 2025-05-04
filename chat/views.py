from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from .forms import CommentForm, PostForm
from .models import Post, Comment


@login_required
def home(request):
    # Get users whose posts to display on news feed and add users account
    _users = list(request.user.followers.all())
    _users.append(request.user)

    # Get posts from users accounts whose posts to display and order by latest
    # Use select_related to optimize queries
    posts = Post.objects.filter(user__in=_users).order_by('-posted_date').select_related('user')
    
    # No need to manually set comments, Django's template system will access them as needed
    # The line below was causing an error:
    # for post in posts:
    #     post.comments = post.comments.set()
    
    return render(request, 'chat/home.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        if 'description' in request.POST:
            description = request.POST.get('description')
            picture = request.FILES.get('image')
            
            post = Post(user=request.user, description=description)
            if picture:
                post.picture = picture
            post.save()
            return redirect('chat:home')
        else:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('chat:home')
    else:
        form = PostForm()
    return render(request, 'chat/add_post.html', {'form': form})


@login_required
@require_POST
def comment_post(request, post_id):
    """ Add a comment to a post - Renamed from add_comment for template consistency """
    post = get_object_or_404(Post, id=post_id)
    
    if 'text' in request.POST:
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, user=request.user, text=text)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    
    return redirect('chat:home')