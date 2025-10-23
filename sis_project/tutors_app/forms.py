from django import forms
from admin_app.models import Tutor, Student, AcademicGroup


class TutorProfileForm(forms.ModelForm):
    """Form for editing tutor profile information"""
    
    class Meta:
        model = Tutor
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
            # Exclude current tutor from username uniqueness check
            if Tutor.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
                raise forms.ValidationError('Username already exists.')
        else:
            if Tutor.objects.filter(username=username).exists():
                raise forms.ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance and self.instance.pk:
            # Exclude current tutor from email uniqueness check
            if Tutor.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise forms.ValidationError('Email already exists.')
        else:
            if Tutor.objects.filter(email=email).exists():
                raise forms.ValidationError('Email already exists.')
        return email


class TutorPasswordChangeForm(forms.Form):
    """Form for changing tutor password"""
    
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
    
    def __init__(self, tutor, *args, **kwargs):
        self.tutor = tutor
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if self.tutor.password != current_password:
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


class StudentForm(forms.ModelForm):
    """Comprehensive form for student management"""
    
    # Add academic group field for display purposes
    academic_group_display = forms.ModelChoiceField(
        queryset=AcademicGroup.objects.none(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100',
            'disabled': 'disabled'
        }),
        label='Academic Group'
    )
    
    class Meta:
        model = Student
        fields = [
            # Academic Group (for display)
            'academic_group_display',
            # Personal Information
            'student_id', 'first_name', 'last_name', 'middle_name', 'birthday', 'gender', 'nation',
            'id_card', 'home_address', 'phone_number',
            'email', 'telegram_username', 'marital_status',
            
            # Family Status
            'is_from_large_family', 'is_from_low_income_family', 'is_from_troubled_family',
            'are_parents_deceased', 'are_parents_divorced', 'is_father_deceased', 'is_mother_deceased', 'has_disability',
            
            # Father Information
            'father_first_name', 'father_last_name', 'father_middle_name',
            'father_phone_number', 'father_telegram_username', 'is_father_retired', 'is_father_disabled',
            
            # Mother Information
            'mother_first_name', 'mother_last_name', 'mother_middle_name',
            'mother_phone_number', 'mother_telegram_username', 'is_mother_retired', 'is_mother_disabled',
            
            # Photo
            'photo'
        ]
        
        widgets = {
            # Personal Information
            'student_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Student ID (Optional - auto-generated if empty)'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Last Name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Middle Name (Optional)'
            }),
            'birthday': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary'
            }),
            'nation': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary'
            }),
            'id_card': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'ID Card (e.g., AD4843147)'
            }),
            'home_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Home Address',
                'rows': 3
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Phone Number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Email (Optional)'
            }),
            'telegram_username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Telegram Username (Optional)'
            }),
            'marital_status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary'
            }),
            
            # Father Information
            'father_first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Father's First Name"
            }),
            'father_last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Father's Last Name"
            }),
            'father_middle_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Father's Middle Name (Optional)"
            }),
            'father_phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Father's Phone Number"
            }),
            'father_telegram_username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Father's Telegram Username (Optional)"
            }),
            
            # Mother Information
            'mother_first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Mother's First Name"
            }),
            'mother_last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Mother's Last Name"
            }),
            'mother_middle_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Mother's Middle Name (Optional)"
            }),
            'mother_phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Mother's Phone Number"
            }),
            'mother_telegram_username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': "Mother's Telegram Username (Optional)"
            }),
            
            # Photo
            'photo': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        
        if group:
            self.fields['academic_group_display'].queryset = AcademicGroup.objects.filter(id=group.id)
            self.fields['academic_group_display'].initial = group
            self.fields['academic_group_display'].label = f'Academic Group: {group.group_name}'

    def clean(self):
        """Custom validation for student form - minimal validation for tutor input"""
        cleaned_data = super().clean()
        
        # Only basic validation - all fields are optional for tutors
        # Students will fill mandatory fields later in their dashboard
        
        # Handle parent deceased logic for consistency
        is_father_deceased = cleaned_data.get('is_father_deceased', False)
        is_mother_deceased = cleaned_data.get('is_mother_deceased', False)
        are_parents_deceased = cleaned_data.get('are_parents_deceased', False)
        
        # If both parents are deceased individually, set are_parents_deceased to True
        if is_father_deceased and is_mother_deceased:
            cleaned_data['are_parents_deceased'] = True
            
        # If are_parents_deceased is True, both individual flags should be True
        if are_parents_deceased:
            cleaned_data['is_father_deceased'] = True
            cleaned_data['is_mother_deceased'] = True
        
        # Optional phone number validation for living parents (when provided)
        if not is_father_deceased and not are_parents_deceased:
            father_name = cleaned_data.get('father_first_name')
            father_phone = cleaned_data.get('father_phone_number')
            
            # Only suggest if name is provided (indicating intent to fill father info)
            if father_name and not father_phone:
                self.add_error('father_phone_number', 'Phone number is recommended when providing father\'s information.')
        
        if not is_mother_deceased and not are_parents_deceased:
            mother_name = cleaned_data.get('mother_first_name')
            mother_phone = cleaned_data.get('mother_phone_number')
            
            # Only suggest if name is provided (indicating intent to fill mother info)  
            if mother_name and not mother_phone:
                self.add_error('mother_phone_number', 'Phone number is recommended when providing mother\'s information.')
        
        return cleaned_data