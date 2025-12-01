"""
This is the main module for the Anime Suggestion System.

This file is Copyright (c) 2023 Anubha Joshi, Lisa Ye, Simran Vig, Iris Li
"""
from typing import Any
from python_ta.contracts import check_contracts

from CourseProject import visualize
from data_class import Data
import matrices
import graph
import networkx as nx
from community import community_louvain
import pickle
import extract_raw
from visualize import visualize_and_display


@check_contracts
def get_user_preferences() -> dict[str, float]:
    """Ask the user for their anime preferences then return their input."""
    user_preferences = {}
    include_more_ratings = 'yes'
    while include_more_ratings == 'yes':
        anime = input('Name an anime (make sure the name of the anime matches the one registered in MAL):')
        if anime in data.anime_to_genre:  # Check whether the user inputted an anime from the graph
            rating = float(input('What rating, from 0.0 to 1.0, would you give this anime?'))
            while not 0.0 <= rating <= 1.0: # Check whether the user inputted a valid rating
                rating = float(input('Please give a rating from 0.0 to 1.0:'))

            user_preferences[anime] = rating
            include_more_ratings = input('To include more ratings, type "yes". Else, type anything:')

        else:
            print('Please input a valid anime name that is part of the dataset.')

    print('Please wait for the results...')
    return user_preferences


@check_contracts
def get_num_suggestions() -> int:
    """Ask the user for the number of anime suggestions they want then return their input."""
    num_suggestions = 0
    is_valid = False
    while not is_valid:
        num_suggestions = input('How many suggestions would you like? (at least one)')
        if num_suggestions.isnumeric():
            if int(num_suggestions) > 0:
                is_valid = True

    return int(num_suggestions)


@check_contracts
def get_anime_suggestions(data: Data, anime_graph: nx.Graph, partition: Any, preferences: dict[str, float],
                          n: int) -> list[str]:
    """Given the graph and user preferences, print and return the suggested anime for the user."""
    # same_cluster = [key for key in partition
    #                 if partition[key] == partition['program_user']
    #                 and anime_graph.nodes[key]['type'] == 'user']

    # anime_weight_avg = {}
    #
    # for anime in data.anime_to_genre:
    #     if anime in preferences:
    #         continue
    #     avg_weight = 0
    #     for username in same_cluster:
    #         if username == 'program_user':
    #             continue
    #         avg_weight += anime_graph[username][anime]['weight']
    #     avg_weight /= len(same_cluster)
    #     anime_weight_avg[anime] = avg_weight

    anime_weight_avg = graph.get_avg_weight_map(anime_graph, list(data.anime_to_genre.keys()), preferences, partition)

    sorted_weight = [k for k, v in sorted(anime_weight_avg.items(), key=lambda item: item[1])]
    n = min(n, len(sorted_weight))
    top_suggestions = sorted_weight[-n:]
    top_suggestions.reverse()
    return top_suggestions


if __name__ == '__main__':

    #If generating csv directly from kaggle file, uncomment the following line:
    extract_raw.extract_data()

    #Code for populating the Data class attributes for use, can uncomment instead of pickle
    #data = Data('animes.csv', 'genres.csv', 'users.csv')
    with open(r"program_data.pkl", 'rb') as f:
        data = pickle.load(f)

    # Code for the matrix multiplication (not needed since we already generated graph)
    # Can uncomment the code below to use instead of using the pickle files
    # (Uncomment the code opening the pickle files)
    # user_genre = matrices.create_user_genre_matrix(data)
    # genre_anime = matrices.create_genre_anime_matrix(data, user_genre)
    # user_to_anime = matrices.mat_mul_map(user_genre, genre_anime,
    #                                      list(data.anime_to_genre.keys()),
    #                                      data.user_to_rating, 100)
    # anime_graph = graph.populate_graph(user_to_anime)
    #
    with open(r"program_graph.pkl", 'rb') as f:
        anime_graph = pickle.load(f)

    # Ask the user for their anime preferences
    # Uncomment the code below if using the pre-built preferences
    user_preferences = get_user_preferences()

    # Here are some pre-built preferences that you may use instead of building your own
    # user_preferences = {'Hunter x Hunter (2011)': 1.0, 'Yagate Kimi ni Naru': 0.82, 'Psycho-Pass': 0.81,
    #                   'Sword Art Online': 0.35, 'No Game No Life': 0.25, 'Black Clover': 0.5,
    #                   'Gintama': 0.85, 'Kimetsu no Yaiba': 0.62, 'Ansatsu Kyoushitsu': 0.78, 'Angel Beats!': 0.8}

    # user_preferences = {'Sayonara no Asa ni Yakusoku no Hana wo Kazarou': 1.0,
    #                 'Dororo': 0.7, 'Haikyuu!! Karasuno Koukou vs. Shiratorizawa Gakuen Koukou': 0.8,
    #                 'Akame ga Kill!': 0.5, 'Beastars': 0.8, 'Owari no Seraph': 0.6,
    #                 'Mob Psycho 100': 0.9, 'Mob Psycho 100 II': 1.0, 'Promare': 0.8,
    #                 'Shingeki no Kyojin Season 3 Part 2': 1.0, 'Shingeki no Kyojin': 0.8,
    #                 'Shingeki no Kyojin Season 2': 0.7, 'Shingeki no Kyojin Season 3': 0.7,
    #                 'Akatsuki no Yona': 0.75, 'Grand Blue': 0.71, 'Fairy Tail': 0.2,
    #                 'Howl no Ugoku Shiro': 0.8, 'Mimi wo Sumaseba': 0.75, 'Mononoke Hime': 0.85,
    #                 'One Punch Man': 0.85, 'Sword Art Online II': 0.6, 'Sword Art Online': 0.5,
    #                 'No Game No Life': 0.4, 'Kimetsu no Yaiba': 0.7, 'Cardcaptor Sakura': 0.77,
    #                 'Nagi no Asu kara': 0.62, 'Yuri!!! on Ice': 0.6,
    #                 'Gyakkyou Burai Kaiji: Ultimate Survivor': 0.86, 'Nisekoi': 0.36}

    # user_preferences = {'Howl no Ugoku Shiro': 0.95, 'Fullmetal Alchemist: Brotherhood': 0.9,
    #                     'Kimi no Na wa.': 0.9, 'Boku dake ga Inai Machi': 0.5, 'Yakusoku no Neverland': 0.85,
    #                     'Toki wo Kakeru Shoujo': 0.7, 'Sen to Chihiro no Kamikakushi': 0.85, 'Mononoke Hime': 0.8,
    #                     'Hotaru no Haka': 0.7, 'Tonari no Totoro': 0.75, 'Haikyuu!!': 0.75,
    #                     'Haikyuu!! Second Season': 0.8, 'Shingeki no Kyojin': 0.8,
    #                     'Shingeki no Kyojin Season 2': 0.75, 'Shingeki no Kyojin Season 3': 0.6,
    #                     'Shingeki no Kyojin Season 3 Part 2': 0.75, 'Shingeki no Kyojin The Final Season': 0.55,
    #                     'Shingeki no Kyojin The Final Season Part 2': 0.55, 'Boku no Hero Academia': 0.4,
    #                     'Death Parade': 0.3}

    graph.add_user_input(anime_graph, user_preferences)

    partition = community_louvain.best_partition(anime_graph)  # Divide the graph into clusters

    cluster_num = partition['program_user']
    same_cluster = graph.get_users_in_cluster(partition, anime_graph, cluster_num)

    # anime_weight_avg = graph.get_avg_weight_map(anime_graph, list(data.anime_to_genre.keys()),
    #                                             partition, cluster_num)
    # # Ask the user for how many anime suggestions they would like
    num_suggestions = get_num_suggestions()

    top_suggestions = get_anime_suggestions(data, anime_graph, partition, user_preferences, int(num_suggestions))
    print('Top Suggestions for you:')
    for i in range(0, len(top_suggestions)):
        print(str(i+1) + ') '+top_suggestions[i])

    sub_graph = graph.sub_cluster(anime_graph, same_cluster, top_suggestions)

    visualize.visualize_and_display(sub_graph)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],
        'allowed-io': [],
        'max-line-length': 120
    })
