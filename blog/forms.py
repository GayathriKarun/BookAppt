from django import forms
from .models import Blog, CATEGORY_CHOICES
from signup.models import User


class BlogForm(forms.ModelForm):
    title = forms.CharField(label='Topic',
                            widget = forms.TextInput(attrs=
                                {
                                "placeholder" : "Enter a Topic here"
                                }))
    content = forms.CharField( widget=forms.Textarea(attrs=
                                 {
                                    "placeholder": "Enter the content here",
                                     "rows" : 20,
                                     "cols" : 50
                                 }))
    summary = forms.CharField( widget=forms.Textarea(attrs=
                                 {
                                    "placeholder": "Enter the summary here",
                                     "rows" : 2,
                                     "cols" : 50
                                 }))
    
    class Meta:
        
        model = Blog
        fields = ['title','img','summary','category','content','draft']


CATEGORY_CHOICES = (
    ("All", "All"),
    ("Mental Health", "Mental Health"),
    ("Heart Disease", "Heart Disease"),
    ("Covid19", "Covid19"),
    ("Immunization", "Immunization"),
)

class BookingForm(forms.Form):
    speciality = forms.CharField(label="Required Speciality", max_length=255, required=True)
    startDateTime = forms.DateTimeField(label="startDateTime", input_formats=['%Y/%m/%d %H:%M'], required=True)