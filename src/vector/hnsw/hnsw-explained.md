# HNSW Explained

## Upfront Summary
The following functions as described in [section 4 of the paper](https://arxiv.org/pdf/1603.09320), work together to create a highly efficient approximate nearest neighbor (ANN) index, balancing query performance with accuracy.

- **Random Level Assignment** creates a pyramid structure with exponentially fewer nodes at higher layers, facilitating efficient navigation.
- **INSERT** integrates a new data point by first using a greedy descent in the sparse upper layers, then establishing diverse local connections via a candidate search and neighbor selection heuristic.
- **SEARCH_LAYER** efficiently explores a single layer by maintaining a dynamic candidate list and halting once no more closer points are found.
- **SELECT_NEIGHBORS_HEURISTIC** ensures that the connectivity in the graph remains both effective for navigation and resistant to redundancy.
- **K-NN SEARCH** combines fast hierarchical descent with a comprehensive local search, ultimately returning the approximate nearest neighbors.

### Random Level Assignment
*(Corresponding to the paper’s randomized level assignment)*

- **Purpose:**
  To decide on which layers a new data point (node) will participate. Higher layers become increasingly sparse, which speeds up the search process.

- **How It Works:**
  - Start at level 0.
  - Repeatedly “flip a coin” (using a probability threshold based on \( mL = 1/\ln(M) \)) to decide whether to increment the level.
  - Stop either when the coin flip fails (the drawn random number exceeds \( mL \)) or when the maximum allowed level is reached.

- **Concept:**
  This mechanism creates an exponentially decaying probability for high levels, ensuring that only a few nodes exist in the top layers. These sparse layers serve as “shortcuts” during search.

---

### INSERT (Algorithm 1)

- **Purpose:**
  To integrate a new data point into the hierarchical graph structure in a way that preserves fast search properties.

- **Step-by-Step Process:**

  1. **Empty Graph Initialization:**
     - **Check for an Entry Point:**
       If no node exists yet (i.e., the structure is empty), the new node becomes the initial entry point for all layers on which it exists.

  2. **Greedy Search in Higher Layers:**
     - **If the New Node Is Lower:**
       If the new node’s level is lower than the current maximum level, start at the top of the hierarchy (using the current global entry point) and perform a greedy descent.
     - **Traversal:**
       For each layer above the new node’s level, the algorithm moves from one node to a neighboring node if that neighbor is closer to the new node. This “greedy” process quickly finds a node near the new point at the appropriate level.

  3. **Layer-wise Insertion (for each level from the minimum of the node’s level and the current maximum layer down to 0):**
     - **Neighborhood Exploration:**
       At the target layer, perform a local search (using the best-first strategy) to gather a candidate list of nearby nodes. The candidate list size is controlled by the parameter \( efConstruction \).
     - **Neighbor Selection:**
       Apply a heuristic (see “Select Neighbors Heuristic” below) to choose a subset of these candidates as neighbors, up to the allowed limit (using \( M \) or \( Mmax \) at layer 0).
     - **Link Formation:**
       Establish bidirectional links between the new node and each selected neighbor. This ensures that both nodes recognize each other in the graph, which is crucial for future search efficiency.

- **Concept:**
  The insertion process builds a layered, proximity graph. By first finding a good entry point via a fast greedy descent and then carefully selecting neighbors at each level, the algorithm maintains both the efficiency and the diversity of connections needed for approximate nearest neighbor search.

---

### SEARCH_LAYER (Algorithm 2)

- **Purpose:**
  To explore one layer of the HNSW graph to find nodes that are near a given query point.

- **Step-by-Step Process:**

  1. **Initialization:**
     - **Start from an Entry Point:**
       Begin at a designated starting node (obtained from a higher layer or the global entry point).
     - **Set Up Data Structures:**
       Maintain a candidate list (nodes to be explored) and a result set (the current best nodes), both organized by their proximity to the query.

  2. **Exploration Loop:**
     - **Best-First Selection:**
       Repeatedly select the candidate that is closest to the query from the candidate list.
     - **Termination Condition:**
       If the closest candidate in the list is farther from the query than the worst node in the result set, the search in this layer terminates.

  3. **Neighbor Examination:**
     - For the chosen candidate, look at all its neighbors in the current layer.
     - For each unvisited neighbor, compute its distance to the query.
     - If the neighbor is promising—either because the result set isn’t full or it is closer than the current worst neighbor—it is added to both the candidate list and the result set.
     - The candidate list and result set are kept sorted by distance.

- **Concept:**
  This best-first search at one level of the graph is efficient because it leverages the existing connections to quickly prune away less promising areas of the search space. The stopping condition ensures that once no closer neighbors are found, the process can stop, avoiding unnecessary exploration.

---

### SELECT_NEIGHBORS_HEURISTIC (Algorithm 4)

- **Purpose:**
  To choose a set of diverse and “useful” neighbors from a candidate list for a node.

- **Step-by-Step Process:**

  1. **Sorting:**
     - Begin by ordering the candidate nodes by their distance to the target node.

  2. **Iterative Selection:**
     - Process each candidate in order.
     - For each candidate, check against the already selected neighbors.
     - **Redundancy Check:**
       If the candidate is “redundant” (i.e., if one of the selected neighbors is closer to this candidate than the candidate is to the target), then the candidate is not added.

  3. **Stop When Full:**
     - Continue until you have selected the maximum allowed number of neighbors (either \( M \) or \( Mmax \)).

- **Concept:**
  This heuristic is critical for ensuring that the local neighborhood is not overly concentrated. By avoiding redundant connections, the algorithm maintains a well-spread graph topology that is more robust for search.

---

### K-NN SEARCH (Algorithm 5)

- **Purpose:**
  To perform an approximate k-nearest neighbor search using the HNSW graph.

- **Step-by-Step Process:**

  1. **Greedy Descent in Upper Layers:**
     - Start at the top layer with the global entry point.
     - At each layer (from the highest down to layer 1), perform a greedy search with a minimal candidate list (using \( ef = 1 \)) to quickly navigate toward the region of the query.

  2. **Comprehensive Search at Layer 0:**
     - Once at the base layer, execute a more thorough search using a larger candidate list (controlled by the parameter \( ef \)).
     - This search gathers a set of candidate nodes in the immediate neighborhood of the query.

  3. **Final Sorting and Selection:**
     - Order the candidates by their distance to the query.
     - Return the top \( k \) nodes as the approximate nearest neighbors.

- **Concept:**
  This two-phase search leverages the hierarchical structure: the upper layers provide fast, coarse localization, and the base layer refines the search with a more exhaustive exploration. This design is what makes HNSW both fast and accurate.

---
