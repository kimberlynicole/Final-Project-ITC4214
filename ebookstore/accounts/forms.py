from django import forms
from django.contrib.auth.models import User
import re
from django import forms
from .models import Profile
from books.models import Book


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name", 
        max_length=20, 
        required=True,
        error_messages={'required': 'Please fill in your first name'}
    )
    last_name = forms.CharField(
        label="Last Name", 
        max_length=20, 
        required=True,
        error_messages={'required': 'Please fill in your last name'}
    )
    username = forms.CharField(
        label="Username", 
        max_length=50, 
        required=True,
        error_messages={'required': 'Please fill in your username'}
    )
    email = forms.EmailField(
        label="Email", 
        required=True,
        error_messages={'required': 'Please fill in your email'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Password", 
        required=True,
        error_messages={'required': 'Please fill in your password'}
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        # Only letters, no numbers or special characters
        if not re.fullmatch(r'[A-Za-z]+', first_name):
            raise forms.ValidationError("First name must contain letters only")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.fullmatch(r'[A-Za-z]+', last_name):
            raise forms.ValidationError("Last name must contain letters only")
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise forms.ValidationError("Enter a valid email address")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters")
        if not any(char.isdigit() or not char.isalnum() for char in password):
            raise forms.ValidationError("Password must contain a number or special character")
        return password
class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


#Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']



from django import forms
from books.models import Book


from django import forms
from books.models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'published_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            # 🔥 IMPORTANT: DO NOT override file widgets
            # Let Django use ClearableFileInput automatically
        }

    # TITLE
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title or not title.replace(" ", "").isalnum():
            raise forms.ValidationError("Title must contain only letters and numbers.")
        return title

    # AUTHOR
    def clean_author(self):
        author = self.cleaned_data.get('author', '').strip()
        if not author or not author.replace(" ", "").isalpha():
            raise forms.ValidationError("Author must contain letters only.")
        return author

    # LANGUAGE
    def clean_language(self):
        language = self.cleaned_data.get('language', '').strip()
        if not language or not language.replace(" ", "").isalpha():
            raise forms.ValidationError("Language must contain letters only.")
        return language

    # CATEGORY
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Category is required.")
        return category

    # PAGES
    def clean_pages(self):
        pages = self.cleaned_data.get('pages')
        if not pages or pages <= 0:
            raise forms.ValidationError("Pages must be greater than 0.")
        return pages

    # PRICE
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not price or price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

    # DATE
    def clean_published_date(self):
        date = self.cleaned_data.get('published_date')
        if not date:
            raise forms.ValidationError("Published date is required.")
        return date

    # COVER
    def clean_cover(self):
        cover = self.cleaned_data.get('cover')
        if not cover and not self.instance.pk:
            raise forms.ValidationError("Cover image is required.")
        return cover

    # PDF
    def clean_pdf_file(self):
        pdf = self.cleaned_data.get('pdf_file')
        if not pdf and not self.instance.pk:
            raise forms.ValidationError("PDF file is required.")
        if pdf and not pdf.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return pdf




from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'bio']

        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }