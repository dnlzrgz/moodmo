from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ExportOptionsForm(forms.Form):
    export_format = forms.ChoiceField(
        choices=[
            ("csv", "CSV"),
            ("json", "JSON"),
        ],
    )
