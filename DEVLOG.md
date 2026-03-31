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
- Fixed node ID generation using:
  - `max(existing_ids) + 1`
- Prevented duplicate edges in both directions
- Added canvas border and workspace layout styling

### Outcome
By the end of Day 1, the project was no longer a mockup. It had a working graph editor with creation, connection, deletion, and clean UI structure.

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

Each algorithm returns a trace of steps instead of only a final answer.

Each step includes:
- current step number
- visited node
- structure snapshot
  - queue / stack / priority queue
- distances (for Dijkstra)
- plain-English explanation

#### Backend API
Added Flask endpoints:
- `/api/algorithm/bfs`
- `/api/algorithm/dfs`
- `/api/algorithm/dijkstra`

These endpoints accept a start node and return the traversal trace as JSON.

#### Frontend Animation
Built traversal controls:
- Run
- Next Step
- Play
- Pause
- Reset Traversal

Added animation state on the frontend:
- current trace
- current step index
- current visited node
- visited history

### Live learning features
- Sidebar updates live with:
  - Queue for BFS
  - Stack for DFS
  - Priority Queue for Dijkstra
- Dijkstra also displays distance updates
- Explanations update after every step

### Predict Mode
Built a working Predict Mode:
- Checkbox toggle to enable Predict Mode
- First step auto-reveals
- Later steps require the user to click the node they believe will be visited next
- Correct answer:
  - score increases
  - positive feedback shown
- Wrong answer:
  - guessed node flashes red
  - correct node is revealed next
  - score does not increase

### Bugs I hit
- Route existed in code but server had not been restarted
- Start node errors happened because deleted node IDs were not reused
- Traversal colors and previous runs were not resetting properly
- Predict feedback was getting overwritten by the normal explanation
- Play mode conflicted with Predict Mode

### Fixes
- Restarted Flask after new route changes
- Added traversal reset state
- Added persistent visited-node history
- Prevented Play from being used with Predict Mode enabled
- Merged correctness feedback with step explanations
- Added red/green visual feedback for prediction results

### Outcome
By the end of this push, Graph Explorer became an actual interactive learning tool, not just a graph visualizer. It now supports active recall through Predict Mode, which is the core differentiator of the project.

---

## Current Status

### Working features
- Graph editor
- Weighted undirected edges
- Node delete + incident edge cleanup
- Edge delete
- BFS animation
- DFS animation
- Dijkstra animation
- Live data structure panel
- Step explanations
- Play / Pause / Reset
- Predict Mode
- Scoring
- Correct / wrong visual feedback

### Not built yet
- SQLite save/load
- scenario presets
- polished styling
- README
- demo video

---

## Key lesson
The most important architectural decision was returning a traversal trace from the backend instead of only a final answer. That single decision made animation, explanation, and Predict Mode possible.