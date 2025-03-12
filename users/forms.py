from allauth.account.forms import SignupForm
from django import forms
from .models import User

class CustomSignupForm(SignupForm):
    """ Custom Signup Form that validates Student ID """

    name = forms.CharField(max_length=255, required=True, label="Full Name")
    student_id = forms.CharField(max_length=8, required=True, label="Student ID")

    def clean_student_id(self):
        """ Validate that the student ID is exactly 8 digits and contains only numbers """
        student_id = self.cleaned_data.get("student_id")

        # Ensure Student ID is exactly 8 characters long and contains only numbers
        if not student_id.isdigit() or len(student_id) != 8:
            raise forms.ValidationError("Invalid Student ID. It must be exactly 8 digits (numbers only).")

        # Ensure Student ID is unique (no duplicate student IDs)
        if User.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This Student ID is already registered.")

        return student_id

    def save(self, request):
        """ Save user with validated Student ID """
        user = super().save(request)
        user.name = self.cleaned_data["name"]
        user.student_id = self.cleaned_data["student_id"]
        user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'profile_picture']
