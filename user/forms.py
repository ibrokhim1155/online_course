from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from user.models import User


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    # def clean(self):
    #     password = self.data.get('password')
    #     password2 = self.data.get('confirm_password')
    #
    #     if password != password2:
    #         raise forms.ValidationError('Passwords do not match.')
    #
    #     return password

    # def save(self, commit=True):
    #     user = super(RegisterModelForm, self).save(commit=False)
    #     user.set_password(self.data['password'])
    #     user.is_active = True
    #     user.is_staff = True
    #     user.is_superuser = True
    #     if commit:
    #         user.save()
    #     return user


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
