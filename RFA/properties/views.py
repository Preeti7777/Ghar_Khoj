# properties/views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyImage, Facility, Wishlist
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
                request, 'Your property has been submitted and is pending for review.')
            return redirect('property_list')  # change to your actual URL name

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
    properties = (
        Property.objects
        .filter(status="approved")
        .select_related("owner")
        .prefetch_related("images", "facility")
        .order_by("-created_at")
    )

    # Basic property filters
    property_type = request.GET.get("property_type")
    province = request.GET.get("province")
    district = request.GET.get("district")
    city = request.GET.get("city")
    min_rent = request.GET.get("min_rent")
    max_rent = request.GET.get("max_rent")

    if property_type:
        properties = properties.filter(property_type=property_type)

    if province:
        properties = properties.filter(province__iexact=province)

    if district:
        properties = properties.filter(district__iexact=district)

    if city:
        properties = properties.filter(city__icontains=city)

    if min_rent:
        properties = properties.filter(monthly_rent__gte=min_rent)

    if max_rent:
        properties = properties.filter(monthly_rent__lte=max_rent)

    # Facility filters
    facility_filters = [
        "car_parking",
        "bike_parking",
        "wifi",
        "drinking_water",
        "water_supply_24_7",
        "attached_bathroom",
        "balcony",
        "furnished",
        "cctv",
        "security_guard",
        "pet_allowed",
        "laundry_facility",
        "lift",
        "generator",
    ]

    for facility in facility_filters:
        if request.GET.get(facility):
            properties = properties.filter(**{
                f"facility__{facility}": True
            })

    wishlist_ids = []

    if request.user.is_authenticated:
        wishlist_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list("property_id", flat=True)

    context = {
        "properties": properties,
        "wishlist_ids": wishlist_ids,

        "property_types": Property.PROPERTY_TYPES,

        "selected_property_type": property_type,
        "selected_province": province,
        "selected_district": district,
        "selected_city": city,
        "selected_min_rent": min_rent,
        "selected_max_rent": max_rent,

        "facility_filters": {
            facility: request.GET.get(facility)
            for facility in facility_filters
        },

        "provinces": (
            Property.objects
            .filter(status="approved")
            .values_list("province", flat=True)
            .distinct()
            .order_by("province")
        ),

        "districts": (
            Property.objects
            .filter(status="approved")
            .values_list("district", flat=True)
            .distinct()
            .order_by("district")
        ),
    }

    return render(request, "properties/property_list.html", context)


def property_detail(request, pk):
    property = get_object_or_404(
        Property.objects
        .select_related("owner", "facility")
        .prefetch_related("images"),
        pk=pk,
        status="approved"
    )

    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(
            user=request.user,
            property=property
        ).exists()

    return render(request, "properties/property_detail.html", {
        "property": property,
        "is_wishlisted": is_wishlisted
    })

@login_required
def toggle_wishlist(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    property_obj = get_object_or_404(Property, pk=pk, status="approved")

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        property=property_obj
    )

    if created:
        return JsonResponse({
            "wishlisted": True,
            "message": "Added to wishlist"
        })

    wishlist_item.delete()

    return JsonResponse({
        "wishlisted": False,
        "message": "Removed from wishlist"
    })

@login_required
def wishlist_list(request):
    if request.user.role != "TENANT":
        messages.error(request, "Only tenants can view wishlist.")
        return redirect("property_list")

    wishlist_items = (
        Wishlist.objects
        .filter(user=request.user)
        .select_related("property", "property__owner")
        .prefetch_related("property__images", "property__facility")
        .order_by("-created_at")
    )

    return render(request, "properties/wishlist.html", {
        "wishlist_items": wishlist_items,
    })


@login_required
def remove_from_wishlist(request, pk):
    if request.method == "POST":
        wishlist_item = get_object_or_404(
            Wishlist,
            user=request.user,
            property_id=pk
        )

        wishlist_item.delete()
        messages.success(request, "Property removed from wishlist.")

    return redirect("wishlist_list")