from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone

from .models import Event, Registration


from django.shortcuts import render
from django.utils import timezone

from .models import Event, Registration

def event_list(request):
    """
    A5 Part 2A: Template-based event list + GET filter checkbox show_cancelled.
    """
    show_cancelled = request.GET.get("show_cancelled") == "on"
    if show_cancelled != True:
        events = Event.objects.all().order_by('starts_at').filter(is_cancelled = False)
    else:
        events = Event.objects.all().order_by('starts_at')
    
    return render(request, "conferences/event_list.html", {"show_cancelled": show_cancelled, "events": events})


def registration_form(request):
    """
    A5 Part 2B: 
    Collect validation errors and re-render the form 
    with a list of error messages.
    """
    
    if request.method == "GET":
        return render(request, "conferences/registration_form.html")
    
    errors = []
    data = {}
    
    data["event_id"] = request.POST.get("event_id", "").strip()
    data["attendee_email"] = request.POST.get("attendee_email", "")
    data["checked_in"] = request.POST.get("checked_in") == "on"

    if not data["event_id"]:
        errors.append("Name is required.")

    try:
        data["event_id"] = int(data["event_id"])
    except ValueError:
        errors.append("event_id must be a number")

    if not data["attendee_email"]:
        errors.append("Email is required.")
    
    if "@" not in data["attendee_email"] or "." not in data["attendee_email"]:
        errors.append("Invalid email format")

    if not data["checked_in"]:
        errors.append("Event is required.")
    
    if not errors:
        try:
            event_obj = Event.objects.get(id=data["event_id"])
            if event_obj.is_cancelled:
                errors.append("Event is cancelled")
        except Event.DoesNotExist:
            errors.append("Event not found")

    if errors:
        return render(request, "conferences/registration_form.html", {
            "errors": errors,
            "data": data
        })
    
    registration = Registration.objects.create(
        event=data["event_id"],
        attendee_email=data["attendee_email"],
        checked_in=data["checked_in"],
        registered_at=timezone.now()
    )
    
    return render(request, "conferences/registration_confirmation.html", {"registered_at": timezone.now()})


    