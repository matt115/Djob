from django.shortcuts import render

from django.views import generic

from .models import Profile
# Create your views here.

from django.shortcuts import get_object_or_404
from authentication.models import User
from django.urls import reverse
from django.shortcuts import redirect
from .models import Profile
from .forms import ProfileEditForm
from django.http import HttpResponseRedirect

from authentication.forms import UserEditForm
from django.utils.decorators import classonlymethod
from functools import update_wrapper
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    '''
    redirects to profile detail view.
    '''
    profile = get_object_or_404(Profile, user__email=request.user.email)
    return redirect(profile, permanent=True)

class ProfileDetailView(generic.detail.DetailView):
    '''
    Renders the profile requested by URL.
    '''
    model = Profile

    def get_object(self, queryset=None):
        if self.request.user.email == self.kwargs.get('email'):
            return self.request.user.profile

        pino = get_object_or_404(
            User,
            email=self.kwargs.get('email')
        )
        return pino.profile

    def _is_owner(self):
        if self.request.user.email == self.kwargs.get('email'):
            print("is owner!")
            return True
        return False

    def get_context_data(self, **kwargs):
        if self._is_owner():
            kwargs.update({'owner': True})

        kwargs.update({
            'friends': list(self.request.user.contacts.all())
        })
        return super(ProfileDetailView, self).get_context_data(**kwargs)

class EditAccountView(LoginRequiredMixin, PermissionRequiredMixin, generic.base.View, generic.base.TemplateResponseMixin):
    '''
    *_keys are form's fields which are used to split
    fields in POST request.
    '''
    template_name = 'account/profile_update_form.html'
    success_url = 'account:profile_detail'
    user_keys = ['email', 'first_name', 'last_name']
    profile_keys = ['description']

    permission_required = ('can_change_profile')

    @classmethod
    def check_and_save(cls, f1, f2):
        if f1.is_valid() and f2.is_valid():
            f1.save()
            f2.save()

    def post(self, request, *args, **kwargs):

        user_data = { k: request.POST[k] for k in self.user_keys }
        profile_data = { k: request.POST[k] for k in self.profile_keys }
        f1 = UserEditForm(user_data, instance=request.user)
        f2 = ProfileEditForm(profile_data, request.FILES, instance=request.user.profile)
        self.check_and_save(f1, f2)

        return HttpResponseRedirect(reverse(self.success_url,
                                            args=[request.user.email]))

    def get(self, request, *args, **kwargs):
        f1 = UserEditForm(instance=request.user)
        f2 = ProfileEditForm(instance=request.user.profile)
        return self.render_to_response({'f1': f1, 'f2': f2})
