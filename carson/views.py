from django.shortcuts import render
from carson.models import *

def index(request):
    context = {
        "trusted": Tweet.trusted.all()[:20],
        "untrusted": Tweet.untrusted.all()[:20],
    }
    return render(request, "carson/index.html", context)
