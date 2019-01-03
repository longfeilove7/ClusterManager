from django import forms


class FileUploadForm(forms.Form):
    name = forms.CharField(max_length=20, min_length=3, required=True, label='名称:')
    my_file = forms.FileField(label='文件名称:')

