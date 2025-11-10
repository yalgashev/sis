"""
Advanced filtering forms for tutor reports
"""
import django_filters
from django import forms
from django.db.models import Q
from admin_app.models import Student, AcademicGroup, School, Department


class AdvancedStudentFilter(django_filters.FilterSet):
    """Advanced filter for students with all database fields"""
    
    # Search by name
    search = django_filters.CharFilter(
        method='filter_by_name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name...'
        }),
        label='Search Name'
    )
    
    # Academic Information
    academic_group = django_filters.ModelChoiceFilter(
        queryset=AcademicGroup.objects.none(),  # Will be set dynamically
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="All Groups"
    )
    
    department = django_filters.ModelChoiceFilter(
        field_name='academic_group__department',
        queryset=Department.objects.none(),  # Will be set dynamically
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="All Departments"
    )
    
    # Personal Information
    gender = django_filters.ChoiceFilter(
        choices=Student.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="All Genders"
    )
    
    nation = django_filters.ChoiceFilter(
        choices=Student.NATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="All Nationalities"
    )
    
    marital_status = django_filters.ChoiceFilter(
        choices=Student.MARITAL_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="All Statuses"
    )
    
    # Personal Information Filters
    id_card = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by ID card number...'
        }),
        label='ID Card Number'
    )
    
    hobbies = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search hobbies and interests...'
        }),
        label='Hobbies & Interests'
    )
    
    special_skills = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search special skills and talents...'
        }),
        label='Special Skills & Talents'
    )
    
    languages_spoken = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search languages spoken...'
        }),
        label='Languages Spoken'
    )
    
    # Family Status Filters
    is_from_large_family = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='From Large Family',
        empty_label=None
    )
    
    is_from_low_income_family = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='From Low Income Family',
        empty_label=None
    )
    
    is_from_troubled_family = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='From Troubled Family',
        empty_label=None
    )
    
    are_parents_deceased = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Parents Deceased',
        empty_label=None
    )
    
    are_parents_divorced = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Parents Divorced',
        empty_label=None
    )
    
    is_father_deceased = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Father Deceased',
        empty_label=None
    )
    
    is_mother_deceased = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Mother Deceased',
        empty_label=None
    )
    
    has_disability = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Has Disability',
        empty_label=None
    )
    
    # Parent Status
    is_father_retired = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Father Retired',
        empty_label=None
    )
    
    is_father_disabled = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Father Disabled',
        empty_label=None
    )
    
    is_mother_retired = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Mother Retired',
        empty_label=None
    )
    
    is_mother_disabled = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Mother Disabled',
        empty_label=None
    )
    
    # Siblings and Children Count
    siblings_count = django_filters.NumberFilter(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of siblings',
            'min': 0
        }),
        label='Siblings Count'
    )
    
    children_count = django_filters.NumberFilter(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of children',
            'min': 0
        }),
        label='Children Count'
    )
    
    # Code of Conduct Agreement
    agreed_to_code_of_conduct = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Agreed to Code of Conduct',
        empty_label=None
    )
    
    # Active Status
    is_active = django_filters.ChoiceFilter(
        choices=[('', 'Any'), (True, 'Yes'), (False, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Active Students Only',
        empty_label=None
    )
    
    class Meta:
        model = Student
        fields = []
    
    def __init__(self, *args, **kwargs):
        """Initialize filter with tutor's assigned groups"""
        assigned_groups = kwargs.pop('assigned_groups', None)
        super().__init__(*args, **kwargs)
        
        if assigned_groups is not None:
            self.filters['academic_group'].queryset = assigned_groups
            # Also filter departments to only show those from assigned groups
            # Convert queryset to list to avoid slice+distinct issue
            department_ids = list(assigned_groups.values_list('department_id', flat=True))
            department_ids = list(set(department_ids))  # Remove duplicates manually
            self.filters['department'].queryset = Department.objects.filter(id__in=department_ids)
    
    def filter_by_name(self, queryset, name, value):
        """Filter by first name, last name, or middle name"""
        if value:
            return queryset.filter(
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(middle_name__icontains=value)
            )
        return queryset


class QuickStudentFilter(django_filters.FilterSet):
    """Quick filter for common searches"""
    
    search = django_filters.CharFilter(
        method='filter_by_name',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Search students by name...'
        }),
        label='Quick Search'
    )
    
    academic_group = django_filters.ModelChoiceFilter(
        queryset=AcademicGroup.objects.none(),  # Will be set dynamically
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        empty_label="All Groups"
    )
    
    gender = django_filters.ChoiceFilter(
        choices=Student.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        empty_label="All Genders"
    )
    
    class Meta:
        model = Student
        fields = []
    
    def __init__(self, *args, **kwargs):
        """Initialize filter with tutor's assigned groups"""
        assigned_groups = kwargs.pop('assigned_groups', None)
        super().__init__(*args, **kwargs)
        
        if assigned_groups is not None:
            self.filters['academic_group'].queryset = assigned_groups
    
    def filter_by_name(self, queryset, name, value):
        """Filter by first name, last name, or middle name"""
        if value:
            return queryset.filter(
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(middle_name__icontains=value)
            )
        return queryset