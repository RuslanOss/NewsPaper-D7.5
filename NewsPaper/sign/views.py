from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView

from .forms import UpdateProfileForm
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile_update.html'
    form_class = UpdateProfileForm
    success_url = '/news/'
    success_message = 'User profile updated successfully.'

    def get_object(self, **kwargs):
        return self.request.user