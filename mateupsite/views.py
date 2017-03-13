from django.db.models import Sum
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Attribute

# Create your views here.
class IndexPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class RegisterPageView(TemplateView, generic.FormView):
    success_url = "/"
    form_class = UserCreationForm
    template_name = "registration.html"

    def get(self, request, **kwargs):
        the_form = UserCreationForm()

        return render(request, self.template_name, context={"form": the_form})

    def post(self, request, *args, **kwargs):
        the_form = UserCreationForm(data=request.POST)
        if the_form.is_valid():
            u = the_form.save()
            u.save()
            return redirect('index')
        else:
            return render(request, self.template_name, context={"form": the_form})


class MatchPageView(LoginRequiredMixin, TemplateView):
    template_name = 'match.html'
    raise_exception = True # raise a 403 error instead of redirecting
    #login_url = "/"

    def get(self, request, **kwargs):
        user = Profile.objects.get(user=request.user)
        desired_attributes = user.attributes.filter(enabled=True) #Consider only enabled attribs
        candidates = Profile.objects.exclude(pk=user.pk)  #Avoid searching for ourselves
        candidates = candidates.filter(attributes__in=desired_attributes) #All users with at least one attr in common with the user
        candidates = candidates.annotate(proximity=Sum('attributes__value')) # This is the most important part, the candidates are evaluated by the sum of the value of the attributes they share with the user
        matches = candidates.order_by('-proximity')  #Best matches first
        return render(request, self.template_name, context={'user':user, 'matches': matches})