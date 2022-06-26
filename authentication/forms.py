import email
from django import forms
from django.contrib.auth import get_user_model

class Loginform(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()

class Registerform(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    cpassword = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        user = get_user_model()
        email = self.cleaned_data.get('email')
        valpwd = self.cleaned_data['password']
        valcpwd = self.cleaned_data['cpassword']
        username = self.cleaned_data['name']
        if valpwd != valcpwd:
            raise forms.ValidationError("Passwords do not match")
        if user.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already exists")
        if user.objects.filter(username=username).exists():
            raise forms.ValidationError("Username Already exists")
        return self.cleaned_data

class Profileform(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email','username','first_name', 'last_name']

