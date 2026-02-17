from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

tasks = []
task_id = 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")
    if status == "completed":
        return jsonify([t for t in tasks if t["completed"]])
    if status == "active":
        return jsonify([t for t in tasks if not t["completed"]])
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def create_task():
    global task_id
    data = request.json

    if not data or not data.get("title"):
        return jsonify({"error": "Title required"}), 400

    task = {
        "id": task_id,
        "title": data["title"],
        "completed": False,
        "priority": data.get("priority", "Medium")
    }
    tasks.append(task)
    task_id += 1
    return jsonify(task), 201

@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json
    for t in tasks:
        if t["id"] == id:
            t["title"] = data.get("title", t["title"])
            t["completed"] = data.get("completed", t["completed"])
            t["priority"] = data.get("priority", t["priority"])
            return jsonify(t)
    return jsonify({"error": "Task not found"}), 404

@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    global tasks
    if any(t["id"] == id for t in tasks):
        tasks = [t for t in tasks if t["id"] != id]
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Task not found"}), 404

# 🔥 TESTLER İÇİN RESET ENDPOINT
@app.route("/api/reset", methods=["POST"])
def reset_tasks():
    global tasks, task_id
    tasks = []
    task_id = 1
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
