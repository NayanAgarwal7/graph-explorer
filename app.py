from flask import Flask, render_template, request, jsonify
from algorithms import bfs_trace, dfs_trace, dijkstra_trace
from db import init_db, save_graph, load_graph, list_graphs

app = Flask(__name__)
init_db()

graph = {
    "nodes": [],
    "edges": []
}


def find_node(node_id):
    for node in graph["nodes"]:
        if node["id"] == node_id:
            return node
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/graph")
def get_graph():
    return jsonify(graph)


@app.route("/api/graph/reset", methods=["POST"])
def reset_graph():
    graph["nodes"].clear()
    graph["edges"].clear()
    return jsonify({"ok": True})


@app.route("/api/graph/save", methods=["POST"])
def save_current_graph():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    name = data.get("name")

    if not name or not str(name).strip():
        return jsonify({"error": "Graph name is required"}), 400

    save_graph(name.strip(), graph)

    return jsonify({
        "ok": True,
        "message": f"Graph '{name.strip()}' saved successfully"
    })


@app.route("/api/graphs", methods=["GET"])
def get_saved_graphs():
    graphs = list_graphs()
    return jsonify(graphs)


@app.route("/api/graph/load/<string:name>", methods=["GET"])
def load_saved_graph(name):
    saved_graph = load_graph(name)

    if saved_graph is None:
        return jsonify({"error": "Graph not found"}), 404

    graph["nodes"] = saved_graph.get("nodes", [])
    graph["edges"] = saved_graph.get("edges", [])

    return jsonify({
        "ok": True,
        "graph": graph
    })


@app.route("/api/node", methods=["POST"])
def add_node():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    x = data.get("x")
    y = data.get("y")

    if x is None or y is None:
        return jsonify({"error": "x and y are required"}), 400

    if not graph["nodes"]:
        next_id = 1
    else:
        next_id = max(node["id"] for node in graph["nodes"]) + 1

    node = {
        "id": next_id,
        "label": str(next_id),
        "x": x,
        "y": y
    }

    graph["nodes"].append(node)
    return jsonify(node), 201


@app.route("/api/edge", methods=["POST"])
def add_edge():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    source = data.get("source")
    target = data.get("target")
    weight = data.get("weight", 1)

    if source is None or target is None:
        return jsonify({"error": "source and target are required"}), 400

    if find_node(source) is None or find_node(target) is None:
        return jsonify({"error": "Invalid node id"}), 400

    if source == target:
        return jsonify({"error": "Self-loops not allowed right now"}), 400

    for edge in graph["edges"]:
        same_direction = edge["source"] == source and edge["target"] == target
        reverse_direction = edge["source"] == target and edge["target"] == source

        if same_direction or reverse_direction:
            return jsonify({"error": "Edge already exists"}), 400

    edge = {
        "source": source,
        "target": target,
        "weight": weight
    }

    graph["edges"].append(edge)
    return jsonify(edge), 201

@app.route("/api/node/<int:node_id>", methods=["DELETE"])
def delete_node(node_id):
    node = find_node(node_id)

    if node is None:
        return jsonify({"error": "Node not found"}), 404

    graph["nodes"] = [current_node for current_node in graph["nodes"] if current_node["id"] != node_id]
    graph["edges"] = [
        edge for edge in graph["edges"]
        if edge["source"] != node_id and edge["target"] != node_id
    ]

    return jsonify({"ok": True})


@app.route("/api/edge", methods=["DELETE"])
def delete_edge():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    source = data.get("source")
    target = data.get("target")

    if source is None or target is None:
        return jsonify({"error": "source and target are required"}), 400

    original_count = len(graph["edges"])

    graph["edges"] = [
        edge for edge in graph["edges"]
        if not (
            (edge["source"] == source and edge["target"] == target) or
            (edge["source"] == target and edge["target"] == source)
        )
    ]

    if len(graph["edges"]) == original_count:
        return jsonify({"error": "Edge not found"}), 404

    return jsonify({"ok": True})


@app.route("/api/algorithm/bfs", methods=["POST"])
def run_bfs():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    start_node = data.get("start_node")

    if start_node is None:
        return jsonify({"error": "start_node is required"}), 400

    result = bfs_trace(graph, start_node)

    if result["error"] is not None:
        return jsonify({"error": result["error"]}), 400

    return jsonify(result)


@app.route("/api/algorithm/dfs", methods=["POST"])
def run_dfs():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    start_node = data.get("start_node")

    if start_node is None:
        return jsonify({"error": "start_node is required"}), 400

    result = dfs_trace(graph, start_node)

    if result["error"] is not None:
        return jsonify({"error": result["error"]}), 400

    return jsonify(result)


@app.route("/api/algorithm/dijkstra", methods=["POST"])
def run_dijkstra():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    start_node = data.get("start_node")

    if start_node is None:
        return jsonify({"error": "start_node is required"}), 400

    result = dijkstra_trace(graph, start_node)

    if result["error"] is not None:
        return jsonify({"error": result["error"]}), 400

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)