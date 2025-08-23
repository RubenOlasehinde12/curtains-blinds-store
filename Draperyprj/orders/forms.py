from django import forms

SHIPPING = (
    ("standard", "Standard (3–5 days) — €0.00"),
    ("express",  "Express (1–2 days) — €6.99"),
)

class CheckoutForm(forms.Form):
    email = forms.EmailField(required=True, label="Email (for receipt)")
    phone = forms.CharField(required=False, label="Phone (optional)")

    shipping_method = forms.ChoiceField(
        choices=SHIPPING, initial="standard", widget=forms.RadioSelect, required=True
    )

   
    shipping_name = forms.CharField(required=False, label="Full name")
    shipping_country = forms.CharField(required=False, initial="Ireland")
    shipping_address1 = forms.CharField(required=False, label="Address")
    shipping_city = forms.CharField(required=False, label="City")
    shipping_postcode = forms.CharField(required=False, label="Postcode")

    coupon = forms.CharField(required=False, label="Coupon")
    notes = forms.CharField(required=False, widget=forms.Textarea, label="Order notes")
    agree = forms.BooleanField(required=True, label="I agree to the terms and privacy policy")
