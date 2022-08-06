from django.views.generic import\
    ListView,\
    DetailView,\
    CreateView,\
    UpdateView,\
    DeleteView


from .forms import PostForm
from .filters import PostFilter
from django.urls import reverse_lazy
from datetime import datetime
from .models import (Author,
    Post,
    Category,
   )
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import resolve
from .tasks import new_post_subscription
from django.contrib import messages



class PostsList(ListView):
    model = Post
    permission_required = (
        'news.view_post',
    )
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 3


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs




class PostDetail(DetailView):
    model = Post
    permission_required = (
        'news.view_post',
    )
    template_name = 'new.html'
    context_object_name = 'new'


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = (
        'news.add_post',
    )
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')



    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.authorUser = Author.objects.get(authorUser=self.request.user)
        postauthor = self.object.authorUser
        DAILY_POST_LIMIT = 30
        error_message = f'No more than {DAILY_POST_LIMIT} posts a day, dude!'
        posts = Post.objects.all()

        today_posts_count = 0
        for post in posts:
            if post.author == postauthor:
                time_delta = datetime.now().date() - post.dateCreation.date()
                if time_delta.total_seconds() < (60 * 60 * 24):
                    today_posts_count += 1

        if today_posts_count < DAILY_POST_LIMIT:
            self.object.save()
            id_new_post = self.object.id
            print('notifying subscribers from view (no signals)...', id_new_post)
            new_post_subscription.apply_async([id_new_post], countdown=5)

            validated = super().form_valid(form)

        else:
            messages.error(self.request, self.error_message)
            validated = super().form_invalid(form)

        return validated


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = (
        'news.change_post',
    )
    template_name = 'profile_update.html'
    success_url = reverse_lazy('post_list')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        post.isUpdated = True
        return post


class PostDelete(DeleteView):
    model = Post
    permission_required = (
        'news.change_post',
    )
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')



class SearchListViews(PostsList):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostAuthor(ListView):
    model = Post
    template_name = 'filtered.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        queryset = Post.objects.filter(author=Author.objects.get(id=self.id))

        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['subscription_object'] = 'author_subscription'
        context['name'] = Author.objects.get(authorUser=user)

        is_subscribed = Author.objects.get(id=self.id).subscribers.filter(id=user.id).exists()
        context['is_subscribed'] = is_subscribed

        return context


class PostTag(ListView):
    model = Post
    template_name = 'filtered.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        queryset = Post.objects.filter(postCategory=Category.objects.get(id=self.id))
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['subscription_object'] = 'category_subscription'
        context['name'] = Category.objects.get(id=self.id)

        is_subscribed = Category.objects.get(id=self.id).subscribers.filter(id=user.id).exists()
        context['is_subscribed'] = is_subscribed

        return context


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()

    if not is_subscribed:
        cat.subscribers.add(user)
        html = render_to_string(
            template_name='subscribed_category.html',
            context={
                'categories': cat,
                'user': user,
            },
        )
        cat_repr = f'{cat}'
        email = user.email
        msg = EmailMultiAlternatives(
            subject=f'Subscription to {cat_repr} category',
            from_email=settings.EMAIL_HOST_USER,
            to=[email, 'mr.bacardi-92@mail.ru'],
        )

        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)

        return redirect('/news/')

    return redirect('/news/')


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()

    if is_subscribed:
        cat.subscribers.remove(user)
    return redirect('/news/')


