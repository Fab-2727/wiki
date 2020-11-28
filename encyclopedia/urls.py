from django.urls import path

from . import views

urlpatterns = [
    path("main", views.index, name="index"),
    path("main/<str:pageName>", views.getPage, name="getPage"),
    path("search", views.searchForEntry, name="searchForEntry"),
    path("newentry", views.newEntry, name="newEntry"),
    path("editentry/<str:pageName>", views.editEntry, name="editEntry"),
    path("randomentry", views.getRandomEntry, name="getRandomEntry")
]
