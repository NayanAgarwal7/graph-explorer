# Graph Explorer

Graph Explorer is an interactive graph algorithm learning tool built with Flask, Python, JavaScript, HTML, CSS, and SQLite.

## Tagline
**Don't just watch algorithms run. Learn to think like them.**

## Video Demo: 
https://youtu.be/3UnpI44tTy

## Overview
Many students can follow a graph traversal animation when they watch it passively, but still struggle to predict what happens next on a new graph.

Graph Explorer was built to solve that problem through interaction.

It combines:
- a custom graph editor
- step-by-step algorithm animation
- live queue / stack / priority queue display
- Predict Mode with scoring
- demo scenarios with meaningful real-world interpretations

## Core Features

### Graph Editor
- Add nodes by left clicking on empty canvas space
- Add weighted edges by clicking one node and then another
- Delete nodes with right click
- Delete edges with right click

### Algorithms
Implemented from scratch:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Dijkstra’s Algorithm

### Traversal Controls
- Run
- Next Step
- Play
- Pause
- Reset Traversal

### Learning Features
- Live queue display for BFS
- Live stack display for DFS
- Live priority queue and distance updates for Dijkstra
- Plain-English explanation after every step
- Predict Mode with score tracking
- Green / red visual feedback for correct and wrong predictions

### Demo + Sandbox Design
Graph Explorer supports two types of use:

#### 1. Demo Scenarios
Built-in example graphs:
- City Map
- Social Network
- Course Prerequisites

These help users understand where graph algorithms are useful in real-world style situations.

#### 2. Custom Graph Mode
Users can build, save, load, and explore their own graphs.

This makes the project both:
- a learning demo
- and a personal graph sandbox

## Why This Project Is Useful
Graph Explorer is designed for students who want to build actual intuition for graph algorithms, not just memorize definitions.

It helps users answer questions like:
- Which node will BFS visit next?
- Why does DFS go deep before backtracking?
- How does Dijkstra choose the next cheapest node?
- How do queue, stack, and priority queue states change over time?

## Tech Stack
- Python
- Flask
- JavaScript
- HTML
- CSS
- SQLite

## Project Structure
```text
graphexplorer/
├── app.py
├── algorithms.py
├── db.py
├── schema.sql
├── DEVLOG.md
├── README.md
├── requirements.txt
├── static/
│   ├── graph.js
│   └── style.css
└── templates/
    └── index.html