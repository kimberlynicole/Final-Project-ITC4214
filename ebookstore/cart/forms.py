from django import forms
import re

class PaymentForm(forms.Form):

    card_number = forms.CharField(
        label="Card Number",
        max_length=19,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "1234 5678 9012 3456"
        })
    )

    name_on_card = forms.CharField(
        label="Name on Card",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "John Doe"
        })
    )

    expiry_date = forms.CharField(
        label="Expiry Date",
        max_length=5,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "MM/YY"
        })
    )

    cvv = forms.CharField(
        label="CVV",
        max_length=4,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "123"
        })
    )

    #CARD NUMBER VALIDATION
    def clean_card_number(self):
        card = self.cleaned_data['card_number'].replace(" ", "")

        if not card.isdigit():
            raise forms.ValidationError("Card number must contain only digits.")

        if len(card) != 16:
            raise forms.ValidationError("Card number must be exactly 16 digits.")

        return card
    
    #validation on name on the card
    def clean_name_on_card(self):
        name = self.cleaned_data['name_on_card']

        # Only letters and spaces
        if not re.match(r'^[A-Za-z\s]+$', name):
            raise forms.ValidationError(
                "Name must contain only letters and spaces."
            )

        return name

    # CVV VALIDATION
    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']

        if not cvv.isdigit():
            raise forms.ValidationError("CVV must contain only digits.")

        if len(cvv) not in [3, 4]:
            raise forms.ValidationError("CVV must be 3 or 4 digits.")

        return cvv

    #  EXPIRY DATE VALIDATION
    def clean_expiry_date(self):
        expiry = self.cleaned_data['expiry_date']

        # MM/YY format
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiry):
            raise forms.ValidationError("Expiry date must be in MM/YY format.")

        return expiry