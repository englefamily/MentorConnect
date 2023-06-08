from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Remember Me', required=False)