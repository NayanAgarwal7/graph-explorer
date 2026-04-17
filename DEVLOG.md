# DEVLOG

## Project
Graph Explorer — Interactive graph algorithm learning tool

## Tagline
Don't just watch algorithms run. Learn to think like them.

---

## Day 1 — Graph Editor Foundation

### Goals
- Set up Flask app
- Create graph drawing canvas
- Add nodes
- Add weighted edges
- Add delete functionality
- Build basic layout

### What I built
- Flask project scaffold with `app.py`, `templates/`, and `static/`
- Canvas-based graph editor
- Left click on empty space adds a node
- Left click one node, then another creates a weighted edge
- Right click on a node deletes that node and all connected edges
- Right click on an edge deletes only that edge
- Sidebar with usage instructions
- Selected-node highlight when creating edges

### Technical decisions
- Stored graph state in-memory as:
  - `graph["nodes"]`
  - `graph["edges"]`
- Used Flask API routes for node and edge operations
- Treated graph as undirected for traversal logic

### Bugs I hit
- Flask was not installed in the active environment
- `algorithms.py` looked broken because the file had not been saved
- Node ID collision after deleting the last node
- Duplicate undirected edges were allowed in reverse order
- Canvas existed but looked invisible until styled

### Fixes
- Installed Flask in the correct virtual environment
- Fixed node ID generation using `max(existing_ids) + 1`
- Prevented duplicate edges in both directions
- Added canvas border and workspace layout styling

### Outcome
By the end of Day 1, the project had a working graph editor with creation, connection, deletion, and a usable interface.

---

## Day 2 — Algorithms + Animation + Predict Mode

### Goals
- Implement BFS, DFS, and Dijkstra from scratch
- Return step-by-step traces from the backend
- Animate traversal on the frontend
- Show data structure state live
- Build Predict Mode with scoring

### What I built

#### Algorithms
Implemented from scratch in `algorithms.py`:
- BFS
- DFS
- Dijkstra

Each algorithm returns a full trace of steps instead of only a final result.

Each step includes:
- step number
- visited node
- structure snapshot
- distances for Dijkstra
- plain-English explanation

#### Backend API
Added algorithm routes:
- `/api/algorithm/bfs`
- `/api/algorithm/dfs`
- `/api/algorithm/dijkstra`

#### Frontend
Built controls for:
- Run
- Next Step
- Play
- Pause
- Reset Traversal

Added frontend animation state:
- current trace
- current step index
- current visited node
- visited history

### Learning features
- Live queue panel for BFS
- Live stack panel for DFS
- Live priority queue and distance updates for Dijkstra
- Step explanation after each move

### Predict Mode
Built Predict Mode with:
- checkbox toggle
- click-based prediction
- scoring
- red / green visual feedback
- correctness message merged with traversal explanation

### Bugs I hit
- Route existed but server had not been restarted
- Traversal state did not reset cleanly
- Feedback text was getting overwritten
- Predict Mode conflicted with Play mode
- Start-node issues appeared after node deletion testing

### Fixes
- Restarted Flask after route updates
- Added traversal reset state
- Prevented Play mode while Predict Mode is enabled
- Preserved visited-node history
- Combined prediction feedback with step explanation

### Outcome
By the end of Day 2, Graph Explorer had become a real interactive learning tool rather than just a graph drawer.

---

## Day 3 — SQLite Save/Load

### Goals
- Persist graphs beyond one app session
- Save user-created graphs by name
- Load previously saved graphs

### What I built
- Added `schema.sql`
- Added `db.py`
- Initialized SQLite database on app startup
- Added save route for current graph
- Added load route for named graphs
- Added graph listing route

### New routes
- `/api/graph/save`
- `/api/graphs`
- `/api/graph/load/<name>`

### Database structure
Saved each graph with:
- id
- name
- graph_data
- created_at

### Bugs I hit
- Save worked but I forgot some changed files were not committed
- Testing old saved names caused confusion during loading
- Database file began changing during repeated local tests

### Fixes
- Checked save/load using PowerShell requests and UI prompts
- Cleaned commit flow
- Confirmed graph JSON was correctly round-tripping through SQLite

### Outcome
The project gained persistence. Custom graphs could now be saved and loaded instead of being lost on refresh.

---

## Day 4 — Scenario Presets

### Goals
- Add meaningful built-in graph examples
- Connect algorithm learning with real-world style use cases

### What I built
Added three demo scenarios:
- City Map
- Social Network
- Course Prerequisites

Each scenario loads a fixed graph with meaningful labels.

### Why this mattered
This made the project easier to understand from a user point of view:
- Dijkstra on a city map
- BFS on a social network
- DFS on course dependency chains

### Outcome
Graph Explorer became both:
- a graph sandbox
- and a concept demo tool

---

## Day 5 — Product Direction Experiments

### What I tried
I experimented with a different product direction where scenarios stopped being fixed demo graphs and instead acted as meanings or interpretations for any custom graph.

Example idea:
- same graph, but interpreted as a city map
- same graph, but interpreted as a social network

### Why I explored it
I wanted to see whether scenarios could be made dynamic and user-driven.

### Problem discovered
This made the product more confusing:
- a random user graph does not naturally become a real city map
- scenario meaning and scenario graph started colliding
- the interface became less clear for actual users

### Outcome
This experiment helped clarify the real product direction even though it was not the final design.

---

## Day 6 — Revert and Product Clarity

### Decision
I reverted to a cleaner **Demo + Sandbox** design:

#### Demo mode
Built-in fixed scenarios:
- City Map
- Social Network
- Course Prerequisites

#### Sandbox mode
User-created custom graphs:
- create
- edit
- save
- load
- explore with algorithms

### Why this was better
It made the product understandable:
- examples stay meaningful
- user graphs stay flexible
- both use the same traversal engine

### Outcome
This became the final direction of the project.

---

## Day 7 — UI Polish + Final Documentation

### Goals
- Make the interface cleaner
- Finalize README
- Finalize DEVLOG
- Prepare the project for demo/submission

### Improvements
- Cleaner layout structure
- Better spacing and card-based interface
- Stronger visual hierarchy
- Updated README for final product explanation
- Extended DEVLOG to include later design decisions

### Outcome
The project reached a polished prototype stage with both learning value and a clear final direction.

---

## Final Working Features
- Graph editor
- Weighted undirected edges
- Node delete + connected edge cleanup
- Edge delete
- BFS
- DFS
- Dijkstra
- Step trace animation
- Queue / stack / priority queue display
- Plain-English step explanation
- Predict Mode
- Score tracking
- Correct / wrong feedback
- SQLite save/load
- Built-in demo scenarios

---

## Future Version Ideas
- Draggable nodes
- Rename custom nodes
- Directed graph mode
- More graph algorithms
- Better mobile responsiveness
- Export/import graph JSON
- Scenario description panel improvements

---

## Key lesson
The biggest lesson from this project was that a technically possible feature is not always a good product feature. Returning traversal traces from the backend made the learning system possible, but the later scenario experiment showed that product clarity matters just as much as code.