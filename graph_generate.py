import networkx as nx
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral4, Spectral8
from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool, BoxZoomTool, ResetTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool)
from bokeh.plotting import from_networkx
from bokeh.io import output_file, output_notebook, show
from itertools import permutations, combinations
import ast
import numpy as np
import pandas as pd
import re

def filter_column(col):
    regex_pattern = re.compile('^[a-zA-Z0-9_.-]*$')
    l = [s for s in col if regex_pattern.match(s)]
    return(l)

df = pd.read_json('data/processed_issues_entities.json')
df['entities_filtered'] = df['entities'].apply(lambda x: filter_column(x))
print(df['entities'])
print(df['entities_filtered'])

g = nx.Graph()
node_weights = {}

for index, row_iter in df.iterrows():
  row = row_iter['entities_filtered']
  row_weights = 1
  if not row:
    print("Empty row", index)
    continue
  #data = ast.literal_eval(row)
  data = row
  comb_list = list(combinations(data, 2))
  for elem in comb_list:
    if(node_weights.get(elem[0])):
        node_weights[elem[0]] += row_weights
    else:
        node_weights[elem[0]] = row_weights
    if(node_weights.get(elem[1])):
        node_weights[elem[1]] += row_weights
    else:
        node_weights[elem[1]] = row_weights

    g.add_edge(elem[0], elem[1])
    if(g[elem[0]][elem[1]].get('edge_weight','NA') == 'NA'):
        g[elem[0]][elem[1]]['edge_weight'] = 1
    else:
        g[elem[0]][elem[1]]['edge_weight'] += 1


pos = nx.random_layout(g)
node_x = []
node_y = []
node_list = []
node_weights_ordered = []

label = {}
for node in g.nodes():
    #print(node, pos[node])
    x, y = pos[node][0], pos[node][1]
    #g.nodes[node[0]]['x'] = x
    #g.nodes[node[0]]['y'] = y
    label[node] = node
    node_x.append(x)
    node_y.append(y)
    node_list.append(node)
    node_weights[node] = np.cbrt(node_weights[node])
    node_weights_ordered.append(node_weights[node])

print(len(node_weights))
print(len(node_weights_ordered))

edge_x = []
edge_y = []
for edge in g.edges():
    x0, y0 = pos[edge[0]][0], pos[edge[0]][1]
    x1, y1 = pos[edge[1]][0], pos[edge[1]][1]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(g.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append(node_list[node] + ' # of connections: '+ str(len(adjacencies[1])))

nx.write_gexf(g, "test.gexf")
#g = nx.read_gexf('test.gexf')
#bb = nx.betweenness_centrality(g)
nx.set_node_attributes(g, label, "label")
nx.set_node_attributes(g, node_weights_ordered, "weights")

plot = Plot(width=1400, height=1000,
            x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))

plot.add_tools(HoverTool(tooltips=[("label","@label"),("weights","@weights")]), BoxZoomTool(), ResetTool(), TapTool())

graph_renderer = from_networkx(g, nx.kamada_kawai_layout, center=(0,0))

print(graph_renderer)

#graph_renderer.node_renderer.data_source.data['index'] = list(reversed(range(len(g))))
graph_renderer.node_renderer.data_source.data['size'] = node_weights_ordered
graph_renderer.node_renderer.data_source.data['hoversize'] = [25]*len(g)
#graph_renderer.node_renderer.data_source.data['color'] = ['lightblue']*len(g)
node_color = np.cbrt(node_adjacencies)
print(node_color)
graph_renderer.node_renderer.data_source.data['color'] = node_color
#graph_renderer.node_renderer.glyph = Circle(size='size',
#                                            fill_color=linear_cmap('color',
#                                                                'Blues8',
#                                                                min(node_color),
#                                                                max(node_color))
#                                           )

graph_renderer.node_renderer.selection_glyph = Circle(size='hoversize', fill_color=Spectral4[2])
#graph_renderer.node_renderer.hover_glyph = Circle(size='hoversize', fill_color=Spectral4[1])

graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.5, line_width=2)
#graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
#graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

#graph_renderer.selection_policy = NodesAndLinkedEdges()

print(graph_renderer)
print(graph_renderer.to_json(include_defaults=True))
print("Writing out file interactive_graphs.html")
output_file("data/index.html")
show(plot)
