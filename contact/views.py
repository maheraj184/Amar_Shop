from django.shortcuts import render
from .models import GroupMember

def contact_us(request):
    members = GroupMember.objects.all()
    return render(request, 'contact/contact_us.html', {'members': members})
