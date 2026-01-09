import copy

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from . import blackjack as blackjack

def home(request) -> HttpResponse:
    return render(request, 'blackjack/home.html', {})

def game(request) -> HttpResponse:
    return render(request, 'blackjack/game.html', {})

class BlackjackGame(APIView):
    @staticmethod
    def get_game(request: Request) -> dict:
        if not request.session.get('game'):
            request.session['game'] = blackjack.new_game().model_dump()
        return request.session['game']

    @staticmethod
    def client_obfuscate(game: blackjack.BlackjackGame) -> dict:
        if game.over and game.player.count <= 21:
            return game.model_dump()
        game_copy = copy.deepcopy(game)
        game_copy.deck = []
        game_copy.dealer.count = 0
        game_copy.dealer.hand[1] = blackjack.unrevealed_card()
        return game_copy.model_dump()

    def get(self, request: Request) -> Response:
        game_session_data = blackjack.load_game(self.get_game(request))
        return Response(self.client_obfuscate(game_session_data))

    def post(self, request: Request):
        game_session_data: dict = self.get_game(request)
        loaded_game = blackjack.load_game(game_session_data)

        action = request.data.get('action')
        if action == "restart":
            request.session['game'] = blackjack.new_game().model_dump()
            return Response()

        updated_game = blackjack.process_game(loaded_game, action)

        client_response = self.client_obfuscate(updated_game)
        request.session['game'] = updated_game.model_dump()

        return Response(client_response)