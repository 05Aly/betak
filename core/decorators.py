from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def approved_user_required(view_func):
    """
    Decorator that ensures a user is logged in AND is approved by the admin.
    Otherwise redirects them to the pending_approval page.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_approved and not request.user.is_superuser:
            return redirect('pending_approval')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def seller_required(view_func):
    """
    Decorator that ensures a user is a seller.
    Otherwise redirects them to the homepage with an error message.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.account_type != 'seller' and not request.user.is_superuser:
            messages.error(request, "عذراً، هذه الصفحة مخصصة للبائعين فقط.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
