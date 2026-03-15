from django import forms
from .models import Project
import datetime
from user.models import Bid
class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["title", "description", "budget", "deadline","image"]

        widgets = {
            "deadline": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "min": datetime.date.today().isoformat()
                }
            )
        }



class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price", "message"]