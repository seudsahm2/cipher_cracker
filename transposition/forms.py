from django import forms

class TranspositionForm(forms.Form):
    CIPHER_CHOICES = [
        ('railfence', 'Rail-fence'),
        ('columnar', 'Columnar'),
        ('route', 'Route'),
        ('double', 'Double Transposition'),
        ('myszkowski', 'Myszkowski'),
    ]
    
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    operation = forms.ChoiceField(choices=[('encrypt', 'Encrypt'), ('decrypt', 'Decrypt')])
    cipher_type = forms.ChoiceField(choices=CIPHER_CHOICES)
    
    # Conditional fields
    rails = forms.IntegerField(min_value=2, required=False)
    key = forms.CharField(required=False)
    key1 = forms.CharField(required=False)
    key2 = forms.CharField(required=False)
    rows = forms.IntegerField(min_value=1, required=False)
    cols = forms.IntegerField(min_value=1, required=False)