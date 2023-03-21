from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from blog.forms import CreationTicketForm, CreationReviewForm
from blog.models import Ticket, Review


@login_required
def home_page(request):
    tickets = Ticket.objects.prefetch_related('review_set').all()
    for ticket in tickets:
        if not ticket.review_set.filter(user=request.user).exists():
            ticket.has_review = False
        else:
            ticket.has_review = True

    return render(request,
                  "blog/home.html",
                  {'tickets': tickets, }
                  )


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


@login_required
def modify_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    image_after = ticket.image.name
    if request.user == ticket.uploader:
        if request.method == 'POST':
            form = CreationTicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                if 'image' in request.FILES:
                    default_storage.delete(image_after)
                photo = form.save(commit=False)
                photo.uploader = request.user
                photo.save()
                return redirect('home')

        elif request.method == 'GET':
            form = CreationTicketForm(instance=ticket)
    else:
        return redirect('home')

    return render(request,
                  'blog/modify_ticket.html',
                  {'form': form}
                  )


@login_required
def remove_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.user == ticket.uploader:
        if request.method == 'POST':
            if default_storage.exists(ticket.image.name):
                print(ticket.image.name)
                default_storage.delete(ticket.image.name)
            ticket.delete()
            return redirect('home')
    else:
        return redirect('home')

    return render(request,
                  'blog/remove_ticket.html',
                  {'ticket': ticket},
                  )


@login_required
def creation_review(request, id):
    review_exist = Ticket.objects.prefetch_related('review_set').get(id=id)
    if not review_exist.review_set.filter(user=request.user).exists():
        if request.method == 'POST':
            form = CreationReviewForm(request.POST)
            if form.is_valid():
                form_save = form.save(commit=False)
                form_save.user = request.user
                form_save.ticket = Ticket.objects.get(id=id)
                form_save.save()
                return redirect('home')
        else:
            ticket = Ticket.objects.get(id=id)
            form = CreationReviewForm()
    else:
        return redirect('home')
    return render(request,
                  "blog/creation_review.html",
                  {'form': form, 'ticket': ticket}
                  )


@login_required
def modify_review(request, id):
    review = Review.objects.get(id=id)
    if request.user == review.user:
        if request.method == 'POST':
            form = CreationReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('home')

        elif request.method == 'GET':
            form = CreationReviewForm(instance=review)
    else:
        return redirect('home')

    return render(request,
                  'blog/modify_review.html',
                  {'form': form}
                  )


@login_required
def remove_review(request, id):
    review = Review.objects.get(id=id)
    if request.user == review.user:
        if request.method == 'POST':
            review.delete()
            return redirect('home')
    else:
        return redirect('home')

    return render(request,
                  'blog/remove_review.html',
                  {'review': review},
                  )
