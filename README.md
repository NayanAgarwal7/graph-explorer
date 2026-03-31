# Graph Explorer

Graph Explorer is an interactive graph algorithm learning tool built with Flask, Python, JavaScript, HTML, and CSS.

## Tagline
**Don't just watch algorithms run. Learn to think like them.**

## Why I built it
Many students watch BFS, DFS, and Dijkstra animations but still struggle to predict what happens next on a new graph. Passive watching does not build real intuition.

Graph Explorer is designed to turn graph traversal into active learning.

## Core idea
Users build their own graph directly in the browser, choose an algorithm, and step through the traversal visually.

Instead of only showing the result, the backend returns a full step-by-step trace. The frontend uses that trace to animate the traversal, display the live data structure state, and support Predict Mode.

## Features
- Add nodes by clicking on the canvas
- Add weighted edges by selecting two nodes
- Delete nodes with right click
- Delete edges with right click
- BFS traversal animation
- DFS traversal animation
- Dijkstra traversal animation
- Live queue / stack / priority queue display
- Step-by-step explanation panel
- Play, Pause, Next Step, and Reset Traversal controls
- Predict Mode with scoring
- Visual red/green feedback for wrong and correct predictions

## Tech stack
- Python
- Flask
- JavaScript
- HTML
- CSS

## Algorithms implemented
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Dijkstra's Algorithm

All algorithms were implemented from scratch.

## Project structure
graphexplorer/
├── app.py
├── algorithms.py
├── db.py
├── explainer.py
├── schema.sql
├── DEVLOG.md
├── requirements.txt
├── static/
│   ├── graph.js
│   └── style.css
└── templates/
    └── index.html

## How to run
1. Create and activate a virtual environment
2. Install dependencies
3. Run the Flask app
4. Open the local server in the browser

python -m venv venv
venv\Scripts\activate
pip install flask
python app.py

Then open: http://127.0.0.1:5000

## Current status

Working prototype completed:
- Graph editor works
- Traversal animation works
- Predict Mode works

Planned next:
- SQLite save/load
- Real-world graph presets
- Improved UI polish
- Demo video