from collections import deque
import heapq


def build_adjacency_list(graph):
    adjacency = {node["id"]: [] for node in graph["nodes"]}

    for edge in graph["edges"]:
        source = edge["source"]
        target = edge["target"]
        weight = edge.get("weight", 1)

        adjacency[source].append({
            "node": target,
            "weight": weight
        })
        adjacency[target].append({
            "node": source,
            "weight": weight
        })

    for node_id in adjacency:
        adjacency[node_id].sort(key=lambda neighbor: neighbor["node"])

    return adjacency


def bfs_trace(graph, start_node):
    adjacency = build_adjacency_list(graph)

    if start_node not in adjacency:
        return {
            "algorithm": "bfs",
            "steps": [],
            "error": "Start node not found"
        }

    visited = {start_node}
    queue = deque([start_node])
    steps = []
    step_number = 1

    while queue:
        current = queue.popleft()
        added_neighbors = []

        for neighbor in adjacency[current]:
            neighbor_id = neighbor["node"]

            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append(neighbor_id)
                added_neighbors.append(neighbor_id)

        if step_number == 1:
            explanation = f"Start at node {current}."
            if added_neighbors:
                explanation += f" Enqueue neighbors {added_neighbors}."
            else:
                explanation += " It has no unvisited neighbors."
        else:
            explanation = f"Visit node {current}."
            if added_neighbors:
                explanation += f" Enqueue neighbors {added_neighbors}."
            else:
                explanation += " No new neighbors were added."

        steps.append({
            "step": step_number,
            "visited": current,
            "structure": list(queue),
            "distances": None,
            "explanation": explanation
        })

        step_number += 1

    return {
        "algorithm": "bfs",
        "steps": steps,
        "error": None
    }


def dfs_trace(graph, start_node):
    adjacency = build_adjacency_list(graph)

    if start_node not in adjacency:
        return {
            "algorithm": "dfs",
            "steps": [],
            "error": "Start node not found"
        }

    visited = set()
    stack = [start_node]
    steps = []
    step_number = 1

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        added_neighbors = []

        neighbors = adjacency[current]
        for neighbor in reversed(neighbors):
            neighbor_id = neighbor["node"]

            if neighbor_id not in visited:
                stack.append(neighbor_id)
                added_neighbors.append(neighbor_id)

        if step_number == 1:
            explanation = f"Start at node {current}."
            if added_neighbors:
                explanation += f" Push neighbors {list(reversed(added_neighbors))} onto the stack."
            else:
                explanation += " It has no unvisited neighbors."
        else:
            explanation = f"Visit node {current}."
            if added_neighbors:
                explanation += f" Push neighbors {list(reversed(added_neighbors))} onto the stack."
            else:
                explanation += " No new neighbors were added."

        steps.append({
            "step": step_number,
            "visited": current,
            "structure": list(stack),
            "distances": None,
            "explanation": explanation
        })

        step_number += 1

    return {
        "algorithm": "dfs",
        "steps": steps,
        "error": None
    }


def dijkstra_trace(graph, start_node):
    adjacency = build_adjacency_list(graph)

    if start_node not in adjacency:
        return {
            "algorithm": "dijkstra",
            "steps": [],
            "error": "Start node not found"
        }

    distances = {node_id: float("inf") for node_id in adjacency}
    distances[start_node] = 0

    priority_queue = [(0, start_node)]
    visited = set()
    steps = []
    step_number = 1

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)
        relaxed_neighbors = []

        for neighbor in adjacency[current]:
            neighbor_id = neighbor["node"]
            weight = neighbor["weight"]
            new_distance = current_distance + weight

            if new_distance < distances[neighbor_id]:
                distances[neighbor_id] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor_id))
                relaxed_neighbors.append({
                    "node": neighbor_id,
                    "distance": new_distance
                })

        if step_number == 1:
            explanation = f"Start at node {current} with distance 0."
        else:
            explanation = f"Visit node {current} with current shortest distance {current_distance}."

        if relaxed_neighbors:
            updated_text = ", ".join(
                f"{item['node']} -> {item['distance']}"
                for item in relaxed_neighbors
            )
            explanation += f" Updated distances: {updated_text}."
        else:
            explanation += " No shorter paths were found."

        structure_snapshot = [
            {"node": node_id, "distance": distance}
            for distance, node_id in sorted(priority_queue)
        ]

        distances_snapshot = {
            node_id: (None if value == float("inf") else value)
            for node_id, value in distances.items()
        }

        steps.append({
            "step": step_number,
            "visited": current,
            "structure": structure_snapshot,
            "distances": distances_snapshot,
            "explanation": explanation
        })

        step_number += 1

    return {
        "algorithm": "dijkstra",
        "steps": steps,
        "error": None
    }