from django.urls import path
from . import views

app_name = "collection"

urlpatterns = [
    path("", views.home, name = "home"),
    path("games/", views.game_list, name = "game_list"),
    path(
        "games/add/",
        views.game_create,
        name = "game_create"
    ),
    path(
        "collection-items/<int:collection_item_id>/edit/",
        views.collection_item_edit,
        name = "game_edit"
    ),
    path(
        "collection-items/<int:collection_item_id>/delete/",
        views.collection_item_delete,
        name = "game_confirm_delete"
    )
]
