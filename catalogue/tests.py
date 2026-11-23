from django.test import TestCase
from django.utils import timezone

from .forms import GameForm
from .models import Game, Genre

class GameFormTests(TestCase):

    def test_valid_game_form(self):
        """
        A game with only a name should be valid.
        """
        form = GameForm(data={
            "name": "Plunder"
        })

        self.assertTrue(form.is_valid(), form.errors)

        game = form.save()

        self.assertEqual(game.name, "Plunder")
        self.assertEqual(Game.objects.count(), 1)

    def test_valid_complete_game_form(self):
        """
        A complete game with sensible values should be valid.
        """
        form = GameForm(data={
            "name": "Nintendo Monopoly",
            "year_published": 2010,
            "min_players": 2,
            "max_players": 8,
            "play_time_minutes": 75,
            "min_age": 8,
            "complexity": "4.5",
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_name_is_invalid(self):
        """
        A game must have a name.
        """
        form = GameForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_max_players_cannot_be_less_than_min_players(self):
        """
        Maximum players cannot be below minimum players.
        """
        form = GameForm(data={
            "name": "Invalid Game",
            "min_players": 5,
            "max_players": 2,
        })

        self.assertFalse(form.is_valid())
        self.assertIn("max_players", form.errors)

    def test_min_players_must_be_at_least_one(self):
        """
        Minimum players cannot be zero.
        """
        form = GameForm(data={
            "name": "Invalid Game",
            "min_players": 0,
        })

        self.assertFalse(form.is_valid())
        self.assertIn("min_players", form.errors)

    def test_playtime_must_be_positive(self):
        """
        Playtime must be greater than zero.
        """
        form = GameForm(data={
            "name": "Invalid Game",
            "play_time_minutes": 0,
        })

        self.assertFalse(form.is_valid())
        self.assertIn("play_time_minutes", form.errors)

    def test_complexity_must_be_within_range(self):
        """
        Complexity must be between 1.0 and 5.0.
        """
        form = GameForm(data={
            "name": "Invalid Game",
            "complexity": "5.5",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("complexity", form.errors)

    def test_publication_year_cannot_be_in_future(self):
        """
        Publication year cannot exceed the current year.
        """
        future_year = timezone.localdate().year + 1

        form = GameForm(data={
            "name": "Future Game",
            "year_published": future_year,
        })

        self.assertFalse(form.is_valid())
        self.assertIn("year_published", form.errors)

    def test_multiple_genres_can_be_selected(self):
        """
        A game can belong to multiple genres.
        """
        strategy = Genre.objects.get(
            name="Competitive Strategy and Resource Management"
        )

        family = Genre.objects.get(
            name="Family Strategy"
        )

        form = GameForm(data={
            "name": "Catan",
            "genres": [strategy.pk, family.pk],
        })

        self.assertTrue(form.is_valid(), form.errors)

        game = form.save()

        self.assertEqual(game.genres.count(), 2)
        self.assertIn(strategy, game.genres.all())
        self.assertIn(family, game.genres.all())

