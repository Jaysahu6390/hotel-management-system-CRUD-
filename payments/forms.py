from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:

        model = Payment

        fields = [
            "booking",
            "amount",
            "payment_method",
            "remarks",
        ]

        widgets = {

            "booking": forms.Select(
                attrs={"class": "form-select"}
            ),

            "amount": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "payment_method": forms.Select(
                attrs={"class": "form-select"}
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }