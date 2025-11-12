from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db import transaction
from django.core.paginator import Paginator
from admin_app.models import Tutor, AcademicGroup, Student
from .forms import TutorProfileForm, TutorPasswordChangeForm, StudentForm
from .filters import AdvancedStudentFilter, QuickStudentFilter
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from datetime import datetime


def tutor_dashboard_view(request):
    """Display the tutor dashboard"""
    # Check if tutor is logged in
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('login')
    
    # Get tutor
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found. Please log in again.')
        return redirect('login')
    
    # Get statistics
    assigned_groups = tutor.assigned_groups.filter(is_active=True)
    total_groups = assigned_groups.count()
    total_students = sum(group.current_students for group in assigned_groups)
    
    # Calculate group statistics
    groups_by_year = {}
    for group in assigned_groups:
        year = group.study_year
        if year not in groups_by_year:
            groups_by_year[year] = 0
        groups_by_year[year] += 1
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'total_groups': total_groups,
        'total_students': total_students,
        'assigned_groups': assigned_groups[:5],  # Show first 5 groups
        'groups_by_year': groups_by_year,
    }
    
    return render(request, 'tutors/dashboard.html', context)


def tutor_academic_groups_view(request):
    """Display tutor's assigned academic groups"""
    # Check if tutor is logged in
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get tutor
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found. Please log in again.')
        return redirect('login')
    
    # Get assigned groups
    assigned_groups = tutor.assigned_groups.select_related('school', 'department').filter(is_active=True)
    
    # Apply pagination
    paginator = Paginator(assigned_groups, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'page_obj': page_obj,
        'assigned_groups': page_obj,
    }
    
    return render(request, 'tutors/academic_groups.html', context)


def tutor_group_students_view(request, group_id):
    """Display students in a specific academic group"""
    # Check if tutor is logged in
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get tutor and group
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
        group = get_object_or_404(AcademicGroup, id=group_id)
        
        # Check if tutor has access to this group
        if not tutor.assigned_groups.filter(id=group_id).exists():
            messages.error(request, 'You do not have access to this group.')
            return redirect('tutor_academic_groups')
            
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found. Please log in again.')
        return redirect('login')
    
    # Get students in the group
    students = Student.objects.filter(academic_group=group, is_active=True).order_by('last_name', 'first_name')
    
    # Calculate statistics
    total_students = students.count()
    active_students = total_students  # All students filtered by is_active=True already
    # Note: This model doesn't have gender field, so we'll use nationality statistics instead
    uzbek_count = students.filter(nation='uzbek').count()
    other_nations_count = total_students - uzbek_count
    capacity_percentage = round((total_students / group.max_students * 100)) if group.max_students > 0 else 0
    
    # Apply pagination
    paginator = Paginator(students, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'group': group,
        'students': page_obj,
        'page_obj': page_obj,
        'active_students': active_students,
        'male_count': uzbek_count,  # Using uzbek count instead of male
        'female_count': other_nations_count,  # Using other nations instead of female
        'capacity_percentage': capacity_percentage,
    }
    
    return render(request, 'tutors/group_students.html', context)


def tutor_settings_view(request):
    """Handle tutor settings (profile and password)"""
    # Check if tutor is logged in
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get tutor
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found. Please log in again.')
        return redirect('login')
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'profile':
            profile_form = TutorProfileForm(request.POST, instance=tutor)
            password_form = None
            
            if profile_form.is_valid():
                updated_tutor = profile_form.save()
                # Update session
                request.session['tutor_name'] = f"{updated_tutor.first_name} {updated_tutor.last_name}"
                request.session['tutor_username'] = updated_tutor.username
                messages.success(request, 'Profile updated successfully!')
                return redirect('tutors:settings')
            else:
                messages.error(request, 'Please correct the errors below.')
                
        elif form_type == 'password':
            password_form = TutorPasswordChangeForm(tutor, request.POST)
            profile_form = None
            
            if password_form.is_valid():
                # Update password
                tutor.password = password_form.cleaned_data['new_password']
                tutor.save()
                messages.success(request, 'Password changed successfully!')
                return redirect('tutors:settings')
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = None
        password_form = None
    
    # Initialize forms for GET request or if not submitted
    if profile_form is None:
        profile_form = TutorProfileForm(instance=tutor)
    
    if password_form is None:
        password_form = TutorPasswordChangeForm(tutor)
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    
    return render(request, 'tutors/settings.html', context)


def tutor_add_student_view(request, group_id):
    """Add a new student to the academic group"""
    # Check if tutor is logged in
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get tutor and group
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
        group = get_object_or_404(AcademicGroup, id=group_id)
        
        # Check if tutor has access to this group
        if not tutor.assigned_groups.filter(id=group_id).exists():
            messages.error(request, 'You do not have access to this group.')
            return redirect('tutors:academic_groups')
            
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found. Please log in again.')
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, group=group)
        if form.is_valid():
            student = form.save(commit=False)
            student.academic_group = group
            student.save()
            
            # Update group's current students count
            group.current_students = group.students.filter(is_active=True).count()
            group.save()
            
            messages.success(request, f'Student {student.first_name} {student.last_name} added successfully!')
            return redirect('tutors:group_students', group_id=group.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(group=group)
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'group': group,
        'form': form,
        'action': 'Add',
    }
    
    return render(request, 'tutors/add_edit_student.html', context)


def tutor_edit_student_view(request, student_id):
    """Edit an existing student"""
    # Check if tutor is logged in
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get tutor and student
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
        student = get_object_or_404(Student, id=student_id)
        
        # Check if tutor has access to this student's group
        if not tutor.assigned_groups.filter(id=student.academic_group.id).exists():
            messages.error(request, 'You do not have access to this student.')
            return redirect('tutors:academic_groups')
            
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found. Please log in again.')
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student, group=student.academic_group)
        if form.is_valid():
            updated_student = form.save()
            messages.success(request, f'Student {updated_student.first_name} {updated_student.last_name} updated successfully!')
            return redirect('tutors:group_students', group_id=student.academic_group.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student, group=student.academic_group)
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'student': student,
        'group': student.academic_group,
        'form': form,
        'action': 'Edit',
    }
    
    return render(request, 'tutors/add_edit_student.html', context)


def tutor_view_student_view(request, student_id):
    """View student details"""
    # Check if tutor is logged in
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get tutor and student
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
        student = get_object_or_404(Student, id=student_id)
        
        # Check if tutor has access to this student's group
        if not tutor.assigned_groups.filter(id=student.academic_group.id).exists():
            messages.error(request, 'You do not have access to this student.')
            return redirect('tutors:academic_groups')
            
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found. Please log in again.')
        return redirect('login')
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'student': student,
        'group': student.academic_group,
    }
    
    return render(request, 'tutors/view_student.html', context)


def tutor_logout_view(request):
    """Handle tutor logout"""
    # Clear session
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def tutor_delete_student_view(request, student_id):
    """Delete student"""
    # Check if tutor is logged in
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get tutor and student
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
        student = get_object_or_404(Student, id=student_id)
        
        # Check if tutor has access to this student's group
        if not tutor.assigned_groups.filter(id=student.academic_group.id).exists():
            messages.error(request, 'You do not have access to this student.')
            return redirect('tutors:academic_groups')
            
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found. Please log in again.')
        return redirect('login')
    
    group = student.academic_group
    student_name = f"{student.first_name} {student.last_name}"
    
    if request.method == 'POST':
        # Delete the student
        student.delete()
        
        # Update group's current students count
        group.current_students = group.students.filter(is_active=True).count()
        group.save()
        
        messages.success(request, f'Student {student_name} has been deleted successfully!')
        return redirect('tutors:group_students', group_id=group.id)
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'student': student,
        'group': group,
    }
    
    return render(request, 'tutors/delete_student.html', context)


def tutor_reports_view(request):
    """Student reports page with comprehensive field filtering"""
    # Check if tutor is logged in
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    # Get tutor
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found. Please log in again.')
        return redirect('login')
    
    # Get tutor's assigned groups
    assigned_groups = tutor.assigned_groups.filter(is_active=True).order_by('group_name')
    
    # Get selected group (if any)
    selected_group_id = request.GET.get('group')
    selected_group = None
    if selected_group_id and selected_group_id != 'all':
        try:
            selected_group = assigned_groups.get(id=int(selected_group_id))
        except (ValueError, AcademicGroup.DoesNotExist):
            selected_group = None
    
    # Get students queryset based on group selection
    if selected_group:
        students_queryset = Student.objects.filter(
            academic_group=selected_group,
            is_active=True
        ).select_related(
            'academic_group',
            'academic_group__department',
            'academic_group__school'
        ).order_by('last_name', 'first_name')
    else:
        students_queryset = Student.objects.filter(
            academic_group__in=assigned_groups,
            is_active=True
        ).select_related(
            'academic_group',
            'academic_group__department',
            'academic_group__school'
        ).order_by('academic_group__group_name', 'last_name', 'first_name')
    
    # Define all available fields organized by categories
    FIELD_CATEGORIES = {
        'Academic Information': {
            'group_name': 'Group Name',
            'department': 'Department',
            'study_year': 'Study Year',
        },
        'Personal Information': {
            'birthday': 'Date of Birth',
            'gender': 'Gender',
            'nation': 'Nationality',
            'id_card': 'ID Card',
            'home_address': 'Home Address',
            'phone_number': 'Phone Number',
            'email': 'Email',
            'telegram_username': 'Telegram Username',
            'marital_status': 'Marital Status',
        },
        'Family Status': {
            'is_from_large_family': 'From Large Family',
            'is_from_low_income_family': 'From Low Income Family',
            'is_from_troubled_family': 'From Troubled Family',
            'are_parents_deceased': 'Parents Deceased',
            'are_parents_divorced': 'Parents Divorced',
            'is_father_deceased': 'Father Deceased',
            'is_mother_deceased': 'Mother Deceased',
            'has_disability': 'Has Disability',
        },
        'Father Information': {
            'father_first_name': "Father's First Name",
            'father_last_name': "Father's Last Name",
            'father_middle_name': "Father's Middle Name",
            'father_phone_number': "Father's Phone Number",
            'father_telegram_username': "Father's Telegram Username",
            'is_father_retired': 'Father Retired',
            'is_father_disabled': 'Father Disabled',
        },
        'Mother Information': {
            'mother_first_name': "Mother's First Name",
            'mother_last_name': "Mother's Last Name",
            'mother_middle_name': "Mother's Middle Name",
            'mother_phone_number': "Mother's Phone Number",
            'mother_telegram_username': "Mother's Telegram Username",
            'is_mother_retired': 'Mother Retired',
            'is_mother_disabled': 'Mother Disabled',
        },
        'Additional Family Information': {
            'siblings_count': 'Number of Siblings',
            'children_count': 'Number of Children',
        },
        'Personal Interests': {
            'hobbies': 'Hobbies and Interests',
            'special_skills': 'Special Skills and Talents',
            'languages_spoken': 'Languages Spoken',
        },
        'System/Agreement Fields': {
            'agreed_to_code_of_conduct': 'Agreed to Code of Conduct',
            'code_agreement_date': 'Date of Agreement',
        }
    }
    
    # Get selected fields from request
    selected_fields = []
    for category, fields in FIELD_CATEGORIES.items():
        for field_name, field_label in fields.items():
            if request.GET.get(f'field_{field_name}'):
                selected_fields.append(field_name)
    
    # Format student data for display
    students_data = []
    if request.GET.get('apply_filter') and selected_fields:  # Only process if filter is applied
        for student in students_queryset:
            student_data = {
                'id': student.id,
                'full_name': student.get_full_name(),
                'group_name': student.academic_group.group_name,
            }
            
            # Add selected fields with proper formatting
            for field in selected_fields:
                if field == 'group_name':
                    value = student.academic_group.group_name
                elif field == 'department':
                    value = student.academic_group.department.name if student.academic_group.department else 'Not provided'
                elif field == 'study_year':
                    value = student.academic_group.get_study_year_display() if student.academic_group.study_year else 'Not provided'
                elif field == 'birthday':
                    value = student.birthday.strftime('%d/%m/%Y') if student.birthday else 'Not provided'
                elif field == 'code_agreement_date':
                    value = student.code_agreement_date.strftime('%d/%m/%Y') if student.code_agreement_date else 'Not provided'
                elif field.startswith('is_') or field.startswith('are_') or field.startswith('has_') or field == 'agreed_to_code_of_conduct':
                    # Boolean fields
                    field_value = getattr(student, field, False)
                    value = 'Yes' if field_value else 'No'
                elif field == 'gender':
                    value = student.get_gender_display() if student.gender else 'Not provided'
                elif field == 'nation':
                    value = student.get_nation_display() if student.nation else 'Not provided'
                elif field == 'marital_status':
                    value = student.get_marital_status_display() if student.marital_status else 'Not provided'
                else:
                    # Text and number fields
                    field_value = getattr(student, field, None)
                    if field_value is None or field_value == '':
                        value = 'Not provided'
                    else:
                        value = str(field_value)
                
                student_data[field] = value
            
            students_data.append(student_data)
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'assigned_groups': assigned_groups,
        'selected_group': selected_group,
        'field_categories': FIELD_CATEGORIES,
        'selected_fields': selected_fields,
        'students_data': students_data,
        'total_students': len(students_data),
        'filter_applied': request.GET.get('apply_filter', False),
    }
    
    return render(request, 'tutors/reports.html', context)