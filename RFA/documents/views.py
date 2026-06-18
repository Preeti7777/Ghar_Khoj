from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


@login_required
def documents_view(request):
    if request.user.role != "LANDLORD":
        messages.error(request, "Only landlords can view verification documents.")
        return redirect("profile")

    return render(request, "documents/documents.html", {
        "profile_user": request.user
    })