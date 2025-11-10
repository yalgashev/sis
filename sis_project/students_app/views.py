from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import sys
import os
from admin_app.models import Student
from .forms import (
    StudentPersonalDataForm, StudentContactInfoForm, 
    StudentFamilyInfoForm, StudentAdditionalInfoForm,
    StudentPasswordChangeForm
)

# Add project root to path for importing code_content
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code_content import get_code_content


def student_dashboard_view(request):
    """Main student dashboard"""
    # Check if student is logged in
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to access your dashboard.')
        return redirect('login')
    
    # Get student
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('login')
    
    # Calculate completion percentage
    completion_stats = get_completion_stats(student)
    
    context = {
        'student_name': request.session.get('student_name'),
        'student_username': request.session.get('student_username'),
        'student': student,
        'completion_stats': completion_stats,
    }
    
    return render(request, 'students/dashboard.html', context)


def student_general_view(request):
    """General information overview"""
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('login')
    
    context = {
        'student_name': request.session.get('student_name'),
        'student_username': request.session.get('student_username'),
        'student': student,
    }
    
    return render(request, 'students/general.html', context)


def student_personal_data_view(request):
    """Personal data management"""
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentPersonalDataForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal data updated successfully!')
            return redirect('students:personal_data')
    else:
        form = StudentPersonalDataForm(instance=student)
    
    context = {
        'student_name': request.session.get('student_name'),
        'student_username': request.session.get('student_username'),
        'student': student,
        'form': form,
    }
    
    return render(request, 'students/personal_data.html', context)


def student_contact_info_view(request):
    """Contact information management"""
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentContactInfoForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact information updated successfully!')
            return redirect('students:contact_info')
    else:
        form = StudentContactInfoForm(instance=student)
    
    context = {
        'student_name': request.session.get('student_name'),
        'student_username': request.session.get('student_username'),
        'student': student,
        'form': form,
    }
    
    return render(request, 'students/contact_info.html', context)


def student_family_info_view(request):
    """Family information management"""
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentFamilyInfoForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family information updated successfully!')
            return redirect('students:family_info')
    else:
        form = StudentFamilyInfoForm(instance=student)
    
    context = {
        'student_name': request.session.get('student_name'),
        'student_username': request.session.get('student_username'),
        'student': student,
        'form': form,
    }
    
    return render(request, 'students/family_info.html', context)


def student_additional_info_view(request):
    """Additional information management - Personal Interests & Skills"""
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentAdditionalInfoForm(request.POST)
        if form.is_valid():
            # Handle hobbies
            hobbies = form.cleaned_data.get('hobbies')
            if hobbies == 'other':
                student.hobbies = form.cleaned_data.get('hobbies_other', '')
            else:
                student.hobbies = hobbies
            
            # Handle special skills
            special_skills = form.cleaned_data.get('special_skills')
            if special_skills == 'other':
                student.special_skills = form.cleaned_data.get('special_skills_other', '')
            else:
                student.special_skills = special_skills
            
            # Handle languages
            languages_spoken = form.cleaned_data.get('languages_spoken')
            if languages_spoken == 'other':
                student.languages_spoken = form.cleaned_data.get('languages_spoken_other', '')
            else:
                student.languages_spoken = languages_spoken
            
            student.save()
            messages.success(request, 'Personal interests & skills updated successfully!')
            return redirect('students:additional_info')
    else:
        # Initialize form with current values
        form = StudentAdditionalInfoForm(initial={
            'hobbies': student.hobbies or '',
            'special_skills': student.special_skills or '',
            'languages_spoken': student.languages_spoken or '',
        })
    
    context = {
        'student_name': request.session.get('student_name'),
        'student_username': request.session.get('student_username'),
        'student': student,
        'form': form,
    }
    
    return render(request, 'students/additional_info.html', context)


def student_change_password_view(request):
    """Change password functionality"""
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentPasswordChangeForm(request.POST, instance=student)
        if form.is_valid():
            # Save new password
            student.set_password(form.cleaned_data['new_password'])
            student.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('students:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentPasswordChangeForm(instance=student)
    
    context = {
        'student_name': request.session.get('student_name'),
        'student_username': request.session.get('student_username'),
        'student': student,
        'form': form,
    }
    
    return render(request, 'students/change_password.html', context)


def student_logout_view(request):
    """Handle student logout"""
    # Clear session
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def get_completion_stats(student):
    """Calculate completion statistics for student profile"""
    total_fields = 0
    completed_fields = 0
    
    # Personal Data (mandatory fields)
    personal_mandatory = ['birthday', 'nation']
    for field in personal_mandatory:
        total_fields += 1
        if getattr(student, field, None):
            completed_fields += 1
    
    # Contact Info (mandatory fields)  
    contact_mandatory = ['phone_number', 'home_address']
    for field in contact_mandatory:
        total_fields += 1
        if getattr(student, field, None):
            completed_fields += 1
    
    # Family Info (mandatory fields)
    family_mandatory = [
        'father_first_name', 'father_last_name', 'father_phone_number',
        'mother_first_name', 'mother_last_name', 'mother_phone_number'
    ]
    for field in family_mandatory:
        total_fields += 1
        if getattr(student, field, None):
            completed_fields += 1
    
    # Additional Info (mandatory fields)
    additional_mandatory = ['marital_status']
    for field in additional_mandatory:
        total_fields += 1
        if getattr(student, field, None) and getattr(student, field) != 'single':
            completed_fields += 1
    
    completion_percentage = (completed_fields / total_fields * 100) if total_fields > 0 else 0
    
    return {
        'total_fields': total_fields,
        'completed_fields': completed_fields,
        'completion_percentage': round(completion_percentage, 1)
    }


def student_code_of_conduct_view(request):
    """Code of Ethical Conduct page"""
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('login')
    
    # Get code content from external file
    code_content = get_code_content()
    
    context = {
        'student_name': request.session.get('student_name'),
        'student_username': request.session.get('student_username'),
        'student': student,
        'code_content': code_content,
        'already_agreed': student.agreed_to_code_of_conduct,
        'agreement_date': student.code_agreement_date,
    }
    
    return render(request, 'students/code_of_conduct.html', context)


@csrf_exempt
@require_POST
def agree_to_code_of_conduct(request):
    """Handle agreement to code of conduct via AJAX"""
    if 'student_id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Not logged in'})
    
    try:
        student = Student.objects.get(id=request.session['student_id'])
        
        # Check if already agreed
        if student.agreed_to_code_of_conduct:
            return JsonResponse({
                'success': False, 
                'error': 'You have already agreed to the code of conduct'
            })
        
        # Update student record
        student.agreed_to_code_of_conduct = True
        student.code_agreement_date = timezone.now()
        student.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Thank you for agreeing to the Code of Ethical Conduct',
            'agreement_date': student.code_agreement_date.strftime('%B %d, %Y at %I:%M %p')
        })
        
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
