from django import forms

class FormImportarFilmes(forms.Form):

    titulo = forms.CharField(
        label='Título ou palavra chave',
        widget=forms.TextInput(attrs={'placeholder': ' Título ou palavra chave'})
    )
