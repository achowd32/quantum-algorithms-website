from django import forms

class QftForm(forms.Form):
    state = forms.CharField(label="Initial State:", max_length = 6)

class ShorForm(forms.Form):
    a_val = forms.IntegerField(label="A-value:")
