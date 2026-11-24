from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from catalogue.forms import GameForm
from .models import CollectionItem
from .forms import CollectionItemForm

def home(request):
    return render(request, "home.html")

@login_required
def game_list(request):
    games = CollectionItem.objects.filter(
        collection__user = request.user, # collection owned by logged-in user
        item__game__isnull = False # only games for now
    ).select_related( # performance optimizations
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
def game_create(request):   
    if request.method == "POST":
        game_form = GameForm(request.POST, request.FILES)
        collection_form = CollectionItemForm(request.POST, user = request.user)

        if game_form.is_valid() and collection_form.is_valid():
            # create a user-owned catalogue entry
            game = game_form.save(commit = False)
            game.created_by = request.user
            game.save()
            game_form.save_m2m()
            
            # create user's collection entry
            collection_item = collection_form.save(commit = False)
            collection_item.item = game
            collection_item.save()
            
            messages.success(
                request,
                f"{game.name} was successfully added to {collection_item.collection.name}!"
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
        collection_form = CollectionItemForm(
            user = request.user
        )
        
    return render(
        request,
        "catalogue/game_form.html",
        {
            "game_form": game_form,
            "collection_form": collection_form
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
    
    game = collection_item.item.game
    
    if request.method == "POST":
        game_form = GameForm(
            request.POST,
            request.FILES,
            instance = game
        )
        
        collection_form = CollectionItemForm(
            request.POST,
            instance = collection_item,
            user = request.user
        )
        
        if game_form.is_valid() and collection_form.is_valid():
            game_form.save()
            collection_form.save()
            
            messages.success(
                request,
                f"{game.name} was successfully updated!"
            )
            return redirect("collection:game_list")
        else:
            messages.error(
                request,
                "There was a problem with your submission. Please check the form and try again."
            )
    else:
        game_form = GameForm(instance = game)
        collection_form = CollectionItemForm(instance = collection_item, user = request.user)

    return render(
        request,
        "catalogue/game_edit.html",
        {
            "game_form": game_form,
            "collection_form": collection_form,
            "collection_item": collection_item
        }
    )
    
@login_required # only authenticated users can access
def collection_item_delete(request, collection_item_id):
    collection_item = get_object_or_404( # makes sure item belongs to logged-in user
        CollectionItem,
        pk = collection_item_id,
        collection__user = request.user,
        item__game__isnull = False
    )
    
    if request.method == "POST":
        game_name = collection_item.item.name
        collection_name = collection_item.collection.name
    
        collection_item.delete() # delete relationship, not the game itself
    
        messages.success(
            request,
            f"{game_name} was removed from {collection_name}."
        )
    
        return redirect("collection:game_list")
    
    return render(
        request,
        "catalogue/game_confirm_delete.html",
        {
            "collection_item": collection_item
        }
    )
