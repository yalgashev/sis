from django.db import models
from django.utils import timezone


class Admin(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of BigAutoField
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)  # Specify max_length to match your table
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_super_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])


class School(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schools'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_departments_count(self):
        return self.departments.count()


class Department(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    head_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    office_location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departments'
        unique_together = ['school', 'code']

    def __str__(self):
        return f"{self.name} - {self.school.name}"


class AcademicGroup(models.Model):
    STUDY_YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]
    
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    ]
    
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_groups')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='academic_groups')
    group_name = models.CharField(max_length=100)
    study_year = models.IntegerField(choices=STUDY_YEAR_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    academic_year = models.CharField(max_length=20, help_text="e.g., 2024-2025")
    max_students = models.PositiveIntegerField(default=30, help_text="Maximum number of students in this group")
    current_students = models.PositiveIntegerField(default=0, help_text="Current number of enrolled students")
    group_code = models.CharField(max_length=20, blank=True, null=True, help_text="Auto-generated group code")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academic_groups'
        unique_together = ['school', 'department', 'group_name', 'study_year', 'semester', 'academic_year']

    def __str__(self):
        return f"{self.group_name} - {self.get_study_year_display()} {self.get_semester_display()} ({self.academic_year})"
    
    def save(self, *args, **kwargs):
        # Auto-generate group code if not provided
        if not self.group_code:
            year_code = str(self.study_year)
            sem_code = f"S{self.semester}"
            dept_code = self.department.code
            self.group_code = f"{dept_code}-{year_code}{sem_code}-{self.group_name[:3].upper()}"
        super().save(*args, **kwargs)
    
    def get_available_slots(self):
        """Return available student slots in this group"""
        return self.max_students - self.current_students
    
    def is_full(self):
        """Check if the group is at maximum capacity"""
        return self.current_students >= self.max_students


class Tutor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255, help_text="Temporary password for first login")
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    assigned_groups = models.ManyToManyField(
        AcademicGroup, 
        related_name='tutors', 
        blank=True,
        help_text="Academic groups this tutor is responsible for"
    )
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tutors'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_full_name(self):
        """Return the tutor's full name"""
        return f"{self.first_name} {self.last_name}"

    def get_assigned_groups_count(self):
        """Return number of assigned groups"""
        return self.assigned_groups.count()

    def get_total_students(self):
        """Return total number of students across all assigned groups"""
        return sum(group.current_students for group in self.assigned_groups.filter(is_active=True))

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])


class Student(models.Model):
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    NATION_CHOICES = [
        ('uzbek', 'Uzbek'),
        ('russian', 'Russian'),
        ('tajik', 'Tajik'),
        ('kazakh', 'Kazakh'),
        ('kyrgyz', 'Kyrgyz'),
        ('karakalpak', 'Karakalpak'),
        ('tatar', 'Tatar'),
        ('korean', 'Korean'),
        ('other', 'Other'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    # Primary Information
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    academic_group = models.ForeignKey(AcademicGroup, on_delete=models.CASCADE, related_name='students')
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    nation = models.CharField(max_length=50, choices=NATION_CHOICES, default='uzbek', blank=True)
    id_card = models.CharField(max_length=20, blank=True, null=True, help_text="ID Card number (e.g., AD4843147)")
    home_address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='single', blank=True)
    
    # Family Status
    is_from_large_family = models.BooleanField(default=False)
    is_from_low_income_family = models.BooleanField(default=False)
    is_from_troubled_family = models.BooleanField(default=False)
    are_parents_deceased = models.BooleanField(default=False)
    are_parents_divorced = models.BooleanField(default=False, help_text="Check if parents are divorced")
    is_father_deceased = models.BooleanField(default=False)
    is_mother_deceased = models.BooleanField(default=False)
    has_disability = models.BooleanField(default=False)
    
    # Father Information
    father_first_name = models.CharField(max_length=100, blank=True, null=True)
    father_last_name = models.CharField(max_length=100, blank=True, null=True)
    father_middle_name = models.CharField(max_length=100, blank=True, null=True)
    father_phone_number = models.CharField(max_length=20, blank=True, null=True)
    father_telegram_username = models.CharField(max_length=100, blank=True, null=True)
    is_father_retired = models.BooleanField(default=False)
    is_father_disabled = models.BooleanField(default=False)
    
    # Mother Information
    mother_first_name = models.CharField(max_length=100, blank=True, null=True)
    mother_last_name = models.CharField(max_length=100, blank=True, null=True)
    mother_middle_name = models.CharField(max_length=100, blank=True, null=True)
    mother_phone_number = models.CharField(max_length=20, blank=True, null=True)
    mother_telegram_username = models.CharField(max_length=100, blank=True, null=True)
    is_mother_retired = models.BooleanField(default=False)
    is_mother_disabled = models.BooleanField(default=False)
    
    # Additional Family Information
    siblings_count = models.PositiveIntegerField(default=0, help_text="Number of siblings")
    children_count = models.PositiveIntegerField(default=0, help_text="Number of children (if married)")
    guardian_name = models.CharField(max_length=200, blank=True, null=True, help_text="Legal guardian full name (if both parents deceased)")
    guardian_phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Guardian phone number")
    
    # Personal Interests & Skills
    hobbies = models.CharField(max_length=200, blank=True, null=True, help_text="Student's hobbies and interests")
    special_skills = models.CharField(max_length=200, blank=True, null=True, help_text="Special skills and talents")
    languages_spoken = models.CharField(max_length=200, blank=True, null=True, help_text="Languages spoken with proficiency level")
    
    # Photo and System Fields
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    # Authentication Fields
    username = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Username for login (uses ID Card)")
    password = models.CharField(max_length=128, blank=True, null=True, help_text="Password for login")
    last_login = models.DateTimeField(blank=True, null=True)
    
    # Code of Ethical Conduct Agreement
    agreed_to_code_of_conduct = models.BooleanField(default=False, help_text="Student has agreed to the Code of Ethical Conduct")
    code_agreement_date = models.DateTimeField(blank=True, null=True, help_text="Date when student agreed to the code")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        return full_name

    def get_full_name(self):
        """Return full name with middle name if available"""
        full_name = f"{self.first_name} {self.last_name}"
        if self.middle_name:
            full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        return full_name
        
    def get_age(self):
        """Calculate and return age"""
        if not self.birthday:
            return "Not provided"
        from datetime import date
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
    
    def set_password(self, raw_password):
        """Set password using Django's password hashing"""
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check password against stored hash"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)
    
    def setup_authentication(self):
        """Setup authentication using ID card as username and password"""
        if self.id_card:
            self.username = self.id_card
            if not self.password:  # Only set initial password if not already set
                self.set_password(self.id_card)
    
    def save(self, *args, **kwargs):
        """Override save to automatically setup authentication for new students"""
        # If this is a new student (no pk) and has an ID card, setup authentication
        if not self.pk and self.id_card:
            self.setup_authentication()
        super().save(*args, **kwargs)
    
    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])