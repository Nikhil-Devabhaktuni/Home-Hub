"""
home
"""
from django.contrib import admin
from django.urls import path
from home import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.home_view,name=''),

    path('adminclick', views.adminclick_view),
    path('customerclick', views.customerclick_view),
    path('supervisorclick', views.supervisorclick_view),

    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('supervisorignup', views.supervisor_signup_view,name='supervisorignup'),

    path('customerlogin', LoginView.as_view(template_name='home/customerlogin.html'),name='customerlogin'),
    path('supervisorlogin', LoginView.as_view(template_name='home/supervisorlogin.html'),name='supervisorlogin'),
    path('adminlogin', LoginView.as_view(template_name='home/adminlogin.html'),name='adminlogin'),



    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-customer', views.admin_customer_view,name='admin-customer'),
    path('admin-view-customer',views.admin_view_customer_view,name='admin-view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('admin-add-customer', views.admin_add_customer_view,name='admin-add-customer'),
    path('admin-view-customer-enquiry', views.admin_view_customer_enquiry_view,name='admin-view-customer-enquiry'),
    path('admin-view-customer-invoice', views.admin_view_customer_invoice_view,name='admin-view-customer-invoice'),


    path('admin-request', views.admin_request_view,name='admin-request'),
    path('admin-view-request',views.admin_view_request_view,name='admin-view-request'),
    path('change-status/<int:pk>', views.change_status_view,name='change-status'),
    path('admin-delete-request/<int:pk>', views.admin_delete_request_view,name='admin-delete-request'),
    path('admin-add-request',views.admin_add_request_view,name='admin-add-request'),
    path('admin-approve-request',views.admin_approve_request_view,name='admin-approve-request'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    
    path('admin-view-service-cost',views.admin_view_service_cost_view,name='admin-view-service-cost'),
    path('update-cost/<int:pk>', views.update_cost_view,name='update-cost'),

    path('admin-supervisor', views.admin_supervisor_view,name='admin-supervisor'),
    path('admin-view-supervisor',views.admin_view_supervisor_view,name='admin-view-supervisor'),
    path('delete-supervisor/<int:pk>', views.delete_supervisor_view,name='delete-supervisor'),
    path('update-supervisor/<int:pk>', views.update_supervisor_view,name='update-supervisor'),
    path('admin-add-supervisor',views.admin_add_supervisor_view,name='admin-add-supervisor'),
    path('admin-approve-supervisor',views.admin_approve_supervisor_view,name='admin-approve-supervisor'),
    path('approve-supervisor/<int:pk>', views.approve_supervisor_view,name='approve-supervisor'),
    path('delete-supervisor/<int:pk>', views.delete_supervisor_view,name='delete-supervisor'),
    path('admin-view-supervisor-salary',views.admin_view_supervisor_salary_view,name='admin-view-supervisor-salary'),
    path('update-salary/<int:pk>', views.update_salary_view,name='update-salary'),

    path('admin-supervisor-attendance', views.admin_supervisor_attendance_view,name='admin-supervisor-attendance'),
    path('admin-take-attendance', views.admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance', views.admin_view_attendance_view,name='admin-view-attendance'),
    path('admin-feedback', views.admin_feedback_view,name='admin-feedback'),

    path('admin-report', views.admin_report_view,name='admin-report'),

    path('supervisor-dashboard', views.supervisor_dashboard_view,name='supervisor-dashboard'),
    path('supervisor-work-assigned', views.supervisor_work_assigned_view,name='supervisor-work-assigned'),
    path('supervisor-update-status/<int:pk>', views.supervisor_update_status_view,name='supervisor-update-status'),
    path('supervisor-feedback', views.supervisor_feedback_view,name='supervisor-feedback'),
    path('supervisor-salary', views.supervisor_salary_view,name='supervisor-salary'),
    path('supervisor-profile', views.supervisor_profile_view,name='supervisor-profile'),
    path('edit-supervisor-profile', views.edit_supervisor_profile_view,name='edit-supervisor-profile'),

    path('supervisor-attendance', views.supervisor_attendance_view,name='supervisor-attendance'),



    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customer-request', views.customer_request_view,name='customer-request'),
    path('customer-add-request',views.customer_add_request_view,name='customer-add-request'),

    path('customer-profile', views.customer_profile_view,name='customer-profile'),
    path('edit-customer-profile', views.edit_customer_profile_view,name='edit-customer-profile'),
    path('customer-feedback', views.customer_feedback_view,name='customer-feedback'),
    path('customer-invoice', views.customer_invoice_view,name='customer-invoice'),
    path('customer-view-request',views.customer_view_request_view,name='customer-view-request'),
    path('customer-delete-request/<int:pk>', views.customer_delete_request_view,name='customer-delete-request'),
    path('customer-view-approved-request',views.customer_view_approved_request_view,name='customer-view-approved-request'),
    path('customer-view-approved-request-invoice',views.customer_view_approved_request_invoice_view,name='customer-view-approved-request-invoice'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='home/index.html'),name='logout'),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
]
