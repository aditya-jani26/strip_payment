from django import forms

class PaymentIntentForm(forms.Form):
    amount = forms.DecimalField(label='Amount (USD)', max_digits=10, decimal_places=2)
class PaymentMethodForm(forms.Form):
    payment_method_id = forms.CharField(widget=forms.HiddenInput())        