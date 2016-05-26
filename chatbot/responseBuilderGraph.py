'''
Building responses is too complex. Better to model a conversation as a
graph. Also using pep standard from now on.

Start building all graph methods, then probably abstract them away
with chatbot behavior calls. Will use adjacency list for this.
https://en.wikipedia.org/wiki/Adjacency_list

General graph methods:
adjacent(G, x, y): tests whether there is an edge from the vertices x to y;
neighbors(G, x): lists all vertices y such that there is  edge from vtx x to y;
add_vertex(G, x): adds the vertex x, if it is not there;
remove_vertex(G, x): removes the vertex x, if it is there;
add_edge(G, x, y): adds the edge from the vertices x to y, if it is not there;
remove_edge(G, x, y): removes the edge from  vertices x to y, if it is there;
get_vertex_value(G, x): returns the value associated with the vertex x;
set_vertex_value(G, x, v): sets the value associated with the vertex x to v.
'''


class ResponseBuilderGraph:

    def is_adjacent(self, x, y):
        return

    def add_vertex(self, x):
        return

    def remove_vertex(self, x):
        return
