from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from catalogue.forms import GameForm
from catalogue.models import Game
from .models import Collection, CollectionItem
from .forms import CollectionItemForm

@login_required
def game_list(request):
    games = CollectionItem.objects.filter(
        collection__user = request.user, # collection owned by logged-in user
        item__game__isnull = False # only games for now
    ).select_related(
        "collection",
        "item",
        "item__game"
    ).prefetch_related(
        "item__game__genres"
    )
    
    return render(
        request,
        "catalogue/game_list.html",
        {"games": games}
    )
    
@login_required
def game_create(request, collection_id):
    collection = get_object_or_404( # a user cannot add a game to another user's collection
        Collection,
        pk = collection_id,
        user = request.user
    )
    
    if request.method == "POST":
        game_form = GameForm(request.POST, request.FILES)
        collection_form = CollectionItemForm(request.POST)

        if game_form.is_valid() and collection_form.is_valid():
            # create a user-owned catalogue entry
            game = game_form.save(commit = False)
            game.created_by = request.user
            game.save()
            game_form.save_m2m()
            
            # create user's collection entry
            collection_item = collection_form.save(commit = False)
            collection_item.item = game
            collection_item.collection = collection
            collection_item.save()
            
            messages.success(
                request,
                f"{game.name} was successfully added to {collection.name}!"
            )
            
            # redirect to collection page
            return redirect("collection:game_list")
        else: # handling of invalid forms
            messages.error(
                request,
                "There was a problem with your submission. Please check the form and try again."
            )
    else: # handling of get requests
        game_form = GameForm()
        collection_form = CollectionItemForm()
        
    return render(
        request,
        "catalogue/game_form.html",
        {
            "game_form": game_form,
            "collection_form": collection_form,
            "collection": collection
        }
    )

@login_required            
def collection_item_edit(request, collection_item_id):
    collection_item = get_object_or_404(
        CollectionItem,
        pk = collection_item_id,
        collection__user = request.user, # a user can only edit their own games
        item__game__isnull = False
    )
    
    if request.method == "POST":
        form = CollectionItemForm(
            request.POST,
            instance = collection_item
        )
        if form.is_valid():
            form.save()
            
            messages.success(
                request,
                f"{collection_item.item.name} was successfully updated!"
            )
            return redirect("collection:game_list")
        else:
            messages.error(
                request,
                "There was a problem with your submission. Please check the form and try again."
            )
    else:
        form = CollectionItemForm(instance = collection_item)

    return render(
        request,
        "catalogue/collection_item_form.html",
        {
            "form": form,
            "collection_item": collection_item
        }
    )
    
@login_required # only authenticated users can access
@require_POST # view only responds to post requests
def collection_item_delete(request, collection_item_id):
    collection_item = get_object_or_404( # makes sure item belongs to logged-in user
        CollectionItem,
        pk = collection_item_id,
        collection__user = request.user,
        item__game__isnull = False
    )
    
    game_name = collection_item.item.name
    collection_name = collection_item.collection.name
    
    collection_item.delete() # delete relationship, not the game itself
    
    messages.success(
        request,
        f"{game_name} was removed from {collection_name}."
    )
    
    return redirect("collection:game_list")