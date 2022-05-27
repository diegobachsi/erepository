from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import FormLogin, FormPasswordConfirm, FormPasswordReset, FormRegister
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.models import User
from django.contrib import messages

def logar(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('menu:index')
        else:
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    messages.error(request,'Este usuário não está ativo!')
                elif not user.check_password(password):
                    messages.error(request,'Senha incorreta!')
                form = FormLogin()
            except:
                messages.error(request,'Este usuário não existe!')
                form = FormLogin()
    else:
        form = FormLogin()

    context['form'] = form

    return render(request,'partials/login.html', context)

def register(request):
    context = {}
    template = 'partials/register.html'

    if request.method == "POST":
        form = FormRegister(request.POST)
        if form.is_valid():
            form.save()
            form.send_mail() 
            context['is_valid'] = True
            context['form'] = form
            return render(request, 'partials/validate.html', context)
    else:
        form = FormRegister()

    context['form'] = form

    return render(request, template, context)

def registerValidate(request, username): 

    user = User.objects.get(username=username)
    user.is_active = True
    user.save()

    return render(request, 'partials/validate_confirm.html')

def recover_password(request):

    template = 'partials/recover_password.html'
    context = {}

    return render(request, template, context)

class PasswordReset(PasswordResetView):
    form_class = FormPasswordReset
    template_name = 'partials/password_reset.html'
    subject_template_name = 'partials/password_reset_subject.txt'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        emails = [str(elem) for elem in list(User.objects.all().values_list('email'))]
        email = "('" + request.POST["email"] + "',)"
        if form.is_valid():
            if email in emails:
                return super().form_valid(form)
            else:
                messages.error(request, "Esse e-mail não está cadastrado.")

        return render(request, self.template_name, {'form': form})

class PasswordConfirm(PasswordResetConfirmView):
    form_class = FormPasswordConfirm
    template_name = 'partials/password_reset_confirm.html'