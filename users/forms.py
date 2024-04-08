
from django import forms

from users.models import CustomUser


class RegisterForm(forms.ModelForm):

    referral_code = forms.CharField(max_length=10, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password', 'institute',
                  'recommended_by', 'referral_code']

        widgets = {
            'password': forms.PasswordInput(),
            'phone': forms.NumberInput(),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone.isdigit():
            if len(phone) == 10:
                return phone
            raise forms.ValidationError("Phone number must be 10 digits long.")
        raise forms.ValidationError("Phone number must contain only digits.")


# class InstituteRegisterForm(forms.ModelForm):

#     class Meta:
#         model = CustomUser
#         password = forms.CharField(
#             widget=forms.PasswordInput
#         )
#         name = forms.CharField(max_length=100)
#         widgets = {
#             'phone': forms.NumberInput(),
#         }
#         fields = ['email', 'phone', 'password', 'name']

#         def clean_phone(self):
#             phone = self.cleaned_data.get('phone')
#             if (phone.isdigit()):
#                 if len(phone) == 10:
#                     return phone
#                 raise forms.ValidationError("must be of 10 dugut")
#             raise forms.ValidationError("must be of number type")

class LoginForm(forms.ModelForm):

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput())
        model = CustomUser
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['email', 'password']


class UsersForm(forms.Form):

    institute = forms.CharField(max_length=100)
    students = forms.CharField(max_length=100)
