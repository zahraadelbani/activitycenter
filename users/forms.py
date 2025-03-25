from allauth.account.forms import SignupForm
from django import forms
from .models import User

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=255, required=True, label="Full Name")
    student_id = forms.CharField(max_length=8, required=False, label="Student ID")

    def clean_student_id(self):
        student_id = self.cleaned_data.get("student_id")
        if student_id:
            if not student_id.isdigit() or len(student_id) != 8:
                raise forms.ValidationError("Invalid Student ID. It must be exactly 8 digits (numbers only).")
            if User.objects.filter(student_id=student_id).exists():
                raise forms.ValidationError("This Student ID is already registered.")
        return student_id

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data["name"]
        user.student_id = self.cleaned_data.get("student_id", None)
        user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        new_picture = self.cleaned_data.get("profile_picture")

        # Only delete and replace if a new picture was uploaded
        if new_picture and new_picture != user.profile_picture:
            if user.profile_picture and hasattr(user.profile_picture, 'path'):
                user.profile_picture.delete(save=False)
            user.profile_picture = new_picture

        if commit:
            user.save()
        return user


