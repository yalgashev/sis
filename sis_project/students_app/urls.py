from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Student dashboard URLs
    path('dashboard/', views.student_dashboard_view, name='dashboard'),
    path('general/', views.student_general_view, name='general'),
    path('personal-data/', views.student_personal_data_view, name='personal_data'),
    path('contact-info/', views.student_contact_info_view, name='contact_info'),
    path('family-info/', views.student_family_info_view, name='family_info'),
    path('additional-info/', views.student_additional_info_view, name='additional_info'),
    path('change-password/', views.student_change_password_view, name='change_password'),
    path('code-of-conduct/', views.student_code_of_conduct_view, name='code_of_conduct'),
    path('agree-to-code/', views.agree_to_code_of_conduct, name='agree_to_code'),
    path('logout/', views.student_logout_view, name='logout'),
]