from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateGameForm, JoinGameForm
from .models import Game, Player

def index(request):
    return render(request, 'index.html')

def how_to_play(request):
    return render(request, 'how_to_play.html')

import random
import string

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def create_game(request):
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.room_code = generate_room_code()  # Generate a unique room code
            game.save()
            return redirect('game_room', room_code=game.room_code)
    else:
        form = CreateGameForm()
    return render(request, 'create_game.html', {'form': form})

def join_game(request):
    if request.method == 'POST':
        form = JoinGameForm(request.POST)
        if form.is_valid():
            room_code = form.cleaned_data['room_code']
            player_name = form.cleaned_data['player_name']
            game = get_object_or_404(Game, room_code=room_code)
            Player.objects.create(game=game, name=player_name)
            return redirect('game_room', room_code)
    else:
        form = JoinGameForm()
    return render(request, 'join_game.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Game, Player
from .utils import check_name, check_place, check_animal, check_movie
from django.http import JsonResponse
def game_room(request, room_code):
    game = get_object_or_404(Game, room_code=room_code)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        animal = request.POST.get('animal')
        movie = request.POST.get('movie')

        # Check the answers
        name_result = check_name(name, game)
        place_result = check_place(place)
        animal_result = check_animal(animal)
        movie_result = check_movie(movie)

        # Store the answers in a dictionary
        results = {
            'name': name_result,
            'place': place_result,
            'animal': animal_result,
            'movie': movie_result,
        }

        # Calculate scores for all players
        players = game.players.all()
        for player in players:
            player_score = 0
            # For each player, check their answers and calculate score
            for category, result in results.items():
                if result['correct']:
                    player_score += 10  # Correct answer
                else:
                    player_score += 5   # Incorrect answer
            player.score = player_score
            player.save()

        # Update the letter after every round
        game.letter = get_random_letter()  # Generate a new random letter
        game.save()  # Save the game with the new letter

        # Pass the new letter to the template
        return render(request, 'game_room.html', {'game': game, 'results': results, 'letter': game.letter})

    # Show the current letter for GET request
    letter = game.letter
    return render(request, 'game_room.html', {'game': game, 'letter': letter})

def check_name(name, game):
    if name:  # Ensure the name is not empty
        return {'correct': name[0].upper() == game.letter}
    return {'correct': False}  # Return False if the name is empty

import random
import string

def get_random_letter():
    return random.choice(string.ascii_uppercase)

def game_list(request):
    games = Game.objects.all()
    return render(request, 'game_list.html', {'games': games})
def player_scores(request, room_code):
    game = get_object_or_404(Game, room_code=room_code)
    players = game.player_set.all()
    return render(request, 'player_scores.html', {'game': game, 'players': players})
