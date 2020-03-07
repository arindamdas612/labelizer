from django import forms
from django.contrib.auth.models import User

class AddStaffForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()


    def __init__(self, *args, **kwargs):
        super(AddStaffForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        user_username = User.objects.filter(username=username).first()
        if user_username:
            raise forms.ValidationError(
                f'User Name {username} is already taken. Try another!!!'
            )
        
        user_email = User.objects.filter(email=email).first()
        if user_email:
            raise forms.ValidationError(
                f'Email {email} is already taken. Try another!!!'
            )
