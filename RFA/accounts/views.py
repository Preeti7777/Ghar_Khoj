from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from properties.models import Property, Wishlist
from .models import User
from .forms import ProfileUpdateForm, UserRegistrationForm, LoginForm


def register_view(request):

    if request.method == 'POST':

        form = UserRegistrationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('property_list')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileUpdateForm(instance=user)
    my_properties = (
        Property.objects
        .filter(owner=user)
        .prefetch_related("images", "facility")
        .order_by("-created_at")
    )

    approved_count = my_properties.filter(status="approved").count()
    pending_count = my_properties.filter(status="pending").count()
    rejected_count = my_properties.filter(status="rejected").count()

    wishlist_items = (
        Wishlist.objects
        .filter(user=user)
        .select_related("property")
        .prefetch_related("property__images")
        .order_by("-created_at")
    )

    context = {
        "profile_user": user,
        "my_properties": my_properties[:5],
        "approved_count": approved_count,
        "pending_count": pending_count,
        "rejected_count": rejected_count,
        "total_listings": my_properties.count(),
        "wishlist_items": wishlist_items[:5],
        "wishlist_count": wishlist_items.count(),
    }

    return render(request, "accounts/profile.html", {**context, "form": form})