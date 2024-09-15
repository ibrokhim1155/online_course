from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from user.models import User

class CustomUserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class RegisterModelForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class SendingEmailForm(forms.Form):
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Subject'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your message'}),
        label='Message'
    )
    recipient_list = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter emails separated by commas'}),
        label='Recipient Emails'
    )

    def clean_recipient_list(self):
        data = self.cleaned_data['recipient_list']
        email_list = [email.strip() for email in data.split(',')]
        for email in email_list:
            if not forms.EmailField().clean(email):
                raise forms.ValidationError(f'Invalid email address: {email}')
        return ','.join(email_list)