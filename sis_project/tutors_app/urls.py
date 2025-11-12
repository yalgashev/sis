from django.urls import path
from . import views

app_name = 'tutors'

urlpatterns = [
    # Tutor dashboard URLs
    path('dashboard/', views.tutor_dashboard_view, name='dashboard'),
    path('academic-groups/', views.tutor_academic_groups_view, name='academic_groups'),
    path('groups/<int:group_id>/students/', views.tutor_group_students_view, name='group_students'),
    path('reports/', views.tutor_reports_view, name='reports'),
    path('settings/', views.tutor_settings_view, name='settings'),
    path('logout/', views.tutor_logout_view, name='logout'),
    
    # Student management URLs
    path('groups/<int:group_id>/add-student/', views.tutor_add_student_view, name='add_student'),
    path('students/<int:student_id>/edit/', views.tutor_edit_student_view, name='edit_student'),
    path('students/<int:student_id>/', views.tutor_view_student_view, name='view_student'),
    path('students/<int:student_id>/delete/', views.tutor_delete_student_view, name='delete_student'),
]