"""
This Python module contains code to generate the graph for the Anime Suggestion System.

This file is Copyright (c) 2023 Anubha Joshi, Lisa Ye, Simran Vig, Iris Li
"""
from typing import Any
from python_ta.contracts import check_contracts
import networkx as nx


@check_contracts
def populate_graph(user_to_anime: dict[str, dict[str, float]]) -> nx.Graph:
    """Using the given data, populate the anime graph.

    Preconditions:
        - all(all(0.0 <= user_to_anime[user][anime] <= 1.0 for anime in user_to_anime[user]) for user in user_to_anime)
    """
    anime_graph = nx.Graph()

    for user in user_to_anime:
        # Assign attribute to node indicating that the node is a user
        anime_graph.add_node(user, type='user')
        for anime in user_to_anime[user]:
            # Assign attribute to node indicating that the node is an anime
            anime_graph.add_node(anime, type='anime')
            # Set the weight of the edges as the rating
            anime_graph.add_edge(user, anime, weight=user_to_anime[user][anime])

    return anime_graph


@check_contracts
def add_user_input(graph: nx.Graph, anime_ratings: dict[str, float]) -> None:
    """Add the user and the given anime as nodes to the given graph."""
    graph.add_node('program_user', type='user')
    for anime in anime_ratings:
        graph.add_node(anime, type='anime')
        graph.add_edge('program_user', anime, weight=anime_ratings[anime])


@check_contracts
def get_users_in_cluster(partition: Any, graph: nx.Graph, cluster_num: int) -> list[str]:
    """Return a list of all the users in the same cluster as the program user.

    Preconditions:
        - len(nx.get_node_attributes(graph, 'type')) != 0
    """
    same_cluster = [key for key in partition
                    if partition[key] == cluster_num
                    and get_node_type(graph, key) == 'user']

    return same_cluster


@check_contracts
def get_node_type(graph: nx.Graph, n: str) -> str:
    """Return the type of the given node n.

    Preconditions:
        - len(nx.get_node_attributes(graph, 'type')) != 0
    """
    return graph.nodes[n]['type']


@check_contracts
def get_avg_weight_map(graph: nx.Graph, anime_list: list[str], preferences: dict[str, float],
                       cluster_partition: Any) -> dict[str, float]:
    """Return the predicted anime ratings for the user by averaging the ratings of other users' ratings in the same
    cluster.

    Preconditions:
        - all(anime in anime_list for anime in preferences)
    """
    cluster_num = cluster_partition['program_user']
    same_cluster = get_users_in_cluster(cluster_partition, graph, cluster_num)

    anime_weight_avg = {}

    for anime in anime_list:
        if anime in preferences:  # Check whether this anime already has a rating from the user
            continue

        avg_weight = 0
        for username in graph.neighbors(anime):
            if username == 'program_user' or cluster_partition[username] != cluster_num:
                continue
            avg_weight += get_edge_weight(graph, username, anime)
        avg_weight /= len(same_cluster)
        anime_weight_avg[anime] = avg_weight

    return anime_weight_avg


@check_contracts
def sub_cluster(graph: nx.Graph, same_cluster_users: list[str], suggested_anime: list[str]) -> nx.Graph:
    """Return the cluster that the user is part of with only the suggested anime.

    Preconditions:
        - all(user in graph.nodes for user in same_cluster_users)
        - all(anime in graph.nodes for anime in suggested_anime)
    """
    sub_graph = nx.Graph()

    for anime in suggested_anime:
        sub_graph.add_node(anime, type='anime')

    for username in same_cluster_users:
        if username == 'program_user':
            continue

        sub_graph.add_node(username, type='user')
        for anime in suggested_anime:
            sub_graph.add_edge(username, anime, weight=get_edge_weight(graph, username, anime))

    return sub_graph


@check_contracts
def get_edge_weight(graph: nx.Graph, n1: str, n2: str) -> float:
    """Return the weight of the edge between the given nodes in the graph.

    Preconditions:
        - n1 in neighbours(graph, n2) and n2 in neighbours(graph, n1)
    """
    return graph[n1][n2]['weight']


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],
        'allowed-io': [],
        'max-line-length': 120,
        'disable': ['E9999']
    })
