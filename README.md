# thatNode

## Presentation
thatNode is a Python project that aims to implement algorithms from mathematical morphology for graphs. Current version requires the classic `networkx`, `scipy`, `numpy`, `matplotlib`.  

## Binary graph morphology
### Operators
Currently, thatNode provides a set of binary graph operators :
* erosion
* dilatation
* opening
* closing
* skeleton
* distance graph 
* geodesic reconstruction
* connected components labelling
* zones of influence
* laplacian
* symetrical gradient
* internal gradient
* external gradient

For an complete overview of these operators, just download and run binGraphExamples.py :
```python
python3 binGraphExamples.py
```
You will also find illustrations in the illustation folder.

### Constructing a graph
A graph is a networkx graph structure. Currently, thatNode adds the opportunity to create graph edges according to the delaunay triangulation of nodes.

Then you can create binary graph with a few functions, especially `connectedComponents(graph, nbConnComp, nbNodesInConnComp) 

### Drawing a graph
A few functions enables you to draw binary graph, distance graph, labelled graph or graph of zones of influence.

### Miscellaneous
We can import the package in 'main' using  
```python
import tools.drawTools as dt
import tools.gMorphoTools as gmt
```

## Complete example of use
...soon...

## Under development
*

## More precisely on graph Morphology
Mathematical morphology is a useful tool to extract data from a certain structure. It is well-known in image analysis. It has been extended to graphs in the late 80s.

thatNode is based on the research papers : GRAPHS AND MATHEMATICAL MORPHOLOGY by Luc VINCENT (April 1988) and GRAPH MORPHOLOGY IN IMAGE ANALYSIS by Henk HEIJMANS and Luc VINCENT (1992).

The current version does not use structuring elements (i.e. structuring graphs) - see research papers.

## Contact
Hugo GANGLOFF, Hgolou at gmail

## Keywords
Mathematical Morphology, Graphs, Graph Morphology, Python, Networkx
