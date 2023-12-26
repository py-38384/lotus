from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username','email','password1','password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input_field'

class ProfileCostomize(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','bio','mobile_number','display_picture']