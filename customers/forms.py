from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = [
            'full_name',
            'email',
            'phone',
            'gender',
            'address',
            'nationality',
            'id_proof',
        ]

        widgets = {

            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Full Name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'nationality': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'id_proof': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Aadhaar, Passport, Driving Licence'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return phone


    def clean_email(self):
        email = self.cleaned_data["email"]

        exists = Customer.objects.exclude(
            pk=self.instance.pk
        ).filter(
            email=email
        ).exists()

        if exists:
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email