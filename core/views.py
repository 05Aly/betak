import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q

from .models import Property, CustomUser
from .forms import CustomUserCreationForm, PropertyForm
from .decorators import approved_user_required, seller_required

def home_view(request):
    # Only approved properties are shown on the homepage
    properties = Property.objects.filter(waiting_list=False)
    
    # Filter only available for logged-in buyers (or admin)
    is_buyer = request.user.is_authenticated and (request.user.account_type == 'buyer' or request.user.is_superuser)
    
    # Search and Filter Logic
    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_order = request.GET.get('sort', '')

    if is_buyer:
        if search_query:
            properties = properties.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(address__icontains=search_query)
            )
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)
        if sort_order == 'asc':
            properties = properties.order_by('price')
        elif sort_order == 'desc':
            properties = properties.order_by('-price')

    context = {
        'properties': properties,
        'is_buyer': is_buyer,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_order': sort_order,
    }
    return render(request, 'core/home.html', context)

@login_required
@approved_user_required
def property_detail_view(request, pk):
    # Visitors cannot view details unless logged in (handled by @login_required)
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Check if the property is still pending approval (only owner or superuser/admin can see it if pending)
    if property_obj.waiting_list and property_obj.owner != request.user and not request.user.is_superuser:
        messages.warning(request, "هذا العقار قيد المراجعة حالياً من قبل الإدارة.")
        return redirect('home')
        
    context = {
        'property': property_obj,
        'supabase_url': os.getenv('SUPABASE_URL', ''),
        'supabase_anon_key': os.getenv('SUPABASE_ANON_KEY', ''),
    }
    return render(request, 'core/property_detail.html', context)

@login_required
@approved_user_required
@seller_required
def add_property_view(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.waiting_list = True  # Placed on waiting list by default
            property_obj.save()
            messages.success(request, "تمت إضافة عقارك بنجاح، وهو الآن بانتظار مراجعة الإدارة.")
            return redirect('home')
    else:
        form = PropertyForm()
        
    return render(request, 'core/add_property.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # Pending approval by default
            user.save()
            messages.success(request, "تم تسجيل الحساب بنجاح وهو قيد المراجعة حالياً من قبل الإدارة.")
            # Log the user in to show the pending_approval screen
            login(request, user)
            return redirect('pending_approval')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not user.is_approved and not user.is_superuser:
                    return redirect('pending_approval')
                return redirect('home')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "تم تسجيل الخروج بنجاح.")
    return redirect('home')

@login_required
def pending_approval_view(request):
    # If they are already approved, redirect them home
    if request.user.is_approved or request.user.is_superuser:
        return redirect('home')
    return render(request, 'core/pending_approval.html')

@login_required
@staff_member_required
def admin_approvals_view(request):
    # Get all unapproved user accounts (excluding superusers)
    pending_users = CustomUser.objects.filter(is_approved=False, is_superuser=False)
    
    # Get all property offers pending approval
    pending_properties = Property.objects.filter(waiting_list=True)
    
    context = {
        'pending_users': pending_users,
        'pending_properties': pending_properties,
    }
    return render(request, 'core/admin_approvals.html', context)

@login_required
@staff_member_required
def admin_approvals_action_view(request):
    if request.method == 'POST':
        action_type = request.POST.get('action_type')  # 'approve' or 'reject'
        target_type = request.POST.get('target_type')  # 'user' or 'property'
        target_id = request.POST.get('target_id')
        rejection_notes = request.POST.get('rejection_notes', '').strip()
        
        if target_type == 'user':
            user_obj = get_object_or_404(CustomUser, pk=target_id)
            if action_type == 'approve':
                user_obj.is_approved = True
                user_obj.rejection_notes = None
                user_obj.save()
                messages.success(request, f"تمت الموافقة على حساب البائع {user_obj.full_name} وتفعيله.")
            elif action_type == 'reject':
                user_obj.is_approved = False
                user_obj.rejection_notes = rejection_notes if rejection_notes else "تم الرفض من قبل الإدارة"
                user_obj.save()
                messages.warning(request, f"تم رفض حساب البائع {user_obj.full_name} وتسجيل الملاحظات.")
                
        elif target_type == 'property':
            property_obj = get_object_or_404(Property, pk=target_id)
            if action_type == 'approve':
                property_obj.waiting_list = False
                property_obj.rejection_notes = None
                property_obj.save()
                messages.success(request, f"تمت الموافقة على نشر عقار \"{property_obj.title}\" بنجاح.")
            elif action_type == 'reject':
                property_obj.waiting_list = True
                property_obj.rejection_notes = rejection_notes if rejection_notes else "تم الرفض من قبل الإدارة"
                property_obj.save()
                messages.warning(request, f"تم رفض نشر عقار \"{property_obj.title}\" وتسجيل الملاحظات.")
                
    return redirect('admin_approvals')

