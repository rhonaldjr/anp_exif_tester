from django import forms
from imglibrary.models import ImageFile

class FrmImageUpload(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ['image_file',]