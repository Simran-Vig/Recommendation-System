"""This Python module contains the main Data class and is dedicated to storing data
from our anime, genre, and user datasets.

This file is Copyright (c) 2023 Anubha Joshi, Lisa Ye, Simran Vig, Iris Li
"""
from __future__ import annotations
import csv
from python_ta.contracts import check_contracts


@check_contracts
class Data:
    """
    A class whose attributes store dictionaries of anime to genre, genre to anime, and user to anime from the
    inputted csv files.

    Instance Attributes:
    - anime_to_genre: a dictionary of anime title to the list of genres associated with the show
    - genre_to_anime: a dictionary of genre title to the list of animes associated with it
    - user_to_rating: a dictionary of username to another dictionary of an anime title to the user's rating
    of that show

    Representation Invariants:
    - anime titles, genre names and usernames correspond to those on MyAnimeList
    - all(len(self.anime_to_genre[a] > 0) for a in self.anime_to_genre)
    - all(len(self.genre_to_anime[g] > 0) for g in self.genre_to_anime)
    - all([len(self.user_to_rating[u][r]) == 1 for r in self.user_to_rating[u]] for u in self.user_to_rating)
    """
    anime_to_genre: dict[str, list[str]]
    genre_to_anime: dict[str, list[str]]
    user_to_rating: dict[str, dict[str, float]]

    def __init__(self, anime_file='animes.csv', genre_file='genres.csv', user_file='users.csv') -> None:
        """Initializes the Data object with our processed datasets.
        """
        self.anime_to_genre = find_anime_to_genre(anime_file)
        self.genre_to_anime = find_genre_to_anime(genre_file)
        self.user_to_rating = find_user_to_rating(user_file)

    def get_anime_user_dict(self) -> dict[str, list[str]]:
        """Returns a dictionary mapping of each anime to a list of user's with reviews on that anime.

        No preconditions (since it's only self, and any conditions follow as outlined in representation invariants).
        """
        anime_user_map = {}

        for user in self.user_to_rating:
            animes = self.user_to_rating[user]
            for anime in animes:
                if anime not in anime_user_map:
                    anime_user_map[anime] = []
                anime_user_map[anime].append(user)

        return anime_user_map

    def get_top_n_anime_watched(self, n: int) -> list[str]:
        """Returns a list of anime names, of length n, corresponding to the top anime watched (in order from
        best to least).

        Preconditions:
            - n > 0
        """
        anime_user_map = self.get_anime_user_dict()
        anime_watched_map = {anime: len(anime_user_map[anime]) for anime in anime_user_map}
        anime_ordered = sorted(anime_watched_map.items(), key=lambda x: x[1])
        top_anime = [tup[0] for tup in anime_ordered[len(anime_ordered) - n:]]
        top_anime.reverse()
        return top_anime


def find_anime_to_genre(anime_file: str) -> dict[str, list[str]]:
    """Use the given csv file to input a dictionary mapping of anime titles to their associated genres.
    Initialize the returned dictionary as self's anime_to_genre attribute.

    Preconditions:
        - anime_file is valid

    >>> anime_to_genre = find_anime_to_genre('animes.csv')
    >>> 'Action' in anime_to_genre['Shingeki no Kyojin']
    True
    """
    with open(anime_file) as file:
        reader = csv.reader(file)

        csv_array = []

        for row in reader:
            csv_array += [row]

        dict_so_far = {}

        for row in csv_array:
            dict_so_far[row[0]] = [row[x] for x in range(1, len(row))]

        return dict_so_far


def find_genre_to_anime(genre_file: str) -> dict[str, list[str]]:
    """Use the given csv file to input a dictionary mapping of genre titles to their associated animes.
    Initialize the returned dictionary as self's genre_to_anime attribute.

    Preconditions:
        - genre_file is valid

    >>> genre_to_anime_map = find_genre_to_anime('genres.csv')
    >>> 'Fullmetal Alchemist: Brotherhood' in genre_to_anime_map['Action']
    True
    """
    with open(genre_file) as file:
        reader = csv.reader(file)

        csv_array = []

        for row in reader:
            csv_array += [row]

        dict_so_far = {}

        for row in csv_array:
            dict_so_far[row[0]] = [row[x] for x in range(1, len(row))]

        return dict_so_far


def find_user_to_rating(user_file: str) -> dict[str, dict[str, float]]:
    """Use the given csv file to input a dictionary mapping of username to another dictionary,
    which maps each title of the shows they have watched to the user's rating of that show.
    Initialize the returned dictionary as self's user_to_rating attribute

    Preconditions:
        - user_file is valid

    >>> user_to_rating_map = find_user_to_rating('users.csv')
    >>> user_to_rating_map['karthiga']['One Piece'] == 0.9
    True
    """
    with open(user_file) as file:
        reader = csv.reader(file)

        csv_array = []

        for row in reader:
            csv_array += [row]

        dict_so_far = {}

        for row in csv_array:
            dict_so_far[row[0]] = {}
            for i in range(1, len(row) - 1, 2):
                dict_so_far[row[0]][row[i]] = float(row[i + 1]) / 10

        return dict_so_far


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E9992', 'E9997']
    })
