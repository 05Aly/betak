from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Property

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'phone_numbers', 'account_type', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure email and profile_picture are required
        self.fields['email'].required = True
        self.fields['profile_picture'].required = True
        
        # Style form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 mt-1 border rounded-xl bg-brand-dayBg dark:bg-brand-nightBg border-brand-dayBorder dark:border-brand-nightBorder text-brand-dayText dark:text-brand-nightText focus:ring-brand-teal focus:border-brand-teal focus:outline-none'
            })

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'price', 'address', 'description', 'image', 'video']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 mt-1 border rounded-xl bg-brand-dayBg dark:bg-brand-nightBg border-brand-dayBorder dark:border-brand-nightBorder text-brand-dayText dark:text-brand-nightText focus:ring-brand-teal focus:border-brand-teal focus:outline-none'
            })
