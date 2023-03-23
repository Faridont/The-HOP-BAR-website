from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect

class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

        context = {
            'form': form
        }
        return  render(request, self.template_name, context)