from django import forms
from django.forms import inlineformset_factory
from .models import School, Department, AcademicGroup, Tutor, Admin


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'code', 'address', 'phone', 'email', 'website', 
                 'established_date', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter school name'
            }),
            'code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter school code (e.g., CS, ENG)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'rows': 3,
                'placeholder': 'Enter school address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter email address'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter website URL'
            }),
            'established_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'rows': 4,
                'placeholder': 'Enter school description'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary/20'
            })
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'head_name', 'phone', 'email', 
                 'office_location', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm',
                'placeholder': 'Department name'
            }),
            'code': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm',
                'placeholder': 'Dept. code'
            }),
            'head_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm',
                'placeholder': 'Department head name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm',
                'placeholder': 'Phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm',
                'placeholder': 'Email address'
            }),
            'office_location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm',
                'placeholder': 'Office location'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-sm',
                'rows': 2,
                'placeholder': 'Department description'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary/20'
            })
        }


# Create formset for departments
DepartmentFormSet = inlineformset_factory(
    School, 
    Department, 
    form=DepartmentForm,
    extra=1,  # Number of empty forms to display
    can_delete=True,
    min_num=1,  # Minimum number of departments required
    validate_min=True
)


class AcademicGroupForm(forms.ModelForm):
    class Meta:
        model = AcademicGroup
        fields = ['school', 'department', 'group_name', 'study_year', 'semester', 
                 'academic_year', 'max_students', 'current_students', 'description', 'is_active']
        widgets = {
            'school': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'id': 'id_school'
            }),
            'department': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'id': 'id_department'
            }),
            'group_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter group name (e.g., Group A, Morning Group)'
            }),
            'study_year': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all'
            }),
            'semester': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all'
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'e.g., 2024-2025'
            }),
            'max_students': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'min': '1',
                'max': '100',
                'placeholder': 'Maximum number of students'
            }),
            'current_students': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'min': '0',
                'placeholder': 'Current number of students'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'rows': 3,
                'placeholder': 'Enter group description'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary/20'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set department queryset based on selected school
        if 'school' in self.data:
            try:
                school_id = int(self.data.get('school'))
                self.fields['department'].queryset = Department.objects.filter(school_id=school_id, is_active=True)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.school.departments.filter(is_active=True)
        else:
            self.fields['department'].queryset = Department.objects.none()
        
        # Set active schools only
        self.fields['school'].queryset = School.objects.filter(is_active=True)

    def clean(self):
        cleaned_data = super().clean()
        current_students = cleaned_data.get('current_students', 0)
        max_students = cleaned_data.get('max_students', 0)
        
        if current_students > max_students:
            raise forms.ValidationError('Current students cannot exceed maximum students.')
        
        return cleaned_data


class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 
                 'phone_number', 'assigned_groups', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter last name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter unique username'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter temporary password'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Enter phone number'
            }),
            'assigned_groups': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary/20'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active academic groups
        self.fields['assigned_groups'].queryset = AcademicGroup.objects.filter(
            is_active=True
        ).select_related('school', 'department').order_by('school__name', 'department__name', 'study_year', 'semester')
        
        # Make password field show placeholder for editing
        if self.instance and self.instance.pk:
            self.fields['password'].widget.attrs['placeholder'] = 'Leave blank to keep current password'
            self.fields['password'].required = False
        
        # Add help text for assigned groups
        self.fields['assigned_groups'].help_text = 'Select academic groups this tutor will be responsible for'
        
        # Custom labels
        self.fields['assigned_groups'].label = 'Assigned Academic Groups'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Check if username exists (exclude current instance if editing)
            existing_tutor = Tutor.objects.filter(username=username)
            if self.instance and self.instance.pk:
                existing_tutor = existing_tutor.exclude(pk=self.instance.pk)
            
            if existing_tutor.exists():
                raise forms.ValidationError('This username is already taken.')
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email exists (exclude current instance if editing)
            existing_tutor = Tutor.objects.filter(email=email)
            if self.instance and self.instance.pk:
                existing_tutor = existing_tutor.exclude(pk=self.instance.pk)
            
            if existing_tutor.exists():
                raise forms.ValidationError('This email address is already registered.')
        
        return email

    def save(self, commit=True):
        tutor = super().save(commit=False)
        
        # Only update password if it's provided (for editing)
        password = self.cleaned_data.get('password')
        if password:
            tutor.password = password  # In a real app, you'd hash this
        
        if commit:
            tutor.save()
            self.save_m2m()  # Save many-to-many relationships
        
        return tutor


class AdminProfileForm(forms.ModelForm):
    """Form for editing admin profile information"""
    
    class Meta:
        model = Admin
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Last Name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Email Address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
                'placeholder': 'Phone Number'
            }),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance and self.instance.pk:
            # Exclude current admin from username uniqueness check
            if Admin.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
                raise forms.ValidationError('Username already exists.')
        else:
            if Admin.objects.filter(username=username).exists():
                raise forms.ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance and self.instance.pk:
            # Exclude current admin from email uniqueness check
            if Admin.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise forms.ValidationError('Email already exists.')
        else:
            if Admin.objects.filter(email=email).exists():
                raise forms.ValidationError('Email already exists.')
        return email


class PasswordChangeForm(forms.Form):
    """Form for changing admin password"""
    
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
            'placeholder': 'Enter current password'
        })
    )
    
    new_password = forms.CharField(
        label='New Password',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
            'placeholder': 'Enter new password (min 6 characters)'
        })
    )
    
    confirm_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all',
            'placeholder': 'Confirm new password'
        })
    )
    
    def __init__(self, admin, *args, **kwargs):
        self.admin = admin
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if self.admin.password != current_password:
            raise forms.ValidationError('Current password is incorrect.')
        return current_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError('New passwords do not match.')
        
        return cleaned_data