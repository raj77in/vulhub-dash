# 📦 vulhub-dash

A lightweight web dashboard to **browse, search, and launch [Vulhub](https://github.com/vulhub/vulhub) projects** with either **Podman** or **Docker**.
Think of it as a minimal, self-hosted Portainer built specifically for vulnerability labs.

---

## ✨ Features

- 🔍 **Auto-detects container runtime** (Podman or Docker).
- ⚡ **Launch projects** with one click:
  - Supports both **docker-compose.yml** and **Dockerfile** projects.
  - If both are present → you choose which one to run.
- 📂 **Groups projects by subdirectory** for easy navigation.
- 🖥️ **4-column responsive layout** → works even with 100+ projects.
- 🎨 **Dark/Light theme toggle** with persistence.
- ✅ Compatible with `uv` for reproducible installs & runs.

---

## 🚀 Quickstart

### 1. Clone [Vulhub](https://github.com/vulhub/vulhub)

```bash
git clone https://github.com/vulhub/vulhub
cd vulhub
````

### 2. Clone `vulhub-dash`

```bash
git clone https://github.com/YOURUSER/vulhub-dash
cd vulhub-dash
```

### 3. Install dependencies with [uv](https://github.com/astral-sh/uv)

```bash
uv add --script flask python-on-whales
```

### 4. Run the dashboard

```bash
uv run --script app.py
```

This will start the Flask app on [http://127.0.0.1:5000](http://127.0.0.1:5000).

---
## ⚙️ Configuration

* Default **base path**: `./my_projects`
  You can set a new base path from the UI (e.g., point it to your local `vulhub/` checkout).
* Default **runtime**: Podman (if installed), otherwise Docker.
* Image/container names are automatically **lowercased and sanitized** for Podman/Docker compatibility.

---

## 🛠️ Development

Run in dev mode:

```bash
uv run --script app.py
```

Auto-reloads on changes (`debug=True` in `app.py`).

---

## 📌 Roadmap

* [ ] Search bar with live filtering.
* [ ] Show container status (running/stopped).
* [ ] Stop/Restart buttons per project.
* [ ] Support remote Docker/Podman endpoints.

---

## 🤝 Contributing

PRs welcome!

1. Fork this repo
2. Create a feature branch
3. Submit a PR 🎉

---

## 📄 License

MIT License

---

**Project Links**

* Vulhub: [github.com/vulhub/vulhub](https://github.com/vulhub/vulhub)
* This repo: `https://github.com/raj77in/vulhub-dash`
