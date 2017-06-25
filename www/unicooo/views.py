from django.shortcuts import render


def front_page(request):
    return render(request, "frontpage.html")


def public_activities(request):
    return render(request, "public_activities.html")
