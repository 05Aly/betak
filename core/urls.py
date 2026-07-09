from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('property/<int:pk>/', views.property_detail_view, name='property_detail'),
    path('property/add/', views.add_property_view, name='add_property'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pending/', views.pending_approval_view, name='pending_approval'),
    path('admin/approvals/', views.admin_approvals_view, name='admin_approvals'),
    path('admin/approvals/action/', views.admin_approvals_action_view, name='admin_approvals_action'),
]
