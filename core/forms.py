from django import forms

class UploadForm(forms.Form):
    document = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'btn',
        'id': 'upload',
        'name': 'document',
        'placeholder': 'Upload',
    }))


class NewFolderForm(forms.Form):
    folder_name = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'folder-name',
        'name': 'folder-name',
        'placeholder': 'Folder name',
    }))

class DeleleForm(forms.Form):
    delete = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'name': 'delete',
        'placeholder': 'Delete?',
    }))