from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth.models import User
from .mail import send_mail_template
from django.contrib.auth import authenticate

class FormLogin(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Usuário'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Senha'})
    )

class FormRegister(UserCreationForm):

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        help_text="Entre com um e-mail válido!",
    )

    first_name = forms.CharField(
        label="Primeiro Nome",
        widget=forms.TextInput(attrs={'autocomplete': 'first_name'}),
        help_text="Primeiro nome",
    )

    last_name = forms.CharField(
        label="Último Nome",
        widget=forms.TextInput(attrs={'autocomplete': 'last_name'}),
        help_text="Último nome",
    )

    #new
    def send_mail(self):
        email = self.cleaned_data["email"]
        subject = 'Ativar Cadastro'
        context = {
            'username': self.cleaned_data['username'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email'],

        }
        template_name = 'validate_send_email.html'
        send_mail_template(
            subject, template_name, context, [email]
        )

    #new
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_active = False
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':'Usuário', 'class':'form-control'})
        self.fields['first_name'].widget.attrs.update({'placeholder':'Primeiro Nome', 'class':'form-control'})
        self.fields['last_name'].widget.attrs.update({'placeholder':'Último Nome', 'class':'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder':'Email', 'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Senha', 'class':'form-control'})        
        self.fields['password2'].widget.attrs.update({'placeholder':'Repetir Senha', 'class':'form-control'})

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'unique': 'Já existe no cadastro um usuário com este nome.',
            },
        }

class FormPasswordReset(PasswordResetForm):

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'class':'form-control', 'autocomplete': 'email', 'placeholder': 'E-mail'})
    )

class FormPasswordConfirm(SetPasswordForm):

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password', 'placeholder': 'Nova Senha'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete': 'new-password', 'placeholder': 'Confirme a Senha'}),
    )