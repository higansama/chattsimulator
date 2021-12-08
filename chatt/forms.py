from django.forms import ModelForm
from .models import *

class FormBook(ModelForm):
  class Meta:
    model = UserChatt
    fields = ['username']

