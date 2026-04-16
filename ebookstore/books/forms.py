from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ['stars', 'comment']

        widgets = {
            'stars': forms.HiddenInput(),

            'comment': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'rows': 4,
                'placeholder': 'Share your thoughts about this book...'
            })
        }
    def clean_stars(self):
        stars = self.cleaned_data.get('stars')
        if not stars:
            raise forms.ValidationError("Please select a rating")
        return stars