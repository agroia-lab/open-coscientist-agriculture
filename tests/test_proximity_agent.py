"""Tests for coscientist/proximity_agent.py - ProximityGraph serialization."""

import numpy as np

from coscientist.proximity_agent import ProximityGraph


class TestProximityGraphSerialization:
    """Tests for ProximityGraph to_dict/from_dict."""

    def test_empty_graph_roundtrip(self):
        g = ProximityGraph()
        data = g.to_dict()
        g2 = ProximityGraph.from_dict(data)
        assert len(g2.graph.nodes) == 0
        assert len(g2.graph.edges) == 0

    def test_graph_with_nodes_roundtrip(self):
        g = ProximityGraph()
        g.graph.add_node(
            "node-1",
            hypothesis="Test hypothesis 1",
            embedding=np.array([0.1, 0.2, 0.3]),
        )
        g.graph.add_node(
            "node-2",
            hypothesis="Test hypothesis 2",
            embedding=np.array([0.4, 0.5, 0.6]),
        )

        data = g.to_dict()
        g2 = ProximityGraph.from_dict(data)

        assert len(g2.graph.nodes) == 2
        assert g2.graph.nodes["node-1"]["hypothesis"] == "Test hypothesis 1"
        np.testing.assert_array_almost_equal(
            g2.graph.nodes["node-1"]["embedding"], [0.1, 0.2, 0.3]
        )

    def test_graph_with_edges_roundtrip(self):
        g = ProximityGraph()
        g.graph.add_node("a", hypothesis="H1", embedding=np.array([1.0, 0.0]))
        g.graph.add_node("b", hypothesis="H2", embedding=np.array([0.0, 1.0]))
        g.graph.add_edge("a", "b", weight=0.85)

        data = g.to_dict()
        g2 = ProximityGraph.from_dict(data)

        assert len(g2.graph.edges) == 1
        assert g2.graph["a"]["b"]["weight"] == 0.85

    def test_to_dict_numpy_converted_to_list(self):
        g = ProximityGraph()
        g.graph.add_node("n1", hypothesis="H", embedding=np.array([0.1, 0.2]))
        data = g.to_dict()
        # Embedding should be a regular Python list (JSON-safe)
        assert isinstance(data["nodes"]["n1"]["embedding"], list)

    def test_pruned_graph(self):
        g = ProximityGraph()
        g.graph.add_node("a", hypothesis="H1", embedding=np.array([1.0]))
        g.graph.add_node("b", hypothesis="H2", embedding=np.array([1.0]))
        g.graph.add_node("c", hypothesis="H3", embedding=np.array([1.0]))
        g.graph.add_edge("a", "b", weight=0.90)
        g.graph.add_edge("a", "c", weight=0.70)

        pruned = g.get_pruned_graph(min_weight=0.85)
        assert len(pruned.edges) == 1  # Only a-b survives
