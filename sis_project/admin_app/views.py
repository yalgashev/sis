from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction, models
from django.core.paginator import Paginator
from .models import Admin, School, Department, AcademicGroup, Tutor
from .forms import SchoolForm, DepartmentFormSet, AcademicGroupForm, TutorForm
import json


def login_page(request):
    """Display the login page"""
    return render(request, 'login.html')


@csrf_exempt
def login_view(request):
    """Handle login form submission"""
    if request.method == 'POST':
        try:
            # Get data from form submission
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Validate input
            if not username or not password:
                messages.error(request, 'Please fill in all fields.')
                return render(request, 'login.html')
            
            # First try admin login
            try:
                admin = Admin.objects.get(username=username, is_active=True)
                
                # Simple password check (in production, use hashed passwords)
                if admin.password == password:
                    # Store admin info in session
                    request.session['admin_id'] = admin.id
                    request.session['admin_username'] = admin.username
                    request.session['admin_name'] = f"{admin.first_name} {admin.last_name}"
                    request.session['is_super_admin'] = admin.is_super_admin
                    request.session['user_type'] = 'admin'
                    
                    # Update last login
                    admin.update_last_login()
                    
                    # Redirect to admin dashboard
                    return redirect('dashboard')
                else:
                    # Try tutor login if admin password doesn't match
                    tutor_login_attempted = True
                    
            except Admin.DoesNotExist:
                # Admin not found, try tutor login
                tutor_login_attempted = True
            
            # Try tutor login if admin login failed
            if 'tutor_login_attempted' in locals() or True:
                try:
                    tutor = Tutor.objects.get(username=username, is_active=True)
                    
                    # Simple password check (in production, use hashed passwords)
                    if tutor.password == password:
                        # Store tutor info in session
                        request.session['tutor_id'] = tutor.id
                        request.session['tutor_username'] = tutor.username
                        request.session['tutor_name'] = f"{tutor.first_name} {tutor.last_name}"
                        request.session['user_type'] = 'tutor'
                        
                        # Update last login
                        tutor.update_last_login()
                        
                        # Redirect to tutor dashboard
                        return redirect('tutors:dashboard')
                    else:
                        messages.error(request, 'Invalid username or password. Please try again.')
                        
                except Tutor.DoesNotExist:
                    # Try student login if tutor login also failed
                    try:
                        from .models import Student
                        student = Student.objects.get(username=username, is_active=True)
                        
                        # Check password using Django's built-in check
                        if student.check_password(password):
                            # Store student info in session
                            request.session['student_id'] = student.id
                            request.session['student_username'] = student.username
                            request.session['student_name'] = f"{student.first_name} {student.last_name}"
                            request.session['user_type'] = 'student'
                            
                            # Update last login
                            student.update_last_login()
                            
                            # Redirect to student dashboard
                            return redirect('students:dashboard')
                        else:
                            messages.error(request, 'Invalid username or password. Please try again.')
                            
                    except Student.DoesNotExist:
                        messages.error(request, 'Invalid username or password. Please try again.')
                
        except Exception as e:
            messages.error(request, f'Database error: {str(e)}. Please check if the database and admin table exist.')
            
    return render(request, 'login.html')


def dashboard_view(request):
    """Display the admin dashboard"""
    # Check if user is logged in
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('login')
    
    # Get statistics from database
    total_students = sum(group.current_students for group in AcademicGroup.objects.all())
    total_tutors = Tutor.objects.filter(is_active=True).count()
    total_academic_groups = AcademicGroup.objects.count()
    total_schools = School.objects.count()
    
    # Get admin info from session
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'total_students': total_students,
        'total_tutors': total_tutors,
        'total_academic_groups': total_academic_groups,
        'total_schools': total_schools,
    }
    
    return render(request, 'dashboard.html', context)


def logout_view(request):
    """Handle logout"""
    # Clear session
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def settings_view(request):
    """Handle admin settings (profile and password)"""
    # Check if user is logged in
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get current admin
    try:
        admin = Admin.objects.get(id=request.session['admin_id'])
    except Admin.DoesNotExist:
        messages.error(request, 'Admin not found. Please log in again.')
        return redirect('login')
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'profile':
            from .forms import AdminProfileForm
            profile_form = AdminProfileForm(request.POST, instance=admin)
            password_form = None  # We'll initialize empty password form for template
            
            if profile_form.is_valid():
                updated_admin = profile_form.save()
                # Update session with new name
                request.session['admin_name'] = f"{updated_admin.first_name} {updated_admin.last_name}"
                request.session['admin_username'] = updated_admin.username
                messages.success(request, 'Profile updated successfully!')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the errors below.')
                
        elif form_type == 'password':
            from .forms import PasswordChangeForm
            password_form = PasswordChangeForm(admin, request.POST)
            profile_form = None  # We'll initialize empty profile form for template
            
            if password_form.is_valid():
                # Update password
                admin.password = password_form.cleaned_data['new_password']
                admin.save()
                messages.success(request, 'Password changed successfully!')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - initialize empty forms
        profile_form = None
        password_form = None
    
    # Initialize forms for GET request or if not submitted
    if profile_form is None:
        from .forms import AdminProfileForm
        profile_form = AdminProfileForm(instance=admin)
    
    if password_form is None:
        from .forms import PasswordChangeForm
        password_form = PasswordChangeForm(admin)
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'profile_form': profile_form,
        'password_form': password_form,
        'admin': admin,
    }
    
    return render(request, 'settings.html', context)


def schools_list_view(request):
    """Display list of schools"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    schools = School.objects.all().order_by('-created_at')
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'schools': schools,
    }
    
    return render(request, 'schools/schools_list.html', context)


def add_school_view(request):
    """Add new school with departments"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    if request.method == 'POST':
        school_form = SchoolForm(request.POST)
        department_formset = DepartmentFormSet(request.POST)
        
        if school_form.is_valid() and department_formset.is_valid():
            try:
                with transaction.atomic():
                    # Save school
                    school = school_form.save()
                    
                    # Save departments
                    department_formset.instance = school
                    department_formset.save()
                    
                    messages.success(request, f'School "{school.name}" has been created successfully!')
                    return redirect('schools_list')
                    
            except Exception as e:
                messages.error(request, f'Error creating school: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        school_form = SchoolForm()
        department_formset = DepartmentFormSet(initial=[{'is_active': True}])
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'school_form': school_form,
        'department_formset': department_formset,
    }
    
    return render(request, 'schools/add_school.html', context)


def edit_school_view(request, school_id):
    """Edit existing school and departments"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    school = get_object_or_404(School, id=school_id)
    
    if request.method == 'POST':
        school_form = SchoolForm(request.POST, instance=school)
        department_formset = DepartmentFormSet(request.POST, instance=school)
        
        if school_form.is_valid() and department_formset.is_valid():
            try:
                with transaction.atomic():
                    # Save school
                    school = school_form.save()
                    
                    # Save departments
                    department_formset.save()
                    
                    messages.success(request, f'School "{school.name}" has been updated successfully!')
                    return redirect('schools_list')
                    
            except Exception as e:
                messages.error(request, f'Error updating school: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        school_form = SchoolForm(instance=school)
        department_formset = DepartmentFormSet(instance=school)
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'school': school,
        'school_form': school_form,
        'department_formset': department_formset,
    }
    
    return render(request, 'schools/edit_school.html', context)


def delete_school_view(request, school_id):
    """Delete school"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    school = get_object_or_404(School, id=school_id)
    
    if request.method == 'POST':
        try:
            school_name = school.name
            school.delete()
            messages.success(request, f'School "{school_name}" has been deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting school: {str(e)}')
    
    return redirect('schools_list')


# ========== Academic Groups Views ==========

def academic_groups_list_view(request):
    """List all academic groups with pagination and search"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    school_filter = request.GET.get('school', '')
    department_filter = request.GET.get('department', '')
    year_filter = request.GET.get('year', '')
    semester_filter = request.GET.get('semester', '')
    
    # Start with all active academic groups
    academic_groups = AcademicGroup.objects.select_related('school', 'department').all()
    
    # Apply filters
    if search_query:
        academic_groups = academic_groups.filter(
            group_name__icontains=search_query
        )
    
    if school_filter:
        academic_groups = academic_groups.filter(school_id=school_filter)
    
    if department_filter:
        academic_groups = academic_groups.filter(department_id=department_filter)
        
    if year_filter:
        academic_groups = academic_groups.filter(study_year=year_filter)
        
    if semester_filter:
        academic_groups = academic_groups.filter(semester=semester_filter)
    
    # Order by creation date (newest first)
    academic_groups = academic_groups.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(academic_groups, 10)  # 10 groups per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    schools = School.objects.filter(is_active=True).order_by('name')
    departments = Department.objects.filter(is_active=True).order_by('name')
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'page_obj': page_obj,
        'search_query': search_query,
        'schools': schools,
        'departments': departments,
        'selected_school': school_filter,
        'selected_department': department_filter,
        'selected_year': year_filter,
        'selected_semester': semester_filter,
        'study_years': AcademicGroup.STUDY_YEAR_CHOICES,
        'semesters': AcademicGroup.SEMESTER_CHOICES,
    }
    
    return render(request, 'academic_groups/list.html', context)


def add_academic_group_view(request):
    """Add new academic group"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST)
        if form.is_valid():
            try:
                academic_group = form.save()
                messages.success(request, f'Academic Group "{academic_group.group_name}" has been created successfully!')
                return redirect('academic_groups_list')
            except Exception as e:
                messages.error(request, f'Error creating academic group: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AcademicGroupForm()
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'form': form,
    }
    
    return render(request, 'academic_groups/add.html', context)


def edit_academic_group_view(request, group_id):
    """Edit existing academic group"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    academic_group = get_object_or_404(AcademicGroup, id=group_id)
    
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST, instance=academic_group)
        if form.is_valid():
            try:
                academic_group = form.save()
                messages.success(request, f'Academic Group "{academic_group.group_name}" has been updated successfully!')
                return redirect('academic_groups_list')
            except Exception as e:
                messages.error(request, f'Error updating academic group: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AcademicGroupForm(instance=academic_group)
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'form': form,
        'academic_group': academic_group,
    }
    
    return render(request, 'academic_groups/edit.html', context)


def delete_academic_group_view(request, group_id):
    """Delete academic group"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    academic_group = get_object_or_404(AcademicGroup, id=group_id)
    
    if request.method == 'POST':
        try:
            group_name = academic_group.group_name
            academic_group.delete()
            messages.success(request, f'Academic Group "{group_name}" has been deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting academic group: {str(e)}')
    
    return redirect('academic_groups_list')


@csrf_exempt
def get_departments_by_school(request):
    """AJAX view to get departments by school"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            school_id = data.get('school_id')
            
            if school_id:
                departments = Department.objects.filter(
                    school_id=school_id, 
                    is_active=True
                ).values('id', 'name')
                return JsonResponse({
                    'success': True,
                    'departments': list(departments)
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'School ID is required'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# ========== Tutors Views ==========

def tutors_list_view(request):
    """List all tutors with pagination and search"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    school_filter = request.GET.get('school', '')
    department_filter = request.GET.get('department', '')
    
    # Start with all tutors
    tutors = Tutor.objects.prefetch_related('assigned_groups__school', 'assigned_groups__department').all()
    
    # Apply filters
    if search_query:
        tutors = tutors.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
    
    if school_filter:
        tutors = tutors.filter(assigned_groups__school_id=school_filter).distinct()
    
    if department_filter:
        tutors = tutors.filter(assigned_groups__department_id=department_filter).distinct()
    
    # Order by creation date (newest first)
    tutors = tutors.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(tutors, 10)  # 10 tutors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    schools = School.objects.filter(is_active=True).order_by('name')
    departments = Department.objects.filter(is_active=True).order_by('name')
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'page_obj': page_obj,
        'search_query': search_query,
        'schools': schools,
        'departments': departments,
        'selected_school': school_filter,
        'selected_department': department_filter,
    }
    
    return render(request, 'tutors/list.html', context)


def add_tutor_view(request):
    """Add new tutor"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            try:
                tutor = form.save()
                messages.success(request, f'Tutor "{tutor.get_full_name()}" has been created successfully!')
                return redirect('tutors_list')
            except Exception as e:
                messages.error(request, f'Error creating tutor: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TutorForm()
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'form': form,
    }
    
    return render(request, 'tutors/add.html', context)


def edit_tutor_view(request, tutor_id):
    """Edit existing tutor"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    tutor = get_object_or_404(Tutor, id=tutor_id)
    
    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutor)
        if form.is_valid():
            try:
                tutor = form.save()
                messages.success(request, f'Tutor "{tutor.get_full_name()}" has been updated successfully!')
                return redirect('tutors_list')
            except Exception as e:
                messages.error(request, f'Error updating tutor: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TutorForm(instance=tutor)
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin', False),
        'form': form,
        'tutor': tutor,
    }
    
    return render(request, 'tutors/edit.html', context)


def delete_tutor_view(request, tutor_id):
    """Delete tutor"""
    if 'admin_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    tutor = get_object_or_404(Tutor, id=tutor_id)
    
    if request.method == 'POST':
        try:
            tutor_name = tutor.get_full_name()
            tutor.delete()
            messages.success(request, f'Tutor "{tutor_name}" has been deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting tutor: {str(e)}')
    
    return redirect('tutors_list')