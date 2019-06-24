from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime as dt
from .models import Image, Comment, Profile, Contact, Like
from .forms import *
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    '''
    view function to display landing page
    '''
    if request.method == 'POST':
        current_user = request.user
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.main_user = current_user
            profile.save()
        return redirect('profile')
    else:
        form = UpdateProfileForm()

    return render(request, 'index.html',{"form":form})

@login_required(login_url='/accounts/login/')
def like(request,image_id):
    try:
        image=Image.objects.get(id=image_id)
    except Exception as e:
        raise  Http404()

    if request.method=='POST':
        current_user=request.user
        check = Like.objects.filter(main_user = current_user, picture = image_id).all()
        form=LikeForm(request.POST)
        if form.is_valid:
            if len(check) < 1:
                likes=form.save(commit=False)
                likes.main_user=current_user
                likes.picture= image_id
                likes.save()

                images = Image.objects.all()

                for photo in images:
                    likes = Like.objects.filter(picture = photo.id).all()
                    No = len(likes)
                    photo.likes = No

                return redirect('home')
            else:
                Like.objects.filter(main_user = current_user, picture = image_id).delete()
                images = Image.objects.all()
                return redirect('home')
    else:
        form=LikeForm()

    return render(request, 'home.html',{'images':images, "form":form})

@login_required(login_url='/accounts/login/')
def home(request):
    '''
    view function to feeds page
    '''
    current_user=request.user
    people = Contact.objects.filter(user_from = current_user)
    images = Image.objects.all()
    users = Profile.objects.all()

    for photo in images:
        likes = Like.objects.filter(picture = photo.id).all()
        No = len(likes)
        photo.likes = No

    form=LikeForm()

    return render(request, 'home.html',{'images':images, "form":form, "people":people,'current_user':current_user, "users":users})

@login_required(login_url='/accounts/login/')
def image(request):
    '''
    view function to upload image page
    '''
    current_user = request.user
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            user_profile = Profile.get_profile(current_user)
            image.main_user = current_user
            image.profile = user_profile
            image.save()
        return redirect('profile')
    else:
        form = UploadImageForm()

    return render(request, 'image.html', {"form":form})

@login_required(login_url="/accounts/login/")
def profile(request):
    title = request.user.username
    try:
        current_user=request.user
        photos=Image.objects.filter(main_user=current_user).all()
        profile=Profile.get_profile(current_user)
        current_user = request.user
        profile=Profile.get_profile(current_user)

        for photo in photos:
            comments = Comment.objects.filter(picture = photo.id).all()
            No = len(comments)
            photo.comments = No

        for photo in photos:
            likes = Like.objects.filter(picture = photo.id).all()
            No = len(likes)
            photo.likes = No

        followers = Contact.objects.filter(user_to = current_user).all()
        NoFollowers = len(followers)
        current_user.followers = NoFollowers

        following = Contact.objects.filter(user_from = current_user).all()
        NoFollowing = len(following)
        current_user.following = NoFollowing

        if request.method=='POST':
            form=UpdateProfileForm(request.POST,request.FILES )
            if form.is_valid():
                profile=form.save(commit=False)
                bio=form.cleaned_data['bio']
                profile_pic=form.cleaned_data['profile_pic']
                update = Profile.objects.filter(main_user=current_user).update(bio=bio,profile_pic=profile_pic)
                profile.save(update)
            return redirect("profile")
        else:
            form=UpdateProfileForm()

    except Exception as e:
        raise Http404()

    return render(request,"profile.html",{'profile':profile, "title":title, "photos":photos,"form":form})

@login_required(login_url='/accounts/login/')
def update(request):
    current_user = request.user
    profile=Profile.get_profile(current_user)

    if request.method=='POST':
        form=UpdateProfileForm(request.POST,request.FILES )
        if form.is_valid():
            profile=form.save(commit=False)
            bio=form.cleaned_data['bio']
            profile_pic=form.cleaned_data['profile_pic']
            update=Profile.objects.filter(main_user=current_user).update(bio=bio,profile_pic=profile_pic)
            profile.main_user=current_user
        return redirect("profile")
    else:

        form=UpdateProfileForm()

        return render(request,"update.html",{"form":form})

@login_required(login_url='/accounts/login/')
def comment(request,image_id):
    try:
        image=Image.objects.get(id=image_id)
    except Exception as e:
        raise  Http404()

    likes = Like.objects.filter(picture = image.id).all()
    No = len(likes)
    image.likes = No

    if request.method=='POST':
        current_user=request.user
        form=CommentForm(request.POST)
        if form.is_valid:
            comments=form.save(commit=False)
            comments.main_user=current_user
            comments.picture= image_id
            comments.save()
    else:
        form=CommentForm()

    comments = Comment.objects.filter(picture = image_id).all()
    return render(request,"comment.html",{"image":image,'form':form,"comments":comments})

@login_required(login_url='/accounts/login/')
def search(request):
    if 'user' in request.GET and request.GET['user']:
        name=request.GET.get("user")
        users=Profile.search_users(name)
        message=f'{name}'

        return render(request,'search.html',{'message':message,'users':users,"name":name})
    else:
        message="You did not search any user please input a user name"
        return render(request,"search.html",{"message":message})


@login_required(login_url='/accounts/login/')
def otherprofile(request,user_id):
    try:
        user = User.objects.get(id = user_id)
        profile=Profile.get_profile(user)
        photos=Image.objects.filter(main_user=user)
    except Exception as e:
        raise Http404()

    current_user = request.user

    followers = Contact.objects.filter(user_to = user).all()
    NoFollowers = len(followers)
    user.followers = NoFollowers

    following = Contact.objects.filter(user_from = user).all()
    NoFollowing = len(following)
    user.following = NoFollowing

    form=FollowForm()

    return render(request,"otherProfile.html",{"user":user,'profile':profile,"photos":photos,"form":form})

@login_required(login_url='/accounts/login/')
def follow(request,user_id):
    current_user=request.user
    user = User.objects.get(id = user_id)
    profile=Profile.get_profile(user)
    photos=Image.objects.filter(main_user=user)

    if current_user == user:
        return redirect("otherprofile",user_id)
    else:
        if request.method=='POST':
            check = Contact.objects.filter(user_from = current_user, user_to =user).all()
            form=FollowForm(request.POST)
            if form.is_valid:
                if len(check) < 1:
                    follow=form.save(commit=False)
                    follow.user_from=current_user
                    follow.user_to=user
                    follow.save()

                    followers = Contact.objects.filter(user_to = user).all()
                    NoFollowers = len(followers)
                    user.followers = NoFollowers

                    following = Contact.objects.filter(user_from = user).all()
                    NoFollowing = len(following)
                    user.following = NoFollowing

                    return redirect("otherprofile",user_id)

                else:
                    return redirect("otherprofile",user_id)

        else:
            form=FollowForm()

    return render(request,"otherProfile.html",{"user":user,'profile':profile,"photos":photos,"form":form})

