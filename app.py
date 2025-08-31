#!/usr/bin/python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "flask",
#     "python-on-whales",
# ]
# ///
######################################################################
#
#      FileName: app
#
#
#        Author: Amit Agarwal
#   Description:
#       Version: 1.0
#       Created: 20250831 15:16:57
#      Revision: none
#        Author: Amit Agarwal (aka), <amit.agarwal@mobileum.com>
#       Company:
# Last modified: 20250831 15:16:57
#
######################################################################

import os
import shutil
import subprocess
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, session
from python_on_whales import DockerClient

app = Flask(__name__)
app.secret_key = "supersecretkey"  # replace with secure key


def detect_runtimes():
    runtimes = []
    if shutil.which("podman"):
        runtimes.append("podman")
    if shutil.which("docker"):
        runtimes.append("docker")
    return runtimes


RUNTIMES = detect_runtimes()
DEFAULT_RUNTIME = (
    "podman" if "podman" in RUNTIMES else (RUNTIMES[0] if RUNTIMES else None)
)


def find_projects(root_dir):
    """Return dict: {group: [ {path: rel, kinds:[...]} ] }"""
    grouped = {}
    if not os.path.isdir(root_dir):
        return grouped

    base = Path(root_dir).resolve()
    for path, dirs, files in os.walk(base):
        rel_path = Path(path).relative_to(base)
        if not rel_path.parts:
            continue

        kinds = []
        if "docker-compose.yml" in files or "docker-compose.yaml" in files:
            kinds.append("compose")
        if "Dockerfile" in files:
            kinds.append("dockerfile")

        if kinds:
            group = rel_path.parts[0]
            grouped.setdefault(group, []).append(
                {
                    "path": str(rel_path),
                    "kinds": kinds,  # <-- collect BOTH kinds if present
                }
            )

    # sort groups and projects inside
    return {
        g: sorted(plist, key=lambda x: x["path"])
        for g, plist in sorted(grouped.items())
    }


def run_project(path, kind, runtime, name=None, base_path="./my_projects"):
    abs_path = str(Path(base_path).resolve() / path)

    if runtime == "docker":
        if kind == "compose":
            docker = DockerClient(
                compose_files=[os.path.join(abs_path, "docker-compose.yml")]
            )
            docker.compose.up(detach=True)
        elif kind == "dockerfile":
            docker = DockerClient()
            image = docker.build(abs_path, tags=[name or Path(path).name])
            docker.run(image, detach=True, name=name or Path(path).name)

    elif runtime == "podman":
        if kind == "compose":
            subprocess.run(
                ["podman-compose", "-f", "docker-compose.yml", "up", "-d"],
                cwd=abs_path,
                check=True,
            )
        elif kind == "dockerfile":
            # image_name = name or Path(path).name
            image_name = (
                (name or Path(path).name).lower().replace("/", "-").replace(" ", "-")
            )
            subprocess.run(
                ["podman", "build", "-t", image_name, "."], cwd=abs_path, check=True
            )
            subprocess.run(
                ["podman", "run", "-d", "-P", "--name", image_name, image_name],
                cwd=abs_path,
                check=True,
            )
    else:
        raise ValueError("Invalid runtime")


@app.route("/", methods=["GET", "POST"])
def index():
    if "base_path" not in session:
        session["base_path"] = "./my_projects"  # default

    if request.method == "POST":
        if "set_base_path" in request.form:  # user updated base path
            base_path = request.form.get("base_path", "").strip()
            if os.path.isdir(base_path):
                session["base_path"] = base_path
                flash(f"Base path updated to {base_path}", "success")
            else:
                flash(f"Invalid directory: {base_path}", "danger")
            return redirect(url_for("index"))

        runtime = request.form.get("runtime") or DEFAULT_RUNTIME
        if not runtime:
            flash("No container runtime detected!", "danger")
            return redirect(url_for("index"))

        # Collect selected projects and their kinds
        selected_paths = request.form.getlist("projects")
        for spath in selected_paths:
            kind = request.form.get(f"kind_{spath}")
            try:
                run_project(spath, kind, runtime, base_path=session["base_path"])
                flash(f"Started {kind} project at {spath} using {runtime}", "success")
            except Exception as e:
                flash(f"Error starting {spath}: {e}", "danger")
        return redirect(url_for("index"))

    projects = find_projects(session["base_path"])
    return render_template(
        "index.html",
        projects=projects,
        runtimes=RUNTIMES,
        default_runtime=DEFAULT_RUNTIME,
        base_path=session["base_path"],
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
