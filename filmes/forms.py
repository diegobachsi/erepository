from django import forms

class FormCadastrar(forms.Form):

    titulo = forms.CharField(label='Título', widget=forms.TextInput(attrs={'placeholder': 'Título'}))
    descricao = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={'placeholder': 'Descrição'}))
    url_imagem = forms.CharField(label='Url Imagem', widget=forms.TextInput(attrs={'placeholder': 'Url da Imagem'}))
    assistiu = forms.BooleanField(label='Assistiu?', required=False)