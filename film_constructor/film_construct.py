from store.models import Genre, Film
from typing import List

description_delimiter = 1024
actors_delimeter = 5


def add_film(title: str, image: str, rate: str, description: str, genres: List[str], actors: List[str]):
    """
    Add film to database
    :param title: Film title
    :param image: Url to film cover
    :param rate: Rate of film
    :param description: Film description
    :param genres: List of film's genres
    :param actors: List of film's actors
    :return: Database film object (Django orm object)
    """
    # Shorts description
    if len(description) >= description_delimiter:
        description = description[:(description_delimiter - 3)] + '...'
    # Shorts actors
    if len(actors) > actors_delimeter:
        actors = actors[:5]
        actors.append('другие..')

    actors_str = ', '.join(actors)
    film = Film(title=title, image=image, rate=rate, description=description, actors=actors_str)
    film.save()
    # Adding genres to film
    for genre in genres:
        genre_obj = Genre.objects.filter(name=genre)
        if not len(genre_obj):
            genre_obj = Genre(name=genre)
            genre_obj.save()
        else:
            genre_obj = genre_obj[0]

        film.genres.add(genre_obj)

    return film
