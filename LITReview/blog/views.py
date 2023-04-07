from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db.models import Prefetch

from blog.forms import CreationTicketForm, CreationReviewForm, UserFollowsForm
from blog.models import Ticket, Review, UserFollows


@login_required
def home_page(request):
    subcriber = list(UserFollows.objects.filter(subscriber=request.user).values_list('subscription', flat=True))
    subcriber.append(request.user)
    tickets = (Ticket.objects
               .filter(uploader__username__in=subcriber).order_by('-date_created')
               .prefetch_related(Prefetch('review_set', queryset=Review.objects.order_by('time_created'))).all())
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
            return redirect('post')
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
                if 'image' in request.FILES and image_after != "":
                    default_storage.delete(image_after)
                photo = form.save(commit=False)
                photo.uploader = request.user
                photo.save()
                return redirect('post')

        elif request.method == 'GET':
            form = CreationTicketForm(instance=ticket)
    else:
        return redirect('post')

    return render(request,
                  'blog/modify_ticket.html',
                  {'form': form}
                  )


@login_required
def remove_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.user == ticket.uploader:
        if request.method == 'POST':
            print("OOOOOOOOOOOOOOOOOOOOO", ticket.image.name)
            if ticket.image.name != "" and default_storage.exists(ticket.image.name):
                default_storage.delete(ticket.image.name)
            ticket.delete()
            return redirect('post')
    else:
        return redirect('post')

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
    reviews = Review.objects.get(id=id)
    if request.user == reviews.user:
        if request.method == 'POST':
            reviews.delete()
            return redirect('home')
    else:
        return redirect('home')

    return render(request,
                  'blog/remove_review.html',
                  {'reviews': reviews},
                  )


@login_required
def follows(request):
    form = UserFollowsForm()
    data_subscriber_follows = UserFollows.objects.filter(subscriber=request.user).all()
    data_subscription_follows = UserFollows.objects.filter(subscription=request.user).all()

    if request.method == 'POST':
        form = UserFollowsForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.subscriber = request.user
            form.save()
            return redirect('follows')
    return render(request,
                  "blog/follows.html",
                  {'form': form,
                   'data_subscriber_follows': data_subscriber_follows,
                   'data_subscription_follows': data_subscription_follows}
                  )


@login_required
def unfollows(request, id):
    follows = UserFollows.objects.get(id=id)
    if request.user == follows.subscriber:
        follows.delete()
        return redirect('follows')


@login_required
def creation_ticket_critique(request):
    form_ticket = CreationTicketForm()
    form_review = CreationReviewForm()
    if request.method == 'POST':
        form_ticket = CreationTicketForm(request.POST, request.FILES)
        form_review = CreationReviewForm(request.POST)
        if form_ticket.is_valid() and form_review.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.uploader = request.user
            ticket.save()
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = Ticket.objects.get(id=ticket.id)
            review.save()
            return redirect('post')

    return render(request,
                  "blog/creation_ticket_critique.html",
                  {'form_ticket': form_ticket,
                   'form_review': form_review, }
                  )


@login_required
def post(request):
    tickets = (Ticket.objects
               .filter(uploader=request.user)
               .order_by('-date_created')
               .prefetch_related('review_set').all())

    for ticket in tickets:
        if not ticket.review_set.filter(user=request.user).exists():
            ticket.has_review = False
        else:
            ticket.has_review = True

    return render(request,
                  "blog/post.html",
                  {'tickets': tickets}
                  )
