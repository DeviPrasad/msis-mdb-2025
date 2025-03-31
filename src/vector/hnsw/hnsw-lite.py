import numpy as np
import math


class Vec:
    """
    Attributes:
        id: Unique identifier.
        vector: The high-dimensional data vector.
        level: Node's layer.
        neighbors: A dictionary mapping level -> list of neighbor Node objects.
            'key' = level:[0..N] -> 'val' = neighbors: [Node]
    """

    def __init__(self, id, vector):
        self.id = id
        self.vector = vector

    def level(self):
        assert self._level >= 0
        return self._level

    def set_level(self, level):
        assert isinstance(level, int) and level >= 0
        assert not hasattr(self, "_level")
        self._level = level

    def init_neighborhood(self, level):
        assert isinstance(level, int) and level >= 0
        assert not hasattr(self, "_neighbors")
        self._neighbors = {}
        for l in range(level + 1):
            self._neighbors[l] = []

    def has_neighbors(self, level):
        assert isinstance(level, int) and level >= 0
        assert hasattr(self, "_neighbors")
        if self._neighbors == [] and level in self._neighbors:
            assert self._neighbors[level] > 0
        return self._neighbors and level in self._neighbors

    def neighbors(self, level):
        assert isinstance(level, int)
        assert level >= 0 and level <= self.level()
        assert self._neighbors
        assert level in self._neighbors
        return self._neighbors[level]

    # neighbors are always sorted according to their distance from `self`
    def set_neighbors(self, level, neighbors):
        assert isinstance(level, int) and level >= 0 and level <= self.level()
        assert len(neighbors) > 0
        assert all([isinstance(v, Vec) for v in neighbors])
        assert self._neighbors
        assert level in self._neighbors
        assert not any([self.id == n.id for n in neighbors])
        for i in range(1, len(neighbors)):
            assert distance(self, neighbors[i - 1]) <= distance(self, neighbors[i])

        _new = [(t, distance(self, t)) for t in neighbors]
        if len(self._neighbors[level]) == 0:
            print(f"            set neighbors of {self}[{level}] = {_new}")
        else:
            _cur = [(t, distance(self, t)) for t in self._neighbors[level]]
            print(
                f"            replace {self}[{level}] = {_cur}\n            with    {self}[{level}] = {_new}"
            )
        self._neighbors[level] = neighbors

    def add_neighbor(self, level, neighbor):
        assert isinstance(level, int) and level >= 0 and level <= self.level()
        assert isinstance(neighbor, Vec)
        assert self._neighbors
        assert level in self._neighbors
        assert self.id != neighbor.id
        self._neighbors[level].append(neighbor)
        self._neighbors[level] = sorted(
            self._neighbors[level], key=lambda v: distance(self, v)
        )
        print(
            f"            add neighbor {self}[{level}].append({(neighbor, distance(self, neighbor))})"
        )

    def __repr__(self):
        return f"V<{self.id}, L{self.level()}>"
        # return f"N<{(self.vector[0], self.vector[1])}, L{self.level()}>"


def distance(s, t):
    """Euclidean distance between two vectors (rounded to four decimal digits)."""
    assert isinstance(s, Vec)
    assert isinstance(t, Vec)
    return round(np.linalg.norm(np.array(s.vector) - np.array(t.vector)), 4)


def rr3():
    return round(np.random.random() * 10, 3)


class HNSW:
    """
    parameters provided at initialization:
      - M:              Maximum number of neighbors per node for layers > 0.
      - Mmax:           Maximum number of neighbors for layer 0 (typically 2 * M).
      - efConstruction: Size of the candidate list during insertion.
    """

    def __init__(self, M, layer0_M, efConstruction):
        assert M > 0
        assert layer0_M > 0
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
            node = Vec(id=i, vector=vec)
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
        print()
        print(
            f"insert Vec<{q.id}, {q.vector}, {q.level()}>; hnsw_max_level: {self.max_level}"
        )
        if self.entry_point is None:
            self.entry_point = q
            self.max_level = q.level()
            self.nodes[q.id] = q
            print(f"    inserted the first node {q} in layer {q.level()}")
            print()
            return

        # Step 1: Greedy search on layers above q.level.
        # 5. for lc ← L … l+1
        ep = self.entry_point
        for level in range(self.max_level, q.level(), -1):
            print(f"    level {level} greedy search - entry point = {ep}")
            # 6. W ← SEARCH-LAYER(q, ep, ef=1, lc)
            nearest_nodes = self.search_layer(q, ep, ef=1, level=level)
            print(f"        nearest nodes to {q}[{level}] = {nearest_nodes}")
            # 7. ep ← get the nearest element from W to q
            ep = nearest_nodes[0]

        # Step 2: For each layer from min(q.level, max_level) down to 0, insert q.
        # 8. for lc ← min(L, l) … 0 (inclusive)
        for level in range(min(q.level(), self.max_level), -1, -1):
            print(f"    level {level} entry point = {ep}")
            # 9. W ← SEARCH-LAYER(q, ep, efConstruction, lc)
            candidates = self.search_layer(q, ep, ef=self.efConstruction, level=level)
            print(f"        candidates for {q}[{level}] = {candidates}")
            # 10. neighbors ← SELECT-NEIGHBORS(q, W, M, lc) // alg. 3 or alg. 4
            neighbors = self.select_neighbors_heuristic(
                candidates, self.maxM(level), q, il=3
            )
            print(f"        h-selection: q={q}, C={candidates}, S={neighbors}")
            # 11. add bidirectional connections from neighbors to q at layer lc
            HNSW.connect(level, q, neighbors)
            # 12. for each e ∈ neighbors // shrink connections if needed
            for node in neighbors:
                if len(node.neighbors(level)) > (self.Mmax if level == 0 else self.M):
                    new_neighbors = self.select_neighbors_heuristic(
                        node.neighbors(level), self.maxM(level), node, il=4
                    )
                    print(f"        ===== shrink connections of {node}=====")
                    node.set_neighbors(level, new_neighbors)
                    print(f"        ========.")
            ep = candidates[0]
        self.nodes[q.id] = q
        #
        if q.level() > self.max_level:
            print(
                f"    >>>> Update hnsw_max_level from {self.max_level} to {q.level()}"
            )
            print(f"    >>>> Update hnsw_entry_point from {self.entry_point} to {q}")
            self.max_level = q.level()
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

    def select_neighbors_heuristic(self, candidates, M, q, il):
        assert len(candidates) > 0
        assert M > 0
        assert isinstance(q, Vec)
        assert all([isinstance(n, Vec) for n in candidates])

        tabs = "    " * il
        candidates = sorted(candidates, key=lambda node: distance(q, node))
        print(f"{tabs}hns: q={q}, C={candidates}")
        selected = []
        """
        is c closer to q than it is to all (so far) selected nodes?
        - select c only if c closer to q than it is to all so far selected-node s.
        - do not select c if there is at least one selected-node s such that d(c, s) < d(c, q)
        - c if for all s, dist(c, s) > dist(c, q)
        """
        for c in candidates:
            if all([distance(c, s) > distance(c, q) for s in selected]):
                print(
                    f"{tabs}    d:(s;q) {[(((c.id, s.id), distance(c, s)),(c.id, q.id, distance(c, q))) for s in selected]}"
                )
                selected.append(c)
        return selected[:M]

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


def test_two_node_world():
    M = 4  # 16
    layer0_M = 4  # 32
    efConstruction = 8

    hnsw = HNSW.new(M, layer0_M, efConstruction)

    nodes = []
    node_data = [
        (1, [-1, -1], 0),
        (2, [-2, -2], 0),
        (3, [-3, -3], 0),
        (4, [-4, -4], 0),
    ]
    for id, vec, l in node_data:
        node = Vec(id, vector=vec)
        node.set_level(l)
        node.init_neighborhood(l)
        nodes.append(node)

    hnsw.bulk_insert(nodes)
    query_vector = [18.3, 5]
    query = Vec(id="query", vector=query_vector)
    hnsw.knn_search(query, 3, 6)


def test_small_world_in_layer0():
    M = 4  # 16
    layer0_M = 4  # 32
    efConstruction = 8

    hnsw = HNSW.new(M, layer0_M, efConstruction)

    nodes = []
    node_data = [
        (1, [1, 1], hnsw.random_level()),
        (2, [2, 1], hnsw.random_level()),
        (3, [1.5, 1.9], 0),
        (4, [1.5, 1.3], 0),
        (5, [1.6, 1.289], 0),
        (6, [1.4, 1.289], 0),
        (7, [1.7, 1.189], hnsw.random_level()),
        (8, [rr3(), rr3()], 1),
        (9, [rr3(), rr3()], hnsw.random_level()),
        (10, [20.0, rr3()], 1),
        (11, [26.0, rr3()], 2),
        (12, [rr3(), rr3()], hnsw.random_level()),
        (13, [rr3(), rr3()], 2),
        (14, [rr3(), rr3()], 0),
        (15, [rr3(), rr3()], hnsw.random_level()),
        (16, [10.5, 1], 3),
    ]
    for id, vec, l in node_data:
        node = Vec(id, vector=vec)
        node.set_level(l)
        node.init_neighborhood(l)
        nodes.append(node)

    hnsw.bulk_insert(nodes)
    print()
    print(f"entry point of hnsw {hnsw.entry_point}")
    print(f"max_level of hnsw {hnsw.max_level}")

    query_vector = [(rr3(), 0)]
    # query_vector = [18.3, 5]
    query = Vec(id="query", vector=query_vector)
    query.set_level(0)
    query.init_neighborhood(0)

    # Perform k-NN search.
    k = 3  # Number of nearest neighbors to search for.
    ef = 16  # Candidate list size during search (efSea
    neighbors = hnsw.knn_search(query, k, ef)

    print(
        f"\nFound {len(neighbors)} (approximate) nearest neighbors to the query vector {query_vector}"
    )
    for node in neighbors:
        d = distance(query, node) ** 2
        print(f"\tVec<{node.id}, {node.vector}, L{node.level()}> distance {d:.4f}")

    print(node_data)


if __name__ == "__main__":
    # test_two_node_world()
    test_small_world_in_layer0()
