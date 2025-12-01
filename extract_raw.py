"""
This Python module is dedicated to storing data from our anime, genre, and user datasets.

This file is Copyright (c) 2023 Anubha Joshi, Lisa Ye, Simran Vig, Iris Li
"""
from python_ta.contracts import check_contracts
import python_ta
import doctest
import csv


@check_contracts
def _extract_anime_genre_kaggle(csv_file: str) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[int, str]]:
    """
    The function takes in a csv_file to read, and outputs a tuple of three dictionaries. The first one
    is a mapping of each genre to a list of all animes in the genre. The second dictionary in
    the tuple is a mapping of each anime to a list of genres it falls under. The third dictionary in the
    tuple is a mapping of the id of the anime on MyAnimeList to the anime title.

    Preconditions:
        - csv_file is a valid file name that refers to the kaggle file refered in the report

    >>> tups = _extract_anime_genre_kaggle('anime_kaggle.csv')
    >>> 'Haikyuu!! Second Season' in tups[0]['Comedy']
    True
    >>> 'Comedy' in  tups[1]['Haikyuu!! Second Season']
    True
    >>> tups[2][28891] == 'Haikyuu!! Second Season'
    True
    """

    genre_anime_map = {}
    anime_genre_map = {}
    id_anime_map = {}

    with open(csv_file) as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:
            anime_id = row[0]
            anime_title = row[1]
            genres_str = row[3]
            genres_str = genres_str[2:len(genres_str) - 2]
            genres = genres_str.split("', '")

            for genre in genres:
                if genre not in genre_anime_map:
                    genre_anime_map[genre] = []

                genre_anime_map[genre].append(anime_title)

            anime_genre_map[anime_title] = genres
            id_anime_map[int(anime_id)] = anime_title

    return (genre_anime_map, anime_genre_map, id_anime_map)


@check_contracts
def _extract_user_kaggle(csv_file: str, id_anime_map: dict[int, str]) -> dict[str, dict[str, int]]:
    """
    The function takes in a csv_file to read, and outputs a dictionary that maps each username to a
    dictionary mapping each anime title they watched to their rating.

    Preconditions:
        - csv_file is a valid file name that refers to the kaggle file refered in the report

    >>> tup = _extract_anime_genre_kaggle('anime_kaggle.csv')
    >>> user_map = _extract_user_kaggle('UserAnimeList.csv', tup[2])
    >>> user_map['RedvelvetDaisuki']['Haikyuu!! Second Season'] == 8
    True
    """

    user_anime_rating = {}

    with open(csv_file) as file:
        reader = csv.reader(file)

        next(reader)
        row_count = 0

        for row in reader:

            if row_count == 1000000:
                break

            username = row[0]
            anime_id = int(row[1])
            score = int(row[5])

            if anime_id not in id_anime_map:
                continue

            anime_title = id_anime_map[anime_id]

            if username not in user_anime_rating:
                user_anime_rating[username] = {}

            user_anime_rating[username][anime_title] = score

            row_count += 1

    return user_anime_rating


@check_contracts
def _make_anime_csv(file_name: str, anime_genre_map: dict[str, list[str]]) -> None:
    """
    Generates csv from mapping of anime to genre(s) in the following format and puts it in file_name:
    <anime_name>, <genre_1>, <genre_2>, <genre_3>, ..., <genre_n>

    Preconditions:
        - file_name is a valid name for a csv file
        - anime_genre_map was extracted from the function extract_anime_genre_kaggle()
    """
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        for anime in anime_genre_map:
            row = [anime]
            row.extend(anime_genre_map[anime])
            writer.writerow(row)


@check_contracts
def _make_genre_csv(file_name: str, genre_anime_map: dict[str, list[str]]) -> None:
    """
    Generates csv from mapping of genre to anime(s) in the following format and puts it in file_name:
    <genre_name>, <anime_1>, <anime_2>, <anime_3>, ..., <anime_n>

    Preconditions:
        - file_name is a valid name for a file
        - genre_anime_map was extracted from the function extract_anime_genre_kaggle()
    """
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        for genre in genre_anime_map:
            row = [genre]
            row.extend(genre_anime_map[genre])
            writer.writerow(row)


@check_contracts
def _make_user_csv(file_name: str, user_anime_rating_map: dict[str, dict[str, int]]) -> None:
    """
    Generates csv from mapping of username to anime(s) to rating(s) in the following format and puts it in file_name:
    <username>, <anime_1>, <rating_1>, <anime_2>, <rating_2>, ..., <anime_n>, <rating_n>

    Preconditions:
        - file_name is a valid name for a csv file
        - user_anime_rating_map was extracted from the function extract_anime_genre_kaggle()
    """
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        for user in user_anime_rating_map:
            row = [user]
            for anime in user_anime_rating_map[user]:
                row.extend([anime, user_anime_rating_map[user][anime]])
            writer.writerow(row)


@check_contracts
def extract_data(anime_kaggle_file: str = 'anime_kaggle.csv', user_kaggle_file: str = 'UserAnimeList.csv',
                 anime_file: str = 'animes.csv', genre_file: str = 'genres.csv', user_file: str = 'users.csv') \
        -> None:
    """
    This function calls the above functions to create the apprporiate csv files for the program

    Preconditions
        - anime_file, genre_file, and user_file are valid csv file names to extract the data into
        - anime_kaggle_file and user_kaggle_file refer to the correct kaggle downloaded files from the report
    """

    (genre_anime_map, anime_genre_map, id_anime_map) = _extract_anime_genre_kaggle(anime_kaggle_file)
    user_anime_rating_map = _extract_user_kaggle(user_kaggle_file, id_anime_map)

    _make_anime_csv(anime_file, anime_genre_map)
    _make_genre_csv(genre_file, genre_anime_map)
    _make_user_csv(user_file, user_anime_rating_map)

if __name__ == '__main__':

    extract_data()
    doctest.testmod(verbose=True)

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E9992', 'E9997']
    })
