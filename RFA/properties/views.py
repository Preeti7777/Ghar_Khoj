# properties/views.py

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyImage, Facility
from .forms import FacilityForm, PropertyForm


@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        facility_form = FacilityForm(request.POST)

        if form.is_valid() and facility_form.is_valid():
            # Save property
            property = form.save(commit=False)
            property.owner = request.user
            property.save()

            # Save facilities
            facility = facility_form.save(commit=False)
            facility.property = property
            facility.save()

            # Save property images
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                PropertyImage.objects.create(
                    property=property,
                    image=image,
                    is_primary=(i == 0)
                )

            messages.success(
                request, 'Your property has been submitted and is pending review.')
            return redirect('dashboard')  # change to your actual URL name

        else:
            messages.error(
                request, 'Please fix the errors below and try again.')

    else:
        form = PropertyForm()
        facility_form = FacilityForm()

    return render(request, 'properties/add_property.html', {
        'form': form,
        'facility_form': facility_form,
    })


def property_list(request):

    properties = Property.objects.filter(
        status='approved'
    )

    return render(
        request,
        'properties/property_list.html',
        {
            'properties': properties
        }
    )


def property_detail(request, pk):

    property = get_object_or_404(
        Property,
        pk=pk,
        status='approved'
    )

    return render(
        request,
        'properties/property_detail.html',
        {
            'property': property
        }
    )
