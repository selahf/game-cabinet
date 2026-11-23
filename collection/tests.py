from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages, SUCCESS, ERROR
from django.urls import reverse
from django.http import HttpResponse
from unittest.mock import patch

from catalogue.models import Game
from .models import Collection, CollectionItem

User = get_user_model()

class CollectionViewTests(TestCase):
    def setUp(self):
        self.user = User(
            identifier="testuser",
            name="Test User"
        )
        self.user.set_password("testpassword")
        self.user.save()

        self.other_user = User(
            identifier="otheruser",
            name="Other User"
        )
        self.other_user.set_password("otherpassword")
        self.other_user.save()

        self.collection = Collection.objects.create(
            user=self.user,
            name="Family House"
        )

        self.other_collection = Collection.objects.create(
            user=self.other_user,
            name="College Apartment"
        )

        self.client.force_login(self.user)

    def create_game(self, name="Catan", creator = None):
        """
        Create a game in the catalogue.
        """
        if creator is None:
            creator = self.user
        
        return Game.objects.create(
            name=name,
            created_by = creator
        )

    def create_collection_item(self, collection=None, game=None):
        """
        Add a game to a collection.
        """
        if collection is None:
            collection = self.collection

        if game is None:
            game = self.create_game()

        return CollectionItem.objects.create(
            collection=collection,
            item=game
        )
        
    def test_game_create_success(self):
        response = self.client.post(
            reverse(
                "collection:game_create",
                kwargs={"collection_id": self.collection.pk}
            ),
            data={
                "name": "Catan",
            }
        )

        # the view should redirect to the game list
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse("collection:game_list")
        )

        # the game should exist in the catalogue
        game = Game.objects.get(name="Catan")
        self.assertEqual(game.created_by, self.user)

        # the game should be associated with the correct collection
        collection_item = CollectionItem.objects.get(item=game)
        self.assertEqual(collection_item.collection, self.collection)

        # a success message should be generated
        message_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(message_list), 1)
        self.assertEqual(message_list[0].level, SUCCESS)
        self.assertIn("Catan", str(message_list[0]))
        
    def test_game_create_invalid_form(self):
        with patch(
            "collection.views.render",
            return_value=HttpResponse()
        ):
            response = self.client.post(
                reverse(
                    "collection:game_create",
                    kwargs={"collection_id": self.collection.pk}
                ),
                data={}
            )

        # the form should be rendered again rather than redirected
        self.assertEqual(response.status_code, 200)

        # no game or collection item should have been created
        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(CollectionItem.objects.count(), 0)

        # an error message should be generated
        message_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(message_list), 1)
        self.assertEqual(message_list[0].level, ERROR)
        
    def test_collection_item_edit_success(self):
        game = self.create_game()
        collection_item = self.create_collection_item(game=game)

        response = self.client.post(
            reverse(
                "collection:collection_item_edit",
                kwargs={"collection_item_id": collection_item.pk}
            ),
            data={
                "family_favorite": "on",
                "notes": "We love playing this game!",
            }
        )

        # the view should redirect to the game list
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse("collection:game_list")
        )

        # refresh the object to retrieve its updated database values
        collection_item.refresh_from_db()

        self.assertTrue(collection_item.family_favorite)
        self.assertEqual(
            collection_item.notes,
            "We love playing this game!"
        )

        # a success message should be generated
        message_list = list(get_messages(response.wsgi_request))
        self.assertEqual(message_list[0].level, SUCCESS)
        
    def test_user_cannot_edit_another_users_collection_item(self):
        game = self.create_game(creator = self.other_user)

        other_item = self.create_collection_item(
            collection=self.other_collection,
            game=game
        )

        response = self.client.post(
            reverse(
                "collection:collection_item_edit",
                kwargs={"collection_item_id": other_item.pk}
            ),
            data={
                "family_favorite": "on",
                "notes": "Trying to edit someone else's game.",
            }
        )

        # the user should receive a 404 response
        self.assertEqual(response.status_code, 404)

        # the other user's collection item should remain unchanged
        other_item.refresh_from_db()

        self.assertFalse(other_item.family_favorite)
        self.assertEqual(other_item.notes, "")
        
    def test_collection_item_delete_success(self):
        game = self.create_game()
        collection_item = self.create_collection_item(game=game)

        response = self.client.post(
            reverse(
                "collection:collection_item_delete",
                kwargs={"collection_item_id": collection_item.pk}
            )
        )

        # the view should redirect to the game list
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse("collection:game_list")
        )

        # the collection item should be deleted
        self.assertFalse(
            CollectionItem.objects.filter(pk=collection_item.pk).exists()
        )

        # the underlying catalogue game should still exist
        self.assertTrue(
            Game.objects.filter(pk=game.pk).exists()
        )

        # a success message should be generated
        message_list = list(get_messages(response.wsgi_request))
        self.assertEqual(message_list[0].level, SUCCESS)
        self.assertIn("Catan", str(message_list[0]))
        
    def test_user_cannot_delete_another_users_collection_item(self):
        game = self.create_game(creator = self.other_user)

        other_item = self.create_collection_item(
            collection=self.other_collection,
            game=game
        )

        response = self.client.post(
            reverse(
                "collection:collection_item_delete",
                kwargs={"collection_item_id": other_item.pk}
            )
        )

        self.assertEqual(response.status_code, 404)

        # the collection item should still exist
        self.assertTrue(
            CollectionItem.objects.filter(pk=other_item.pk).exists()
        )

        # the catalogue game should still exist
        self.assertTrue(
            Game.objects.filter(pk=game.pk).exists()
        )
        
    def test_collection_item_delete_requires_post(self):
        game = self.create_game()
        collection_item = self.create_collection_item(game=game)

        response = self.client.get(
            reverse(
                "collection:collection_item_delete",
                kwargs={"collection_item_id": collection_item.pk}
            )
        )

        # get requests should not be allowed
        self.assertEqual(response.status_code, 405)

        # the collection item should still exist
        self.assertTrue(
            CollectionItem.objects.filter(pk=collection_item.pk).exists()
        )
        
    def test_game_management_views_require_login(self):
        game = self.create_game()
        collection_item = self.create_collection_item(game=game)

        # log out the test user
        self.client.logout()

        urls_and_methods = [
            (
                reverse("collection:game_list"),
                "get"
            ),
            (
                reverse(
                    "collection:game_create",
                    kwargs={"collection_id": self.collection.pk}
                ),
                "get"
            ),
            (
                reverse(
                    "collection:collection_item_edit",
                    kwargs={"collection_item_id": collection_item.pk}
                ),
                "get"
            ),
            (
                reverse(
                    "collection:collection_item_delete",
                    kwargs={"collection_item_id": collection_item.pk}
                ),
                "post"
            ),
        ]

        for url, method in urls_and_methods:
            with self.subTest(url=url, method=method):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 302)