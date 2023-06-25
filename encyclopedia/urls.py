from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_page, name="new-page"),
    path("random", views.random_page, name="random-page"),

    path("<str:article>/edit", views.edit_page, name="edit-page"),
    path("<str:article>", views.article, name="article")
]
