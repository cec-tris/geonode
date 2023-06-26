from django import forms

from .models import Icon


class IconForm(forms.ModelForm):
    class Meta:
        model = Icon
        fields = ('name', 'path', )

    
    path = forms.FileField(
        widget=forms.FileInput(attrs={
                'accept':'.png, .jpg, .jpeg'
            })
        )