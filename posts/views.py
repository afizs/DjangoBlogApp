from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic.edit import View
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

from .models import Post
from .forms import PostForm, UserForm, LoginForm


# Create your views here.
def hello(request):
    return HttpResponse('Hello World!!')


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return reverse('posts:index')
            else:
                return render(request, 'posts/login.html', {'form': form})
        else:
            return render(request, 'posts/login.html', {'form': form})
    return render(request, 'posts/login.html', {'form': form})


def index(request):
    # logout(request)
    # query_set_list = Post.objects.all().order_by('-timestamp')
    query_set_list = Post.objects.filter(publish__lte=timezone.now()).order_by('-timestamp')
    query = request.GET.get('q')
    if query:
        query_set_list = query_set_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query)).distinct()

    paginator = Paginator(query_set_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        query_set = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_set = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_set = paginator.page(paginator.num_pages)
    context = {
        'object_list': query_set,
        'title': 'Post List'
    }
    return render(request, 'posts/index.html', context)


def detail(request, post_id=None):
    data = get_object_or_404(Post, id=post_id)
    context = {
        'title': data.title,
        'instance': data
    }
    return render(request, 'posts/detail.html', context)


def create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    # to save the data in the db
    if form.is_valid():
        data = form.save(commit=False)
        data.author = request.user
        data.save()
        messages.success(request, 'Successfully created!!')
        return HttpResponseRedirect(data.get_absolute_url())
    if form.errors:
        messages.error(request, 'Not created!!')

    context = {
        'form': form
    }
    return render(request, 'posts/post_form.html', context)
    # if request.method == 'POST':
    #     print request.POST.get('content')


def update(request, post_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Updated!!')
        # success message
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form
        }
    return render(request, 'posts/post_form.html', context)


def delete(request, post_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=post_id)
    instance.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect('posts:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'posts/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data..
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # cleaned normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return user object if credentials are correct
            user = authenticate(username= username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('posts:index')
        return render(request, self.template_name, {'form': form})









