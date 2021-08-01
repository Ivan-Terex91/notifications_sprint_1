from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MoviesListView

router = DefaultRouter()
router.register("movies", MoviesListView, basename="movies")

urlpatterns = [path("", include(router.urls))]
