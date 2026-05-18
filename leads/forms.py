from django import forms

from .models import CareerApplication

MAX_RESUME_MB = 5
MAX_RESUME_BYTES = MAX_RESUME_MB * 1024 * 1024


class CareerApplicationForm(forms.ModelForm):
    class Meta:
        model = CareerApplication
        fields = ['full_name', 'email', 'location', 'college', 'role', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_classes = (
            'w-full px-5 py-3.5 bg-slate-50 border border-slate-200 rounded-xl '
            'focus:bg-white focus:border-brand-navy outline-none transition-all '
            'font-medium text-brand-navy'
        )
        self.fields['full_name'].widget.attrs.update({
            'class': base_classes,
            'placeholder': 'Full name',
        })
        self.fields['email'].widget.attrs.update({
            'class': base_classes,
            'placeholder': 'you@example.com',
        })
        self.fields['location'].widget.attrs.update({
            'class': base_classes,
            'placeholder': 'City, State',
        })
        self.fields['college'].widget.attrs.update({
            'class': base_classes,
            'placeholder': 'College or university',
        })
        self.fields['role'].widget.attrs.update({
            'class': base_classes,
        })
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
