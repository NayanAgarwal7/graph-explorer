from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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

   
if __name__ == "__main__":
    app.run(debug=True)