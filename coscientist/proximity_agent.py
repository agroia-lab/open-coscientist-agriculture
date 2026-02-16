"""
Proximity agent
--------------
- Calculates similarity between hypotheses and builds a graph
"""

import networkx as nx
import numpy as np
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

from coscientist.custom_types import ParsedHypothesis


def create_embedding(text: str, dimensions: int = 256) -> np.ndarray:
    """Create a vector embedding for a text."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=dimensions)
    return np.array(embeddings.embed_query(text))


class ProximityGraph:
    """A graph of hypotheses and their similarity scores."""

    def __init__(self):
        self.graph = nx.Graph()

    def add_hypothesis(self, hypothesis: ParsedHypothesis):
        """Add a hypothesis to the graph."""
        embedding = create_embedding(hypothesis.hypothesis)
        self.graph.add_node(
            hypothesis.uid, hypothesis=hypothesis.hypothesis, embedding=embedding
        )

    def _compute_weighted_edges(
        self, hypothesis_ids_x: list[int], hypothesis_ids_y: list[int]
    ):
        """Compute the weighted edges between two sets of hypotheses."""
        embeddings_x = [self.graph.nodes[id]["embedding"] for id in hypothesis_ids_x]
        embeddings_y = [self.graph.nodes[id]["embedding"] for id in hypothesis_ids_y]
        similarities = cosine_similarity(embeddings_x, embeddings_y)
        # return similarities
        # Add the edges with weights to the graph
        for i, id_x in enumerate(hypothesis_ids_x):
            for j, id_y in enumerate(hypothesis_ids_y):
                if id_x == id_y:
                    continue
                self.graph.add_edge(id_x, id_y, weight=similarities[i, j])

    def update_edges(self):
        """
        Finds all nodes without an edge and all nodes with an edge and
        computes the weighted edges between them. If no nodes have edges,
        it will compute the weighted edges between all nodes.
        """
        # Hypothesis ids x are the nodes with degree greater than 0
        hypothesis_ids_x = [
            node for node in self.graph.nodes if self.graph.degree(node) > 0
        ]
        hypothesis_ids_y = [
            node for node in self.graph.nodes if self.graph.degree(node) == 0
        ]
        if len(hypothesis_ids_y) == 0:
            # Nothing to do, we're already up to date
            return
        elif len(hypothesis_ids_x) == 0:
            # No nodes with edges, compute all edges
            self._compute_weighted_edges(hypothesis_ids_y, hypothesis_ids_y)
        else:
            # Compute edges between nodes with and without edges
            self._compute_weighted_edges(hypothesis_ids_y, hypothesis_ids_y)
            self._compute_weighted_edges(hypothesis_ids_x, hypothesis_ids_y)

    def get_pruned_graph(self, min_weight: float = 0.85) -> nx.Graph:
        """Get a pruned graph with edges with weight less than min_weight removed."""
        pruned_graph = self.graph.copy()
        edges_to_remove = [
            (u, v)
            for u, v, d in pruned_graph.edges(data=True)
            if d["weight"] < min_weight
        ]
        pruned_graph.remove_edges_from(edges_to_remove)
        return pruned_graph

    def get_semantic_communities(
        self, resolution: float = 1.0, min_weight: float = 0.85
    ) -> list[set[int]]:
        """Get the partitions of the graph using the Louvain method."""
        # Prune edges from the graph with weight less than min_weight
        pruned_graph = self.get_pruned_graph(min_weight)
        return nx.community.louvain_communities(pruned_graph, resolution=resolution)

    def to_dict(self) -> dict:
        """Serialize the proximity graph to a JSON-safe dictionary."""
        nodes = {}
        for node_id in self.graph.nodes:
            node_data = self.graph.nodes[node_id]
            nodes[str(node_id)] = {
                "hypothesis": node_data.get("hypothesis", ""),
                "embedding": node_data.get("embedding", np.array([])).tolist(),
            }
        edges = []
        for u, v, data in self.graph.edges(data=True):
            edges.append(
                {
                    "source": str(u),
                    "target": str(v),
                    "weight": float(data.get("weight", 0.0)),
                }
            )
        return {"nodes": nodes, "edges": edges}

    @classmethod
    def from_dict(cls, data: dict) -> "ProximityGraph":
        """Deserialize the proximity graph from a dictionary."""
        graph = cls()
        for node_id, node_data in data.get("nodes", {}).items():
            graph.graph.add_node(
                node_id,
                hypothesis=node_data.get("hypothesis", ""),
                embedding=np.array(node_data.get("embedding", [])),
            )
        for edge_data in data.get("edges", []):
            graph.graph.add_edge(
                edge_data["source"],
                edge_data["target"],
                weight=edge_data["weight"],
            )
        return graph

    @property
    def average_cosine_similarity(self) -> float:
        """Get the average cosine similarity of the graph."""
        return np.mean([d["weight"] for u, v, d in self.graph.edges(data=True)]).item()
