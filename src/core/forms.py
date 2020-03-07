from django import forms

class ProductListForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

    def __init__(self, *args, **kwargs):
        super(ProductListForm, self).__init__(*args, **kwargs)
        self.fields['docfile'].widget.attrs['class'] = 'form-control'