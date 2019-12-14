import igraph
from igraph import Graph, plot
import numpy as np
from typing import List, Tuple
from typing import Optional
import config
from api import get_friends
from api_models import User
from api import get_friends


def get_network(users_ids, as_edgelist=True):
    vertices = set()
    surnames = set()

    for user_id in users_ids:
        vertices.add(user_id)

        friends = get_friends(user_id, '')
        surnames_getting = get_friends(user_id, 'last_name')
        for i in surnames_getting['response']['items']:
            surname = i['last_name']
            surnames.add(surname)

        if not 'error' in friends:
            for user_friend in friends['response']['items']:
                vertices.add(user_friend)
    surnames = [sur for sur in surnames]

    vertices = [vert for vert in vertices]


    if as_edgelist:
        edges = []

        for user_id in vertices:
            friends = get_friends(user_id, '')

            if not 'error' in friends:
                for user_friend in friends['response']['items']:
                    if user_friend in vertices:
                        edges.append((vertices.index(user_id), vertices.index(user_friend)))

        return surnames, edges

    else:
        matrix = [[0 for _ in range(len(vertices))] for _ in range(len(vertices))]

        for user_id in vertices:
            friends = get_friends(user_id)

            if not 'error' in friends:
                for user_friend in friends['response']['items']:
                    if user_friend in vertices:
                        matrix[vertices.index(user_id)][vertices.index(user_friend)] = 1


def plot_graph(graph):
    vertices = graph[0]

    edges = graph[1]

    # Создание графа
    g = Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)

    # Задаем стиль отображения графа
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N ** 3,
        repulserad=N ** 3)

    # Отрисовываем граф
    plot(g, **visual_style)

    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    print(clusters)
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)


user_ids = [150572566]
graph = get_network(user_ids)
plot_graph(graph)
