const canvas = document.getElementById("graphCanvas");
const context = canvas.getContext("2d");

const graphState = {
    nodes: [],
    edges: []
};

const NODE_RADIUS = 20;
let selectedNode = null;

let currentTrace = [];
let currentStepIndex = -1;
let currentVisitedNodeId = null;
let visitedNodes = [];

function drawNode(node) {
    context.beginPath();
    context.arc(node.x, node.y, NODE_RADIUS, 0, Math.PI * 2);

    if (node.id === currentVisitedNodeId) {
        context.fillStyle = "#27ae60";
    } else if (visitedNodes.includes(node.id)) {
        context.fillStyle = "#7DCEA0";
    } else {
        context.fillStyle = "#4A90D9";
    }

    context.fill();

    context.lineWidth = 2;
    context.strokeStyle = "#ffffff";
    context.stroke();

    context.fillStyle = "#ffffff";
    context.font = "bold 14px Arial";
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText(node.label, node.x, node.y);
}

function drawSelectedNode(node) {
    context.beginPath();
    context.arc(node.x, node.y, NODE_RADIUS + 4, 0, Math.PI * 2);
    context.strokeStyle = "#f39c12";
    context.lineWidth = 3;
    context.stroke();
}

function drawEdge(edge) {
    const sourceNode = graphState.nodes.find(node => node.id === edge.source);
    const targetNode = graphState.nodes.find(node => node.id === edge.target);

    if (!sourceNode || !targetNode) {
        return;
    }

    context.beginPath();
    context.moveTo(sourceNode.x, sourceNode.y);
    context.lineTo(targetNode.x, targetNode.y);
    context.strokeStyle = "#333333";
    context.lineWidth = 2;
    context.stroke();

    const midX = (sourceNode.x + targetNode.x) / 2;
    const midY = (sourceNode.y + targetNode.y) / 2;

    context.fillStyle = "#111111";
    context.font = "12px Arial";
    context.textAlign = "center";
    context.textBaseline = "bottom";
    context.fillText(edge.weight, midX, midY - 6);
}

function redrawGraph() {
    context.clearRect(0, 0, canvas.width, canvas.height);

    for (const edge of graphState.edges) {
        drawEdge(edge);
    }

    for (const node of graphState.nodes) {
        drawNode(node);
    }

    if (selectedNode) {
        drawSelectedNode(selectedNode);
    }
}

function loadGraph() {
    fetch("/api/graph")
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Failed to load graph");
            }
            return response.json();
        })
        .then(function (graph) {
            graphState.nodes = graph.nodes || [];
            graphState.edges = graph.edges || [];
            selectedNode = null;
            redrawGraph();
        })
        .catch(function (error) {
            console.error("Error loading graph:", error);
        });
}

function addNode(x, y) {
    fetch("/api/node", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ x, y })
    })
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Failed to create node");
            }
            return response.json();
        })
        .then(function (node) {
            graphState.nodes.push(node);
            redrawGraph();
        })
        .catch(function (error) {
            console.error("Error adding node:", error);
        });
}

function addEdge(sourceId, targetId, weight) {
    fetch("/api/edge", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            source: sourceId,
            target: targetId,
            weight: weight
        })
    })
        .then(function (response) {
            return response.json().then(function (data) {
                return {
                    ok: response.ok,
                    data: data
                };
            });
        })
        .then(function (result) {
            if (!result.ok) {
                throw new Error(result.data.error || "Failed to create edge");
            }

            graphState.edges.push(result.data);
            selectedNode = null;
            redrawGraph();
        })
        .catch(function (error) {
            console.error("Error adding edge:", error);
            alert(error.message);
            selectedNode = null;
            redrawGraph();
        });
}

function getNodeAtPosition(x, y) {
    for (const node of graphState.nodes) {
        const distance = Math.hypot(x - node.x, y - node.y);
        if (distance <= NODE_RADIUS) {
            return node;
        }
    }
    return null;
}


function deleteNode(nodeId) {
    fetch(`/api/node/${nodeId}`, {
        method: "DELETE"
    })
        .then(function (response) {
            return response.json().then(function (data) {
                return {
                    ok: response.ok,
                    data: data
                };
            });
        })
        .then(function (result) {
            if (!result.ok) {
                throw new Error(result.data.error || "Failed to delete node");
            }

            graphState.nodes = graphState.nodes.filter(function (node) {
                return node.id !== nodeId;
            });

            graphState.edges = graphState.edges.filter(function (edge) {
                return edge.source !== nodeId && edge.target !== nodeId;
            });

            if (selectedNode && selectedNode.id === nodeId) {
                selectedNode = null;
            }

            redrawGraph();
        })
        .catch(function (error) {
            console.error("Error deleting node:", error);
            alert(error.message);
        });
}


function distanceToSegment(px, py, x1, y1, x2, y2) {
    const dx = x2 - x1;
    const dy = y2 - y1;

    if (dx === 0 && dy === 0) {
        return Math.hypot(px - x1, py - y1);
    }

    const t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy);
    const clampedT = Math.max(0, Math.min(1, t));

    const closestX = x1 + clampedT * dx;
    const closestY = y1 + clampedT * dy;

    return Math.hypot(px - closestX, py - closestY);
}


function getEdgeAtPosition(x, y) {
    const EDGE_HITBOX = 8;

    for (const edge of graphState.edges) {
        const sourceNode = graphState.nodes.find(function (node) {
            return node.id === edge.source;
        });

        const targetNode = graphState.nodes.find(function (node) {
            return node.id === edge.target;
        });

        if (!sourceNode || !targetNode) {
            continue;
        }

        const distance = distanceToSegment(
            x,
            y,
            sourceNode.x,
            sourceNode.y,
            targetNode.x,
            targetNode.y
        );

        if (distance <= EDGE_HITBOX) {
            return edge;
        }
    }

    return null;
}


function deleteEdge(sourceId, targetId) {
    fetch("/api/edge", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            source: sourceId,
            target: targetId
        })
    })
        .then(function (response) {
            return response.json().then(function (data) {
                return {
                    ok: response.ok,
                    data: data
                };
            });
        })
        .then(function (result) {
            if (!result.ok) {
                throw new Error(result.data.error || "Failed to delete edge");
            }

            graphState.edges = graphState.edges.filter(function (edge) {
                const sameDirection = edge.source === sourceId && edge.target === targetId;
                const reverseDirection = edge.source === targetId && edge.target === sourceId;
                return !(sameDirection || reverseDirection);
            });

            redrawGraph();
        })
        .catch(function (error) {
            console.error("Error deleting edge:", error);
            alert(error.message);
        });
}


function runAlgorithm() {
    const algorithm = document.getElementById("algorithmSelect").value;
    const startNodeInput = prompt("Enter start node id");
    visitedNodes = [];

    if (startNodeInput === null) {
        return;
    }

    const startNode = Number(startNodeInput);

    if (!Number.isInteger(startNode) || startNode <= 0) {
        alert("Start node must be a positive integer");
        return;
    }

    fetch(`/api/algorithm/${algorithm}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ start_node: startNode })
    })
        .then(function (response) {
            return response.json().then(function (data) {
                return {
                    ok: response.ok,
                    data: data
                };
            });
        })
        .then(function (result) {
            if (!result.ok) {
                throw new Error(result.data.error || "Failed to run algorithm");
            }

            currentTrace = result.data.steps || [];
            currentStepIndex = -1;
            currentVisitedNodeId = null;

            updateAlgorithmOutput("Algorithm loaded. Click Next Step.");
            redrawGraph();
            updateDataStructurePanel([]);
        })
        .catch(function (error) {
            console.error("Error running algorithm:", error);
            alert(error.message);
        });
}


function showNextStep() {
    if (currentTrace.length === 0) {
        alert("Run an algorithm first");
        return;
    }

    if (currentStepIndex + 1 >= currentTrace.length) {
        alert("No more steps");
        return;
    }

    currentStepIndex += 1;
    const step = currentTrace[currentStepIndex];

    currentVisitedNodeId = step.visited;

    if (!visitedNodes.includes(step.visited)) {
        visitedNodes.push(step.visited);
    }

    redrawGraph();
    updateAlgorithmOutput(step.explanation);
    updateDataStructurePanel(step.structure, step.distances);
}


function updateAlgorithmOutput(text) {
    const output = document.getElementById("algorithmOutput");
    output.innerHTML = `<p class="visited-note">${text}</p>`;
}

function updateDataStructurePanel(structure, distances = null) {
    const panel = document.getElementById("ds-panel");
    const algorithm = document.getElementById("algorithmSelect").value;

    let html = `
        <p><strong>Controls</strong></p>
        <p>Left click empty space → add node</p>
        <p>Left click node, then another node → add edge</p>
        <p>Right click node → delete node</p>
        <p>Right click edge → delete edge</p>
    `;

    if (algorithm === "bfs") {
        html += `<p><strong>Queue:</strong> ${JSON.stringify(structure)}</p>`;
    } else if (algorithm === "dfs") {
        html += `<p><strong>Stack:</strong> ${JSON.stringify(structure)}</p>`;
    } else if (algorithm === "dijkstra") {
        html += `<p><strong>Priority Queue:</strong> ${JSON.stringify(structure)}</p>`;
    }

    if (distances) {
        html += `<p><strong>Distances:</strong> ${JSON.stringify(distances)}</p>`;
    }

    panel.innerHTML = html;
}


canvas.addEventListener("click", function (event) {
    const canvasBox = canvas.getBoundingClientRect();
    const x = Math.round(event.clientX - canvasBox.left);
    const y = Math.round(event.clientY - canvasBox.top);

    const clickedNode = getNodeAtPosition(x, y);

    if (!clickedNode) {
        selectedNode = null;
        addNode(x, y);
        return;
    }

    if (selectedNode === null) {
        selectedNode = clickedNode;
        redrawGraph();
        return;
    }

    if (selectedNode.id === clickedNode.id) {
        selectedNode = null;
        redrawGraph();
        return;
    }

    let weight = prompt("Enter edge weight", "1");

    if (weight === null) {
        selectedNode = null;
        redrawGraph();
        return;
    }

    weight = Number(weight);

    if (!Number.isFinite(weight) || weight <= 0) {
        alert("Weight must be a positive number");
        selectedNode = null;
        redrawGraph();
        return;
    }

    addEdge(selectedNode.id, clickedNode.id, weight);
});


canvas.addEventListener("contextmenu", function (event) {
    event.preventDefault();

    const canvasBox = canvas.getBoundingClientRect();
    const x = Math.round(event.clientX - canvasBox.left);
    const y = Math.round(event.clientY - canvasBox.top);

    const clickedNode = getNodeAtPosition(x, y);    

    if (clickedNode) {
        deleteNode(clickedNode.id);
        return;
    }

    const clickedEdge = getEdgeAtPosition(x, y);

    if (clickedEdge) {
        deleteEdge(clickedEdge.source, clickedEdge.target);
    }
});


document.getElementById("runAlgorithmBtn").addEventListener("click", runAlgorithm);
document.getElementById("nextStepBtn").addEventListener("click", showNextStep);

loadGraph();