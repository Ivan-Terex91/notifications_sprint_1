from movies.models import Movie
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import MovieSerializer


class MoviesListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = (AllowAny,)
    queryset = Movie.objects.prefetch_related(
        "genres", "actors", "directors", "writers"
    ).all()
