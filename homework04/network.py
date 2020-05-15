import igraph
import requests
import json

from api import get_friends 
from igraph import Graph, plot


def get_network(user_id, iter=20000):
    users_ids, users_names = user_friends(user_id)
    edges = []
    for i in range(len(users_ids)):
        friends_ids = None
        try:
            friends_ids, friends_names = user_friends(users_ids[i])
        except KeyError:
            pass
        if friends_ids is not None:
            for j in range(len(users_ids)):
                if users_ids[j] in friends_ids :
                    edges.append((i, j))
    
    return users_names, edges

def user_friends(user_id):

    ids = []
    names = []
    for user in get_friends(user_id, 'first_name')['response']['items']:        
        ids.append(user['id'])
        names.append(user['first_name'] + ' ' + user['last_name'])
    return ids, names
    
def plot_graph(vertices, edges):
    g = Graph(vertex_attrs={"label": vertices}, edges=edges, directed=False)
    N = len(vertices)
    visual_style = {"layout": g.layout_fruchterman_reingold(maxiter=20000, area=N ** 3, repulserad=N ** 3),
                    "bbox": (1500, 1500), "edge_color": '#A9A9A9', "vertex_label_dist": 1}
    g.simplify(multiple=True, loops=True)
    communities = g.community_fastgreedy()
    clusters = communities.as_clustering()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)


if __name__ == '__main__':
    names, edges = get_network(136054172)
    plot_graph(names, edges)

