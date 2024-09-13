from django import forms
from course.models import Customer
from users.models import Users


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}), required=True)

    class Meta:
        model = Users
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This email "{email}" is already in use.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class SendingEmailForm(forms.Form):
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Email subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Email message'}))
    from_to = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'From'}))
    recipient = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'To'}))

    def clean_recipient(self):
        recipient = self.cleaned_data.get('recipient')
        if not recipient.endswith('@example.com'):
            raise forms.ValidationError('Recipient must use a valid "@example.com" email address.')
        return recipient
