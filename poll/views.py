from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CreatePollForm
from .models import Poll

def home(request):
    polls = Poll.objects.all()
    context = {
        'polls' : polls
    }
    return render(request, 'poll/home.html', context)

def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
        'form' : form
    }
    return render(request, 'poll/create.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        elif selected_option == 'option4':
            poll.option_four_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'poll/vote.html', context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    total_votes = poll.option_one_count + poll.option_two_count + poll.option_three_count + poll.option_four_count
    option_one_percentage = (poll.option_one_count // total_votes) * 100
    option_two_percentage = (poll.option_two_count // total_votes) * 100
    option_three_percentage = (poll.option_three_count // total_votes) * 100
    option_four_percentage = (poll.option_four_count // total_votes) * 100

    context = {
        'poll' : poll,
        'option_one_percentage'  : option_one_percentage,
        'option_two_percentage'  : option_two_percentage,
        'option_three_percentage': option_three_percentage,
        'option_four_percentage' : option_four_percentage
    }
    return render(request, 'poll/results.html', context)