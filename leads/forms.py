from django import forms

from .models import CareerApplication, Role

MAX_RESUME_MB = 5
MAX_RESUME_BYTES = MAX_RESUME_MB * 1024 * 1024

BASE_CLASSES = (
    'w-full px-5 py-3.5 bg-slate-50 border border-slate-200 rounded-xl '
    'focus:bg-white focus:border-brand-navy outline-none transition-all '
    'font-medium text-brand-navy'
)


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'job_description', 'requirements', 'responsibilities', 'benefits', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': BASE_CLASSES,
            'placeholder': 'e.g., Wealth Analyst',
        })
        self.fields['job_description'].widget.attrs.update({
            'class': BASE_CLASSES + ' resize-none',
            'placeholder': 'Complete job description (mandatory)',
            'rows': 6,
        })
        self.fields['requirements'].widget.attrs.update({
            'class': BASE_CLASSES + ' resize-none',
            'placeholder': 'Technical and soft skills requirements',
            'rows': 4,
        })
        self.fields['responsibilities'].widget.attrs.update({
            'class': BASE_CLASSES + ' resize-none',
            'placeholder': 'Key responsibilities',
            'rows': 4,
        })
        self.fields['benefits'].widget.attrs.update({
            'class': BASE_CLASSES + ' resize-none',
            'placeholder': 'Benefits and perks',
            'rows': 3,
        })
        self.fields['is_active'].widget.attrs.update({
            'class': 'w-4 h-4 cursor-pointer',
        })


class CareerApplicationForm(forms.ModelForm):
    class Meta:
        model = CareerApplication
        fields = ['full_name', 'email', 'location', 'college', 'role', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({
            'class': BASE_CLASSES,
            'placeholder': 'Full name',
        })
        self.fields['email'].widget.attrs.update({
            'class': BASE_CLASSES,
            'placeholder': 'you@example.com',
        })
        self.fields['location'].widget.attrs.update({
            'class': BASE_CLASSES,
            'placeholder': 'City, State',
        })
        self.fields['college'].widget.attrs.update({
            'class': BASE_CLASSES,
            'placeholder': 'College or university',
        })
        self.fields['role'].widget.attrs.update({
            'class': BASE_CLASSES,
        })
        # Only show active roles in the dropdown
        self.fields['role'].queryset = Role.objects.filter(is_active=True)
        self.fields['resume'].widget.attrs.update({
            'class': (
                'w-full px-5 py-3.5 bg-slate-50 border border-dashed border-slate-200 '
                'rounded-xl focus:bg-white focus:border-brand-navy outline-none transition-all '
                'font-medium text-brand-navy'
            ),
            'accept': 'application/pdf',
        })

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if not resume:
            return resume
        if resume.size > MAX_RESUME_BYTES:
            raise forms.ValidationError(
                f'Resume must be under {MAX_RESUME_MB} MB.'
            )
        return resume
