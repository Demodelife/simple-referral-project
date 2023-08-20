from django import forms


class CodeConfirmForm(forms.Form):
    """
    Simple mock form to send verification code.
    """

    enter_code = forms.CharField(
        max_length=4,
        widget=forms.TextInput(
            attrs={'placeholder': '1234'}
        )
    )
