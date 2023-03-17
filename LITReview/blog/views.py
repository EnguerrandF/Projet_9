from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from blog.forms import CreationTicketForm
from blog.models import Ticket, Review


@login_required
def home_page(request):
    tickets = Ticket.objects.all()
    return render(request,
                  "blog/home.html",
                  {'tickets': tickets})


@login_required
def creation_ticket(request):
    if request.method == 'POST':
        form = CreationTicketForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            return redirect('home')
    else:
        form = CreationTicketForm()

    return render(request,
                  "blog/creation_ticket.html",
                  {'form': form})
