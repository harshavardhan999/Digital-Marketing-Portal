from django import forms




from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User









class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']



from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


from django.contrib.auth.forms import PasswordResetForm
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, required=True)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        