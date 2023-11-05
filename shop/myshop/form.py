from .models import Comments
from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def save(self, commit=True):
        contact = super(ContactForm, self).save(commit=False)
        if commit:
            contact.save()
        return contact


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'email', 'text_comments')


class SubscribeForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'}))
