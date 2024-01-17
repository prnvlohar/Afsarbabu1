
from django import forms

from users.models import CustomUser

# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        password = forms.CharField(
            widget=forms.PasswordInput
        )
        widgets = {
            # 'password': forms.PasswordInput(),
            'phone': forms.NumberInput(),
        }
        fields = ['email', 'phone', 'password', 'type']

        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if (phone.isdigit()):
                if len(phone) == 10:
                    return phone
                raise forms.ValidationError("must be of 10 dugut")
            raise forms.ValidationError("must be of number type")

        # def clean_password(self):
        #     print('=======================')
        #     password = self.cleaned_data.get('password')
        #     try:
        #         validate_password(password, self.instance)
        #     except forms.ValidationError as error:
        #         print('----------------', error)
        #         # Method inherited from BaseForm
        #         self.add_error('password', error)
        #     return password


class LoginForm(forms.ModelForm):

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput())
        model = CustomUser
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['email', 'password']
