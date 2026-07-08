from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'room_number',
            'room_type',
            'price',
            'capacity',
            'floor',
            'status',
            'description',
            'image',
        ]

        widgets = {
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Room Number'
            }),

            'room_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Price'
            }),

            'capacity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'floor': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }