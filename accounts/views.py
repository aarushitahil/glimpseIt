from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import ProfileForm, RegistrationForm
from .models import UserProfile

User = get_user_model()

def register(request):
    """ Add a new user """
    # redirect if user is already loggedIn
    if request.user.is_authenticated:
        return redirect(reverse('chat:home'))
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # Process POSTed Form data
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1']
                                    )
            # authenticate and log user in, then redirect to newsFeeds
            login(request, new_user)
            return redirect(reverse('chat:home'))

    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request, username):
    """ view profile of user with username """
    user = get_object_or_404(User, username=username)
    # check if current_user is already following the user
    is_following = request.user.is_following(user)
    return render(request, 'accounts/users_profile.html', {'user': user, 'is_following': is_following})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile

        username = request.POST.get('username')
        if username and username != user.username:
            user.username = username
        
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        
        profile.bio = request.POST.get('bio', profile.bio)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.website = request.POST.get('website', profile.website)
        profile.location = request.POST.get('address', profile.address)

        user.save()
        profile.save()

        return redirect('chat:home')  

    return render(request, 'accounts/edit_profile.html')


@login_required
def followers(request):
    # get users followed by the current_user
    users_followed = request.user.followers.all()
    
    # get_users not followed and exclude current_user from the list
    unfollowed_users = User.objects.exclude(id__in=users_followed).exclude(id=request.user.id)
    return render(request, 'accounts/followers.html', {'users_followed': users_followed, 'unfollowed_users': unfollowed_users})


@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    request.user.followers.add(user_to_follow)
    return redirect('accounts:followers')


@login_required
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    request.user.followers.remove(user_to_unfollow)
    return redirect('accounts:followers')