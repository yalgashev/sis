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
    """Advanced reports page with filtering and export functionality"""
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
    
    # Get all students from tutor's assigned groups
    assigned_groups = tutor.assigned_groups.filter(is_active=True)
    students_queryset = Student.objects.filter(
        academic_group__in=assigned_groups
    ).select_related(
        'academic_group',
        'academic_group__department',
        'academic_group__school'
    ).order_by('last_name', 'first_name')
    
    # Apply filters
    filter_type = request.GET.get('filter_type', 'quick')
    
    if filter_type == 'advanced':
        student_filter = AdvancedStudentFilter(
            request.GET, 
            queryset=students_queryset,
            assigned_groups=assigned_groups
        )
    else:
        student_filter = QuickStudentFilter(
            request.GET, 
            queryset=students_queryset,
            assigned_groups=assigned_groups
        )
    
    filtered_students = student_filter.qs
    
    # Pagination
    page_size = request.GET.get('page_size', '25')
    try:
        page_size = int(page_size)
        if page_size not in [10, 25, 50, 100]:
            page_size = 25
    except ValueError:
        page_size = 25
    
    paginator = Paginator(filtered_students, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_students = filtered_students.count()
    total_groups = assigned_groups.count()
    
    # Gender statistics
    gender_stats = {
        'male': filtered_students.filter(gender='male').count(),
        'female': filtered_students.filter(gender='female').count(),
        'not_specified': filtered_students.filter(gender__isnull=True).count() + filtered_students.filter(gender='').count()
    }
    
    # Family status statistics
    family_stats = {
        'large_family': filtered_students.filter(is_from_large_family=True).count(),
        'low_income': filtered_students.filter(is_from_low_income_family=True).count(),
        'troubled_family': filtered_students.filter(is_from_troubled_family=True).count(),
        'parents_deceased': filtered_students.filter(are_parents_deceased=True).count(),
        'parents_divorced': filtered_students.filter(are_parents_divorced=True).count(),
        'has_disability': filtered_students.filter(has_disability=True).count(),
    }
    
    # Code of conduct statistics
    code_stats = {
        'agreed': filtered_students.filter(agreed_to_code_of_conduct=True).count(),
        'not_agreed': filtered_students.filter(agreed_to_code_of_conduct=False).count(),
    }
    
    context = {
        'tutor_name': request.session.get('tutor_name'),
        'tutor_username': request.session.get('tutor_username'),
        'tutor': tutor,
        'filter': student_filter,
        'students': page_obj,
        'filter_type': filter_type,
        'total_students': total_students,
        'total_groups': total_groups,
        'gender_stats': gender_stats,
        'family_stats': family_stats,
        'code_stats': code_stats,
        'page_size': page_size,
        'page_sizes': [10, 25, 50, 100],
        'current_filters': request.GET.urlencode(),
    }
    
    return render(request, 'tutors/advanced_reports.html', context)


def export_filtered_students(request):
    """Export filtered students to Excel with all information"""
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
        assigned_groups = tutor.assigned_groups.filter(is_active=True)
        
        # Get the same filtered queryset as in reports view
        students_queryset = Student.objects.filter(
            academic_group__in=assigned_groups
        ).select_related(
            'academic_group',
            'academic_group__department',
            'academic_group__school'
        ).order_by('last_name', 'first_name')
        
        # Apply the same filters
        filter_type = request.GET.get('filter_type', 'quick')
        if filter_type == 'advanced':
            student_filter = AdvancedStudentFilter(
                request.GET, 
                queryset=students_queryset,
                assigned_groups=assigned_groups
            )
        else:
            student_filter = QuickStudentFilter(
                request.GET, 
                queryset=students_queryset,
                assigned_groups=assigned_groups
            )
        
        students = student_filter.qs
        
        # Create workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Student Report"
        
        # Define comprehensive headers
        headers = [
            "No.", "Student ID", "Full Name", "First Name", "Last Name", "Middle Name",
            "Birthday", "Age", "Gender", "Nation", "ID Card", "Phone", "Email", "Telegram",
            "Home Address", "Marital Status", "Group", "Department", "Study Year", "Semester",
            "Large Family", "Low Income", "Troubled Family", "Parents Deceased", "Parents Divorced",
            "Father Deceased", "Mother Deceased", "Has Disability", "Father Name", "Father Phone",
            "Father Retired", "Father Disabled", "Mother Name", "Mother Phone", "Mother Retired",
            "Mother Disabled", "Siblings Count", "Children Count", "Guardian Name", "Guardian Phone",
            "Hobbies", "Special Skills", "Languages", "Code Agreement", "Agreement Date",
            "Active", "Created Date", "Last Updated"
        ]
        
        # Style headers
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Apply header styles
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = border
        
        # Add data rows
        for row_num, student in enumerate(students, 2):
            # Calculate age
            age = student.get_age() if student.birthday else "N/A"
            
            # Father full name
            father_name = ""
            if student.father_first_name or student.father_last_name:
                father_parts = [student.father_first_name, student.father_middle_name, student.father_last_name]
                father_name = " ".join([part for part in father_parts if part])
            
            # Mother full name
            mother_name = ""
            if student.mother_first_name or student.mother_last_name:
                mother_parts = [student.mother_first_name, student.mother_middle_name, student.mother_last_name]
                mother_name = " ".join([part for part in mother_parts if part])
            
            row_data = [
                row_num - 1,  # No.
                student.student_id or "N/A",
                student.get_full_name(),
                student.first_name,
                student.last_name,
                student.middle_name or "",
                student.birthday.strftime("%Y-%m-%d") if student.birthday else "N/A",
                age,
                student.get_gender_display() if student.gender else "N/A",
                student.get_nation_display() if student.nation else "N/A",
                student.id_card or "N/A",
                student.phone_number or "N/A",
                student.email or "N/A",
                student.telegram_username or "N/A",
                student.home_address or "N/A",
                student.get_marital_status_display() if student.marital_status else "N/A",
                str(student.academic_group),
                student.academic_group.department.name,
                student.academic_group.get_study_year_display(),
                student.academic_group.get_semester_display(),
                "Yes" if student.is_from_large_family else "No",
                "Yes" if student.is_from_low_income_family else "No",
                "Yes" if student.is_from_troubled_family else "No",
                "Yes" if student.are_parents_deceased else "No",
                "Yes" if student.are_parents_divorced else "No",
                "Yes" if student.is_father_deceased else "No",
                "Yes" if student.is_mother_deceased else "No",
                "Yes" if student.has_disability else "No",
                father_name,
                student.father_phone_number or "N/A",
                "Yes" if student.is_father_retired else "No",
                "Yes" if student.is_father_disabled else "No",
                mother_name,
                student.mother_phone_number or "N/A",
                "Yes" if student.is_mother_retired else "No",
                "Yes" if student.is_mother_disabled else "No",
                student.siblings_count,
                student.children_count,
                student.guardian_name or "N/A",
                student.guardian_phone_number or "N/A",
                student.hobbies or "N/A",
                student.special_skills or "N/A",
                student.languages_spoken or "N/A",
                "Yes" if student.agreed_to_code_of_conduct else "No",
                student.code_agreement_date.strftime("%Y-%m-%d %H:%M") if student.code_agreement_date else "N/A",
                "Yes" if student.is_active else "No",
                student.created_at.strftime("%Y-%m-%d"),
                student.updated_at.strftime("%Y-%m-%d")
            ]
            
            for col_num, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_num, column=col_num, value=value)
                cell.border = border
                cell.alignment = Alignment(vertical="center", wrap_text=True)
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)  # Maximum width of 50
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Set row height for header
        ws.row_dimensions[1].height = 30
        
        # Add summary sheet
        summary_ws = wb.create_sheet("Summary")
        summary_ws.append(["Filter Summary"])
        summary_ws.append(["Total Students", len(students)])
        summary_ws.append(["Export Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        summary_ws.append(["Exported by", tutor.get_full_name()])
        
        # Add filter information
        if request.GET:
            summary_ws.append([])
            summary_ws.append(["Applied Filters:"])
            for key, value in request.GET.items():
                if value and key != 'page':
                    summary_ws.append([key.replace('_', ' ').title(), value])
        
        # Style summary sheet
        for row in summary_ws.iter_rows():
            for cell in row:
                cell.font = Font(size=11)
                cell.alignment = Alignment(vertical="center")
        
        # Create response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        filename = f"student_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        wb.save(response)
        return response
        
    except Exception as e:
        messages.error(request, f'Error exporting data: {str(e)}')
        return redirect('tutors:reports')


def export_students_info(request):
    
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
        assigned_groups = tutor.assigned_groups.filter(is_active=True)
        students = Student.objects.filter(academic_group__in=assigned_groups, is_active=True).order_by('last_name', 'first_name')
        
        # Create workbook and worksheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "TALABALAR TO'G'RISIDA MA'LUMOT"
        
        # Define headers in Uzbek with English translations
        headers = [
            "T/R",  # No.
            "F.I.SH",  # Full Name
            "Tug'ilgan sanasi",  # Birthday
            "Jinsi",  # Gender
            "Millati",  # Nationality
            "Manzili",  # Address
            "Telefon raqami",  # Phone
            "Elektron pochta",  # Email
            "Guruhi",  # Group
        ]
        
        # Style headers
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")
        
        # Add student data
        for row, student in enumerate(students, 2):
            ws.cell(row=row, column=1, value=row-1)  # T/R
            ws.cell(row=row, column=2, value=f"{student.last_name} {student.first_name} {student.middle_name or ''}".strip())  # F.I.SH
            ws.cell(row=row, column=3, value=student.birthday.strftime("%d.%m.%Y") if student.birthday else "")  # Tug'ilgan sanasi
            ws.cell(row=row, column=4, value=student.get_gender_display() if student.gender else "")  # Jinsi
            ws.cell(row=row, column=5, value=student.get_nation_display() if student.nation else "")  # Millati
            ws.cell(row=row, column=6, value=student.home_address or "")  # Manzili
            ws.cell(row=row, column=7, value=student.phone_number or "")  # Telefon raqami
            ws.cell(row=row, column=8, value=student.email or "")  # Elektron pochta
            ws.cell(row=row, column=9, value=student.academic_group.group_name if student.academic_group else "")  # Guruhi
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Prepare response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        filename = f"Talabalar_ma'lumotlari_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        wb.save(response)
        return response
        
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found.')
        return redirect('login')


def export_parents_info(request):
    """Export OTA-ONALAR TO'G'RISIDA MA'LUMOT (Parents Information)"""
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
        assigned_groups = tutor.assigned_groups.filter(is_active=True)
        students = Student.objects.filter(academic_group__in=assigned_groups, is_active=True).order_by('last_name', 'first_name')
        
        # Create workbook and worksheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "OTA-ONALAR TO'G'RISIDA MA'LUMOT"
        
        # Define headers in Uzbek
        headers = [
            "T/R",  # No.
            "Talaba F.I.SH",  # Student Full Name
            "Ota F.I.SH",  # Father Full Name
            "Ota telefoni",  # Father Phone
            "Ona F.I.SH",  # Mother Full Name
            "Ona telefoni",  # Mother Phone
            "Vasiy F.I.SH",  # Guardian Full Name
            "Vasiy telefoni",  # Guardian Phone
            "Farzandlar soni",  # Number of Children
            "Aka-uka soni",  # Number of Siblings
            "Guruhi",  # Group
        ]
        
        # Style headers
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")
        
        # Add student data
        for row, student in enumerate(students, 2):
            ws.cell(row=row, column=1, value=row-1)  # T/R
            ws.cell(row=row, column=2, value=f"{student.last_name} {student.first_name} {student.middle_name or ''}".strip())  # Talaba F.I.SH
            ws.cell(row=row, column=3, value=student.father_name or "")  # Ota F.I.SH
            ws.cell(row=row, column=4, value=student.father_phone_number or "")  # Ota telefoni
            ws.cell(row=row, column=5, value=student.mother_name or "")  # Ona F.I.SH
            ws.cell(row=row, column=6, value=student.mother_phone_number or "")  # Ona telefoni
            ws.cell(row=row, column=7, value=student.guardian_name or "")  # Vasiy F.I.SH
            ws.cell(row=row, column=8, value=student.guardian_phone_number or "")  # Vasiy telefoni
            ws.cell(row=row, column=9, value=student.children_count or "")  # Farzandlar soni
            ws.cell(row=row, column=10, value=student.siblings_count or "")  # Aka-uka soni
            ws.cell(row=row, column=11, value=student.academic_group.group_name if student.academic_group else "")  # Guruhi
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Prepare response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        filename = f"Ota-onalar_ma'lumotlari_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        wb.save(response)
        return response
        
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found.')
        return redirect('login')


def export_social_status(request):
    """Export IJTIMOIY AHVOL (Social Status)"""
    if 'tutor_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    
    try:
        tutor = Tutor.objects.get(id=request.session['tutor_id'])
        assigned_groups = tutor.assigned_groups.filter(is_active=True)
        students = Student.objects.filter(academic_group__in=assigned_groups, is_active=True).order_by('last_name', 'first_name')
        
        # Create workbook and worksheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "IJTIMOIY AHVOL"
        
        # Define headers in Uzbek
        headers = [
            "T/R",  # No.
            "Talaba F.I.SH",  # Student Full Name
            "Qiziqishlari",  # Hobbies/Interests
            "Maxsus ko'nikmalari",  # Special Skills
            "Tillar",  # Languages
            "Ijtimoiy faollik",  # Social Activity
            "Akademik guruh",  # Academic Group
            "Oila ahvoli",  # Family Status
        ]
        
        # Style headers
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")
        
        # Add student data
        for row, student in enumerate(students, 2):
            # Determine family status based on available parent information
            family_status = "To'liq oila"  # Complete family
            if not student.father_name and not student.mother_name:
                family_status = "Yetim"  # Orphan
            elif not student.father_name:
                family_status = "Otasiz"  # Fatherless
            elif not student.mother_name:
                family_status = "Onasiz"  # Motherless
            
            ws.cell(row=row, column=1, value=row-1)  # T/R
            ws.cell(row=row, column=2, value=f"{student.last_name} {student.first_name} {student.middle_name or ''}".strip())  # Talaba F.I.SH
            ws.cell(row=row, column=3, value=student.hobbies or "")  # Qiziqishlari
            ws.cell(row=row, column=4, value=student.special_skills or "")  # Maxsus ko'nikmalari
            ws.cell(row=row, column=5, value=student.languages_spoken or "")  # Tillar
            ws.cell(row=row, column=6, value=student.social_media_activity or "")  # Ijtimoiy faollik
            ws.cell(row=row, column=7, value=student.academic_group.group_name if student.academic_group else "")  # Akademik guruh
            ws.cell(row=row, column=8, value=family_status)  # Oila ahvoli
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Prepare response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        filename = f"Ijtimoiy_ahvol_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        wb.save(response)
        return response
        
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found.')
        return redirect('login')
