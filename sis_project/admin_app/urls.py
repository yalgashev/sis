from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('login/', views.login_view, name='login_submit'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='settings'),
    
    # School management URLs
    path('schools/', views.schools_list_view, name='schools_list'),
    path('schools/add/', views.add_school_view, name='add_school'),
    path('schools/edit/<int:school_id>/', views.edit_school_view, name='edit_school'),
    path('schools/delete/<int:school_id>/', views.delete_school_view, name='delete_school'),
    
    # Academic Groups management URLs
    path('academic-groups/', views.academic_groups_list_view, name='academic_groups_list'),
    path('academic-groups/add/', views.add_academic_group_view, name='add_academic_group'),
    path('academic-groups/edit/<int:group_id>/', views.edit_academic_group_view, name='edit_academic_group'),
    path('academic-groups/delete/<int:group_id>/', views.delete_academic_group_view, name='delete_academic_group'),
    
    # Tutors management URLs
    path('tutors/', views.tutors_list_view, name='tutors_list'),
    path('tutors/add/', views.add_tutor_view, name='add_tutor'),
    path('tutors/edit/<int:tutor_id>/', views.edit_tutor_view, name='edit_tutor'),
    path('tutors/delete/<int:tutor_id>/', views.delete_tutor_view, name='delete_tutor'),
    
    # AJAX URLs
    path('api/departments-by-school/', views.get_departments_by_school, name='get_departments_by_school'),
]