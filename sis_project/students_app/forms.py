from django import forms
from admin_app.models import Student


class StudentPersonalDataForm(forms.ModelForm):
    """Form for student personal data - birthday, gender, and nation (other data provided by tutor)"""
    
    class Meta:
        model = Student
        fields = ['birthday', 'gender', 'nation', 'marital_status']
        
        widgets = {
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
            'marital_status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary'
            }),
        }
    
    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if not birthday:
            raise forms.ValidationError('Birthday is required.')
        return birthday
    
    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError('Gender is required.')
        return gender
    
    def clean_nation(self):
        nation = self.cleaned_data.get('nation')
        if not nation:
            raise forms.ValidationError('Nation is required.')
        return nation
    
    def clean_marital_status(self):
        marital_status = self.cleaned_data.get('marital_status')
        if not marital_status:
            raise forms.ValidationError('Marital status is required.')
        return marital_status


class StudentContactInfoForm(forms.ModelForm):
    """Form for student contact information (removed Instagram and emergency contact info)"""
    
    class Meta:
        model = Student
        fields = ['phone_number', 'home_address', 'email', 'telegram_username']
        
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Phone Number'
            }),
            'home_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Home Address',
                'rows': 3
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Email (Optional)'
            }),
            'telegram_username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Telegram Username (Optional)'
            }),
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('Phone number is required.')
        return phone_number
    
    def clean_home_address(self):
        home_address = self.cleaned_data.get('home_address')
        if not home_address:
            raise forms.ValidationError('Home address is required.')
        return home_address


class StudentFamilyInfoForm(forms.ModelForm):
    """Form for student family information"""
    
    class Meta:
        model = Student
        fields = [
            'is_father_deceased', 'is_mother_deceased', 'are_parents_divorced',
            'father_first_name', 'father_last_name', 'father_middle_name',
            'father_phone_number', 'is_father_retired', 'is_father_disabled',
            'mother_first_name', 'mother_last_name', 'mother_middle_name',
            'mother_phone_number', 'is_mother_retired', 'is_mother_disabled',
            'siblings_count', 'children_count', 'guardian_name', 'guardian_phone_number'
        ]
        
        widgets = {
            'is_father_deceased': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
            'is_mother_deceased': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
            'are_parents_divorced': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
            'father_first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Father\'s First Name'
            }),
            'father_last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Father\'s Last Name'
            }),
            'father_middle_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Father\'s Middle Name (Optional)'
            }),
            'father_phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Father\'s Phone Number'
            }),
            'is_father_retired': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
            'is_father_disabled': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
            'mother_first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Mother\'s First Name'
            }),
            'mother_last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Mother\'s Last Name'
            }),
            'mother_middle_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Mother\'s Middle Name (Optional)'
            }),
            'mother_phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Mother\'s Phone Number'
            }),
            'is_mother_retired': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
            'is_mother_disabled': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
            'siblings_count': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Number of Siblings',
                'min': 0
            }),
            'children_count': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Number of Children (if married)',
                'min': 0
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Legal Guardian Full Name (if both parents deceased)'
            }),
            'guardian_phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Guardian Phone Number'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        is_father_deceased = cleaned_data.get('is_father_deceased', False)
        is_mother_deceased = cleaned_data.get('is_mother_deceased', False)
        
        # Validate father information if not deceased
        if not is_father_deceased:
            father_first_name = cleaned_data.get('father_first_name')
            father_last_name = cleaned_data.get('father_last_name')
            father_phone = cleaned_data.get('father_phone_number')
            
            if not father_first_name:
                self.add_error('father_first_name', 'Father\'s first name is required.')
            if not father_last_name:
                self.add_error('father_last_name', 'Father\'s last name is required.')
            if not father_phone:
                self.add_error('father_phone_number', 'Father\'s phone number is required.')
        
        # Validate mother information if not deceased
        if not is_mother_deceased:
            mother_first_name = cleaned_data.get('mother_first_name')
            mother_last_name = cleaned_data.get('mother_last_name')
            mother_phone = cleaned_data.get('mother_phone_number')
            
            if not mother_first_name:
                self.add_error('mother_first_name', 'Mother\'s first name is required.')
            if not mother_last_name:
                self.add_error('mother_last_name', 'Mother\'s last name is required.')
            if not mother_phone:
                self.add_error('mother_phone_number', 'Mother\'s phone number is required.')
        
        # Validate guardian information if both parents are deceased
        if is_father_deceased and is_mother_deceased:
            guardian_name = cleaned_data.get('guardian_name')
            guardian_phone = cleaned_data.get('guardian_phone_number')
            
            if not guardian_name:
                self.add_error('guardian_name', 'Legal guardian name is required when both parents are deceased.')
            if not guardian_phone:
                self.add_error('guardian_phone_number', 'Guardian phone number is required when both parents are deceased.')
        
        return cleaned_data


class StudentAdditionalInfoForm(forms.ModelForm):
    """Form for additional student information - Personal Interests & Skills only"""
    
    # Hobbies choices
    HOBBY_CHOICES = [
        ('', 'Select a hobby'),
        ('reading', 'Reading'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('drawing', 'Drawing/Art'),
        ('cooking', 'Cooking'),
        ('travel', 'Traveling'),
        ('gaming', 'Gaming'),
        ('photography', 'Photography'),
        ('dancing', 'Dancing'),
        ('movies', 'Watching Movies'),
        ('other', 'Other'),
    ]
    
    # Special Skills choices
    SKILL_CHOICES = [
        ('', 'Select a skill'),
        ('computer_skills', 'Computer Skills'),
        ('programming', 'Programming'),
        ('graphic_design', 'Graphic Design'),
        ('musical_instrument', 'Musical Instrument'),
        ('public_speaking', 'Public Speaking'),
        ('leadership', 'Leadership'),
        ('teamwork', 'Teamwork'),
        ('problem_solving', 'Problem Solving'),
        ('communication', 'Communication'),
        ('time_management', 'Time Management'),
        ('other', 'Other'),
    ]
    
    # Languages for Central Asia
    LANGUAGE_CHOICES = [
        ('', 'Select a language'),
        ('uzbek', 'Uzbek'),
        ('russian', 'Russian'), 
        ('english', 'English'),
        ('kazakh', 'Kazakh'),
        ('kyrgyz', 'Kyrgyz'),
        ('tajik', 'Tajik'),
        ('turkmen', 'Turkmen'),
        ('karakalpak', 'Karakalpak'),
        ('turkish', 'Turkish'),
        ('persian', 'Persian'),
        ('arabic', 'Arabic'),
        ('chinese', 'Chinese'),
        ('korean', 'Korean'),
        ('other', 'Other'),
    ]
    
    hobbies = forms.ChoiceField(
        choices=HOBBY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary'
        })
    )
    
    hobbies_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': 'Please specify your hobby'
        })
    )
    
    special_skills = forms.ChoiceField(
        choices=SKILL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary'
        })
    )
    
    special_skills_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': 'Please specify your special skill'
        })
    )
    
    languages_spoken = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary'
        })
    )
    
    languages_spoken_other = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': 'Please specify the language and proficiency level'
        })
    )
    
    class Meta:
        model = Student
        fields = []  # We'll handle the data manually


class StudentPasswordChangeForm(forms.Form):
    """Form for changing student password"""
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': 'Current Password'
        }),
        label='Current Password'
    )
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': 'New Password'
        }),
        label='New Password',
        min_length=6,
        help_text='Password must be at least 6 characters long.'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': 'Confirm New Password'
        }),
        label='Confirm New Password'
    )
    
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if self.instance and not self.instance.check_password(current_password):
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