import numpy as np
import math


class Node:
    """
    Attributes:
        id: Unique identifier.
        vector: The high-dimensional data vector.
        level: Node's layer.
        neighbors: A dictionary mapping level -> list of neighbor Node objects.
    """

    def __init__(self, id, vector):
        self.id = id
        self.vector = vector
        # self.level = level
        self._neighbors = None  # 'key' = level:[0..N] -> 'val' = neighbors: [Node]

    def set_level(self, level):
        assert isinstance(level, int) and level >= 0
        self.level = level

    def init_neighborhood(self, level):
        assert isinstance(level, int) and level >= 0
        assert self._neighbors is None
        self._neighbors = {}
        for l in range(level + 1):
            self._neighbors[l] = []

    def has_neighbors(self, level):
        assert isinstance(level, int) and level >= 0
        return self._neighbors and level in self._neighbors

    def neighbors(self, level):
        assert isinstance(level, int)
        assert level >= 0 and level <= self.level and level <= self.level
        assert self._neighbors is not None
        assert level in self._neighbors
        return self._neighbors[level]

    def set_neighbors(self, level, neighbors):
        assert isinstance(level, int) and level >= 0 and level <= self.level
        assert len(neighbors) > 0
        assert self._neighbors is not None
        assert level in self._neighbors and not self._neighbors[level]
        self._neighbors[level] = neighbors

    def add_neighbor(self, level, neighbor):
        assert isinstance(level, int) and level >= 0 and level <= self.level
        assert self._neighbors is not None
        if level not in self._neighbors:
            self._neighbors[level] = []
        self._neighbors[level].append(neighbor)

    def __repr__(self):
        return f"Node({self.id, self.level})"


def distance(s, t):
    """Euclidean distance between two vectors."""
    assert isinstance(s, Node)
    assert isinstance(t, Node)
    return np.linalg.norm(np.array(s.vector) - np.array(t.vector))


class HNSW:
    """
    parameters provided at initialization:
      - M:              Maximum number of neighbors per node for layers > 0.
      - Mmax:           Maximum number of neighbors for layer 0 (typically 2 * M).
      - efConstruction: Size of the candidate list during insertion.
    """

    def __init__(self, M, layer0_M, efConstruction):
        assert M > 0
        assert layer0_M >= M
        assert efConstruction > 1

        self.M = M
        # ml: Level multiplier = 1/ln(M), used in random level generation.
        self.mL = 1 / math.log(M)
        self.Mmax = layer0_M
        self.efConstruction = efConstruction
        self.entry_point = None  # Current entry point for the graph.
        self.max_level = -1  # Maximum layer currently in the graph.
        self.nodes = {}  # Optional: store nodes by id.
        self.all_nodes = []  # Optional: store nodes by id.
        self.population = [0] * 32

    # Create an HNSW instance with the given hyperparameters.
    def with_seeded_prng(M, layer0_M, efConstruction, seed):
        """
        M              -- Maximum number of neighbors per node (layers > 0).
        layer0_M       -- Maximum number of neighbors for layer 0.
        efConstruction -- Candidate list size during insertion.
        seed           -- Random seed for reproducibility.
        """

        np.random.seed(seed)
        return HNSW(M, layer0_M, efConstruction)

    def new(M, layer0_M, efConstruction):
        np.random.seed()
        return HNSW(M, layer0_M, efConstruction)

    def create_random_nodes(self, num_nodes, vector_dim):
        assert num_nodes > 0
        assert vector_dim > 0
        # Create random nodes.
        nodes = []
        for i in range(num_nodes):
            vec = np.random.rand(vector_dim)
            l = self.random_level()
            node = Node(id=i, vector=vec)
            node.set_level(l)
            node.init_neighborhood(l)
            nodes.append(node)
            # increment the count the inhabitants in the layer
            self.population[lvl] += 1
        return nodes

    def bulk_insert(self, nodes):
        assert len(nodes) > 0
        self.insert(nodes[0])
        for node in nodes[1:]:
            self.insert(node)
        self.all_nodes = nodes

    def random_level(self):
        """
        Sample a random level for a new node using an exponential distribution.
        The probability of increasing level is determined by mL, capped by L.
        Recall that a geometric progression has the form a, ar, ar^2, ar^3, ar^4,...
        """
        assert self.mL == 1 / np.log(self.M)
        return -int(np.log(np.random.random()) * self.mL)

    def maxM(self, level):
        assert isinstance(level, int)
        assert level >= 0 and level <= self.max_level
        return self.Mmax if level == 0 else self.M

    def connect(level, node, neighbors):
        node.set_neighbors(level, neighbors)
        for n in neighbors:
            n.add_neighbor(level, node)

    # -------------------------------------------------------------------------
    # Algorithm 1: INSERT(q, ep, M, efConstruction)
    # -------------------------------------------------------------------------
    def insert(self, q):
        """
        Insert a new node q (of type Node) into the HNSW graph.

        Uses a greedy search from the current entry point at layers above q.level,
        then for each layer from min(q.level, max_level) down to 0, it performs a
        neighborhood search followed by neighbor selection (Algorithm 4).
        For layer 0, Mmax is used instead of M.
        """
        if self.entry_point is None:
            self.entry_point = q
            self.max_level = q.level
            self.nodes[q.id] = q
            print(f"\tinserted the first node {q} in layer {q.level}")
            return

        # Step 1: Greedy search on layers above q.level.
        # 5. for lc ← L … l+1
        ep = self.entry_point
        for level in range(self.max_level, q.level, -1):
            # 6. W ← SEARCH-LAYER(q, ep, ef=1, lc)
            nearest_nodes = self.search_layer(q, ep, ef=1, level=level)
            # 7. ep ← get the nearest element from W to q
            ep = nearest_nodes[0]

        # Step 2: For each layer from min(q.level, max_level) down to 0, insert q.
        # 8. for lc ← min(L, l) … 0 (inclusive)
        for level in range(min(q.level, self.max_level), -1, -1):
            # 9. W ← SEARCH-LAYER(q, ep, efConstruction, lc)
            candidates = self.search_layer(q, ep, ef=self.efConstruction, level=level)
            # 10. neighbors ← SELECT-NEIGHBORS(q, W, M, lc) // alg. 3 or alg. 4
            neighbors = self.select_neighbors_heuristic(candidates, self.maxM(level), q)
            # 11. add bidirectional connections from neighbors to q at layer lc
            HNSW.connect(level, q, neighbors)
            # 12. for each e ∈ neighbors // shrink connections if needed
            for node in neighbors:
                if len(node._neighbors[level]) > (self.Mmax if level == 0 else self.M):
                    new_neighbors = self.select_neighbors_heuristic(
                        node.neighbors(level),
                        self.maxM(level),
                        node,
                    )
                    node.set_neighbors(level, new_neighbors)
            ep = candidates[0]
        self.nodes[q.id] = q
        #
        if q.level > self.max_level:
            self.max_level = q.level
            self.entry_point = q

    def farthest_distance(neighbors):
        assert len(neighbors) > 0
        for e, d in neighbors:
            assert type(d) == "int"
            assert isinstance(d, int)
        max(neighbors, key=lambda x: x[1])[1]

    # Algorithm 2: SEARCH_LAYER(q, ep, ef, level)
    def search_layer(self, q, ep, ef, level):
        """
        searches for the nearest neighbors of query node q starting from entry point ep.
        returns a list of nodes sorted by distance to q.
        """
        visited = set()  # v // set of visited elements
        candidates = []  # C // set of candidates
        nn = []  # W // dynamic list of found nearest neighbors

        visited.add(ep.id)  # 1. v ← ep
        candidates.append((ep, distance(q, ep)))  # 2. C ← ep
        nn.append((ep, distance(q, ep)))  # 3. W ← ep

        candidates.sort(key=lambda x: x[1])

        while candidates:  # 4. while │C│ > 0
            # 5. c ← extract nearest element from C to q
            candidates = sorted(candidates, key=lambda x: x[1])
            nearest_candidate, nearest_candidate_dist = candidates.pop(0)
            # 6. f ← get furthest element from W to q
            farthest_neighbor_dist = max(nn, key=lambda x: x[1])[1]
            # 7. if distance(c, q) > distance(f, q)
            if nearest_candidate_dist > farthest_neighbor_dist:
                break  # 8. all elements in W have been evaluated
            if nearest_candidate.has_neighbors(level):  # 9. neighborhood(c) at layer lc
                # 9. for each e ∈ neighborhood(c) at layer lc // update C and W
                for neighbor in nearest_candidate.neighbors(level):
                    # 10. if e ∉ v (use e only if it is not already visited)
                    if neighbor.id not in visited:
                        # 11. v ← v ⋃ e
                        visited.add(neighbor.id)
                        # distance(e, q)
                        dist_neighbor = distance(q, neighbor)
                        # 12. f ← get furthest element from W to q
                        f = max(nn, key=lambda x: x[1])[1]
                        # 13. if distance(e, q) < distance(f, q) or │W│ < ef
                        if dist_neighbor < f or len(nn) < ef:
                            # 14. C ← C ⋃ e
                            candidates.append((neighbor, dist_neighbor))
                            # 15. W ← W ⋃ e
                            nn.append((neighbor, dist_neighbor))
                            # 16. if │W│ > ef
                            # 17. remove furthest element from W to q
                            nn = sorted(nn, key=lambda x: x[1])[:ef]
        # 18. return W
        return [node for (node, d) in sorted(nn, key=lambda x: x[1])]

    # Algorithm 4: SELECT_NEIGHBORS_HEURISTIC(candidate_list, M, q)
    def select_neighbors_heuristic(self, candidates, M, q):
        """
        Select up to M neighbors from candidate_list.
        """
        candidates = sorted(candidates, key=lambda node: distance(q, node))
        selected = []
        for candidate in candidates:
            good = True
            for s in selected:
                if distance(candidate, s) < distance(q, candidate):
                    good = False
                    break
            if good:
                selected.append(candidate)
            if len(selected) >= M:
                break
        return selected

    # -------------------------------------------------------------------------
    # Algorithm 5: K_NN_SEARCH(q, k, ef)
    # -------------------------------------------------------------------------
    def knn_search(self, q, k, ef):
        cur_ep = self.entry_point
        # Greedy descent: from the top layer down to layer 1.
        for level in range(self.max_level, 0, -1):
            candidates = self.search_layer(q, cur_ep, ef=1, level=level)
            print(f"\tknn_search - candidates at level {level} {candidates}")
            cur_ep = candidates[0]
        candidate_list = self.search_layer(q, cur_ep, ef=ef, level=0)
        candidate_list.sort(key=lambda node: distance(q, node))
        return candidate_list[:k]


def test_randomized_vectors_hnsw():
    M = 16
    L = 5
    layer0_M = 32
    efConstruction = 200

    num_nodes = 1024 * 1024  # Number of nodes in the index.

    dim = 2  # vector dimension
    hnsw = HNSW.new(M, layer0_M, efConstruction, L)
    # hnsw = HNSW.with_seeded_prng(M, layer0_M, efConstruction, L, seed)
    nodes = hnsw.create_random_nodes(num_nodes, dim)
    print(hnsw.population)


def test_small_world_in_layer0():
    M = 16
    layer0_M = 32
    efConstruction = 8

    nodes = []
    node_data = [
        (3, [3.0, 0.0], 3),
        (8, [8.0, 0.0], 1),
        (4, [4.0, 0.0], 0),
        (5, [5.0, 0.0], 0),
        (11, [11.0, 0.0], 1),
        (6, [6.0, 1.0], 12),
        (2, [2.0, 0.0], 20),
        (7, [7.0, 0.0], 0),
        (9, [9.0, 0.0], 2),
        (10, [10.0, 0.0], 0),
        (12, [12.0, 0.0], 1),
        (13, [13.0, 0.0], 0),
        (14, [14.0, 0.0], 0),
        (1, [1.0, 0.0], 25),
        (20, [20.0, 0.0], 0),
        (30, [30.0, 0.0], 0),
    ]
    for id, vec, l in node_data:
        node = Node(id, vector=vec)
        node.set_level(l)
        node.init_neighborhood(l)
        nodes.append(node)

    hnsw = HNSW.new(M, layer0_M, efConstruction)
    hnsw.bulk_insert(nodes)
    print(f"\tentry point of hnsw {hnsw.entry_point}")
    print(f"\tmax_level of hnsw {hnsw.max_level}")

    query_vector = [8.30, 0]
    query = Node(id="query", vector=query_vector)
    query.set_level(0)
    query.init_neighborhood(0)

    # Perform k-NN search.
    k = 3  # Number of nearest neighbors to search for.
    ef = 16  # Candidate list size during search (efSea
    neighbors = hnsw.knn_search(query, k, ef)

    print("Query vector:", query_vector)
    print(f"Found {len(neighbors)} nearest neighbors")
    for node in neighbors:
        d = distance(query, node) ** 2
        print(f"\tNode {node.id}<{node.vector}> at {node.level} with distance {d:.4f}")


if __name__ == "__main__":
    test_small_world_in_layer0()
