import numpy as np
import math


class Node:
    """
    A simple node in the HNSW graph.

    Attributes:
        id: Unique identifier.
        vector: The high-dimensional data vector.
        level: The maximum layer this node exists in.
        neighbors: A dictionary mapping level -> list of neighbor Node objects.
    """

    def __init__(self, id, vector, level):
        self.id = id
        self.vector = vector
        self.level = level
        self.neighbors = {}  # For each layer, a list of neighbor nodes.

    def __repr__(self):
        return f"Node({self.id, self.level})"

    def neighbor_ids(self):
        for v in self.neighbors:
            print(self.neighbors[v])
        return [v for v in self.neighbors]


class HNSW:
    """
    HNSW implementation mimicking pgvector's default hyperparameters.

    Hyper-parameters provided at initialization:
      - M:              Maximum number of neighbors per node for layers > 0.
      - Mmax:           Maximum number of neighbors for layer 0 (typically 2 * M).
      - efConstruction: Size of the candidate list during insertion.
      - L:              Maximum level allowed for a node.
    """

    def __init__(self, M, layer0_M, efConstruction, L):
        assert M > 0
        assert layer0_M >= M
        assert efConstruction > 1
        assert L > 0

        self.M = M
        # ml: Level multiplier = 1/ln(M), used in random level generation.
        self.mL = 1 / math.log(M)
        self.Mmax = layer0_M
        self.efConstruction = efConstruction
        self.L = L
        self.entry_point = None  # Current entry point for the graph.
        self.max_level = -1  # Maximum layer currently in the graph.
        self.nodes = {}  # Optional: store nodes by id.
        self.all_nodes = []  # Optional: store nodes by id.
        self.population = [0] * L

    # Create an HNSW instance with the given hyperparameters.
    def with_seeded_prng(M, layer0_M, efConstruction, L, seed):
        """
        M              -- Maximum number of neighbors per node (layers > 0).
        layer0_M       -- Maximum number of neighbors for layer 0.
        efConstruction -- Candidate list size during insertion.
        seed           -- Random seed for reproducibility.
        """

        np.random.seed(seed)
        return HNSW(M, layer0_M, efConstruction, L)

    def new(M, layer0_M, efConstruction, L):
        np.random.seed()
        return HNSW(M, layer0_M, efConstruction, L)

    def create_random_nodes(self, num_nodes, vector_dim):
        assert num_nodes > 0
        assert vector_dim > 0
        # Create random nodes.
        nodes = []
        for i in range(num_nodes):
            vec = np.random.rand(vector_dim)
            lvl = self.random_level()
            node = Node(id=i, vector=vec, level=lvl)
            for l in range(lvl + 1):
                node.neighbors[l] = []
            nodes.append(node)
            # increment the count the inhabitants in the layer
            self.population[lvl] += 1
        return nodes

    def bulk_insert(self, nodes):
        assert len(nodes) > 0
        # Insert nodes into the graph.
        self.insert(nodes[0])
        for node in nodes[1:]:
            self.insert(node)
        self.all_nodes = nodes

    def distance(self, vec1, vec2):
        """Euclidean distance between two vectors."""
        return np.linalg.norm(np.array(vec1) - np.array(vec2))

    def random_level(self):
        """
        Sample a random level for a new node using an exponential distribution.
        The probability of increasing level is determined by mL, capped by L.
        Recall that a geometric progression has the form a, ar, ar^2, ar^3, ar^4,...
        """
        assert self.mL == 1 / np.log(self.M)
        l = -int(np.log(np.random.random()) * self.mL)
        level = min(l, self.L - 1)
        # print(
        #    f"level_for_new_node: maxLevels: {self.L} computed: {l}, assigned: {level}"
        # )
        return level

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
            for lvl in range(q.level + 1):
                q.neighbors[lvl] = []
            self.nodes[q.id] = q
            print(f"\tinserted the first node {q} of layer_{q.level}")
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
            # Use Mmax for layer 0; otherwise use M.
            M_param = self.Mmax if level == 0 else self.M
            # 10. neighbors ← SELECT-NEIGHBORS(q, W, M, lc) // alg. 3 or alg. 4
            neighbors = self.select_neighbors_heuristic(candidates, M_param, q)
            # 11. add bidirectional connections from neighbors to q at layer lc
            q.neighbors[level] = neighbors
            for neighbor in neighbors:
                if level not in neighbor.neighbors:
                    neighbor.neighbors[level] = []
                neighbor.neighbors[level].append(q)
            # 12. for each e ∈ neighbors // shrink connections if needed
            for neighbor in neighbors:
                if len(neighbor.neighbors[level]) > (
                    self.Mmax if level == 0 else self.M
                ):
                    neighbor.neighbors[level] = self.select_neighbors_heuristic(
                        neighbor.neighbors[level],
                        (self.Mmax if level == 0 else self.M),
                        neighbor,
                    )
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

        d_ep = self.distance(q.vector, ep.vector)

        visited.add(ep.id)  # 1. v ← ep
        candidates.append((ep, d_ep))  # 2. C ← ep
        nn.append((ep, d_ep))  # 3. W ← ep

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
            if level in nearest_candidate.neighbors:  # 9. neighborhood(c) at layer lc
                # 9. for each e ∈ neighborhood(c) at layer lc // update C and W
                for neighbor in nearest_candidate.neighbors[level]:
                    # 10. if e ∉ v (use e only if it is not already visited)
                    if neighbor.id not in visited:
                        # 11. v ← v ⋃ e
                        visited.add(neighbor.id)
                        # distance(e, q)
                        dist_neighbor = self.distance(q.vector, neighbor.vector)
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
    def select_neighbors_heuristic(self, candidate_list, M, q):
        """
        Select up to M neighbors from candidate_list using the heuristic described in the paper.
        """
        sorted_candidates = sorted(
            candidate_list, key=lambda node: self.distance(q.vector, node.vector)
        )
        selected = []
        for candidate in sorted_candidates:
            good = True
            for s in selected:
                if self.distance(candidate.vector, s.vector) < self.distance(
                    q.vector, candidate.vector
                ):
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
            print(f"\tcandidates at level {level} {candidates}")
            cur_ep = candidates[0]
        candidate_list = self.search_layer(q, cur_ep, ef=ef, level=0)
        candidate_list.sort(key=lambda node: self.distance(q.vector, node.vector))
        return candidate_list[:k]


def test_knn_search(hnsw, dim, k, ef):
    """
    dim  -- vector dimension
    k    -- number of nearest neighbors to search
    ef   -- exploration factor
    """

    # Create a random query node.
    query_vector = np.random.rand(dim)
    query_node = Node(id="query", vector=query_vector, level=0)

    # Perform k-NN search.
    neighbors = hnsw.knn_search(query_node, k, ef)

    print("Query vector:", query_vector)
    print("Found nearest neighbors:")
    for neighbor in neighbors:
        d = hnsw.distance(query_node.vector, neighbor.vector)
        print(f"  Node {neighbor.id} at {neighbor.vector} with distance {d:.4f}")


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
    L = 2
    layer0_M = 32
    efConstruction = 32

    nodes = []
    node_data = [
        (3, [3.0, 0.0], 0),
        (8, [8.0, 0.0], 1),
        (4, [4.0, 0.0], 0),
        (5, [5.0, 0.0], 0),
        (11, [11.0, 0.0], 1),
        (6, [6.0, 1.0], 0),
        (2, [2.0, 0.0], 0),
        (7, [7.0, 0.0], 0),
        (9, [9.0, 0.0], 2),
        (10, [10.0, 0.0], 0),
        (12, [12.0, 0.0], 1),
        (13, [13.0, 0.0], 0),
        (14, [14.0, 0.0], 0),
        (1, [1.0, 0.0], 0),
        (20, [20.0, 0.0], 0),
        (30, [30.0, 0.0], 0),
    ]
    for id, vec, lvl in node_data:
        node = Node(id, vector=vec, level=lvl)
        nodes.append(node)

    print(f"Node: {nodes}")
    hnsw = HNSW.new(M, layer0_M, efConstruction, L)
    hnsw.bulk_insert(nodes)
    print(f"\tentry point of hnsw {hnsw.entry_point}")
    print(f"\tmax_level of hnsw {hnsw.max_level}")

    query_vector = [9.8, 0]
    query_node = Node(id="query", vector=query_vector, level=0)

    # Perform k-NN search.
    k = 4  # Number of nearest neighbors to search for.
    ef = 16  # Candidate list size during search (efSea
    neighbors = hnsw.knn_search(query_node, k, ef)

    print("Query vector:", query_vector)
    print(f"Found {len(neighbors)} nearest neighbors")
    for neighbor in neighbors:
        d = hnsw.distance(query_node.vector, neighbor.vector) ** 2
        print(
            f"\tNode {neighbor.id}<{neighbor.vector}> at {neighbor.level} with distance {d:.4f}"
        )


if __name__ == "__main__":
    test_small_world_in_layer0()
