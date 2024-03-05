from django import forms


class LogisticForm(forms.Form):
    ADMIN_CHOICES = (
        ('На складе в Китае', 'На складе в Китае'),
        ('В пути', 'В пути'),
        ('В пункте выдачи', 'В пункте выдачи'),
    )
    FIELD_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )

    file = forms.FileField()
    password = forms.CharField()
    admin_status = forms.ChoiceField(choices=ADMIN_CHOICES)
    field_choice = forms.ChoiceField(choices=FIELD_CHOICES)
