from django.db import models
from django.db.models import ForeignObject, CharField

class Round(models.Model):
    bet: int = models.PositiveIntegerField(default=0)

class Hand(models.Model):
    round: ForeignObject = models.ForeignKey(Round, on_delete=models.CASCADE)
    cards: CharField = models.CharField(max_length=10)

#from . import card_enums
#
# class Deck(models.Model):
#     def populate(self):
#         if self.card_set.exists():
#             return
#
#         position = 0
#         for suit in card_enums.Suit:
#             for rank in card_enums.Rank:
#                 Card.objects.create(suit=suit, rank=rank, deck=self)
#                 position += 1
#
# class Card(models.Model):
#     suit: int = models.PositiveIntegerField(choices=card_enums.Suit)
#     rank: int = models.PositiveIntegerField(choices=card_enums.Rank)
#     deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
#     position = models.PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return f"{self.get_rank_display()} of {self.get_suit_display()}"

