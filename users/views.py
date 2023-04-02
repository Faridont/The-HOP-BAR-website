from django.contrib.auth.views import LoginView
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from users.models import CustomAuthForm, CustomRegisterForm


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': CustomRegisterForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('auth')

        context = {
            'form': form
        }
        return  render(request, self.template_name, context)


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request):
        context = {
            'form': CustomAuthForm()
        }

        return render(request, self.template_name, context)