"""This Python module contains functions for calculations of anime to genre compatibility and
user to genre compatibility.

This file is Copyright (c) 2023 Anubha Joshi, Lisa Ye, Simran Vig, Iris Li

Notes on variable names:
- user_to_rating: a dictionary of username to another dictionary of an anime title to the user's rating
    of that show (as seen in the Data class)
- anime_to_genre: a dictionary of anime title to the list of genres associated with the show (as seen in the Data class)
- anime_user_map: a dictionary mapping of each anime to a list of user's with reviews on that anime
- user_genre_compatibility: dictionary mapping username to a dictionary with key genre and
    value float representing compatibility (obtained from the user_to_genre_compatibility function)
"""
from __future__ import annotations
from python_ta.contracts import check_contracts


@check_contracts
def anime_to_user_list(user_to_rating: dict[str, dict[str, float]]) -> dict[str, list[str]]:
    """Returns the reverse of user_rating_map: returns a dictionary mapping each anime
    to the list of user's that have reviews for that anime.

    Preconditions
        - user_to_rating != {}
    """
    anime_user_map = {}

    for user in user_to_rating:
        animes = user_to_rating[user]
        for anime in animes:
            if anime not in anime_user_map:
                anime_user_map[anime] = []
            anime_user_map[anime].append(user)

    return anime_user_map


@check_contracts
def user_to_genre_compatibility(user_to_rating: dict[str, dict[str, float]],
                                anime_to_genre: dict[str, list[str]], genre: str, username: str) -> float:
    """Returns a float representing the compatibility/affinity of a given user to a given genre.

    Preconditions:
        - user_to_rating != {}
        - anime_to_genre != {}
        - username in user_to_rating
        - all([anime in anime_to_genre for anime in user_to_rating[user]] for user in user_to_rating)

    >>> u_r_m = {'Bob': {'AOT': 3, 'FMAB': 10, 'MP100': 5}}
    >>> a_g = {'AOT': ['Action'], 'FMAB': ['Action'], 'MP100': ['Action', 'Comedy']}
    >>> g = 'Action'
    >>> u = 'Bob'
    >>> user_to_genre_compatibility(u_r_m, a_g, g, u)
    6.0
    """
    ratings = []

    for anime in user_to_rating[username]:
        if anime not in anime_to_genre:
            continue
        if genre in anime_to_genre[anime]:
            ratings.append(user_to_rating[username][anime])

    if not ratings:
        return 0.5

    return sum(ratings) / len(ratings)


@check_contracts
def anime_to_genre_compatibility(anime: str, genre: str, anime_user_map: dict[str, list[str]],
                                 user_genre_compatibility: dict[str, dict[str, float]],
                                 user_to_rating: dict[str, dict[str, float]],
                                 anime_to_genre: dict[str, list[str]]) -> float:
    """Returns a float representing the compatibility/affinity of a given anime to a given genre.

    Preconditions:
        - anime in anime_to_genre
        - genre in anime_to_genre[anime]
        - all(anime in user_to_rating[user] for user in user_to_rating)
    """
    compatibility = []

    if anime not in anime_user_map:
        return 0.5

    for user in anime_user_map[anime]:
        compatibility.append(user_genre_compatibility[user][genre] * user_to_rating[user][anime])

    initial = (sum(compatibility) / len(compatibility)) ** 0.5

    if genre in anime_to_genre:
        initial **= 0.5

    return initial


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E9992', 'E9997']
    })
