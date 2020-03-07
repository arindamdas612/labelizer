from django import forms
from django.contrib.auth.models import User

class UpdateProfileForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    username = forms.CharField(max_length=20)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.u = kwargs.pop('u', None)
        self.e = kwargs.pop('e', None)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs['class'] = 'form-control round-form'
        self.fields['lastname'].widget.attrs['class'] = 'form-control round-form'
        self.fields['username'].widget.attrs['class'] = 'form-control round-form'
        self.fields['email'].widget.attrs['class'] = 'form-control round-form'
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if username != self.u:
            user_username = User.objects.filter(username=username).first()
            if user_username:
                raise forms.ValidationError(
                    f'User Name {username} is already taken. Try another!!!'
                )
        
        if email != self.e:
            user_email = User.objects.filter(email=email).first()
            if user_email:
                raise forms.ValidationError(
                    f'Email {email} is already taken. Try another!!!'
                )

