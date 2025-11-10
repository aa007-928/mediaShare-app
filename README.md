# 🖼️ Media Share  
**A full-stack AI-powered media sharing platform built with FastAPI + Streamlit**

> 🚀 An intelligent, privacy-aware social app for sharing images and videos with automatic NSFW filtering, JWT-based authentication, and a modern Streamlit UI.

---

## ✨ Overview

**Media Share** is a next-generation content-sharing app that lets users **upload, view, and manage** image or video posts in a global feed — powered by **AI-based content moderation** to ensure a safe and positive environment.

- 🧠 **AI moderation** using a Visual Transformer model to block NSFW uploads.  
- 🔐 **JWT-based authentication** for secure login, signup, and authorization.  
- 🖼️ **Image & video uploads** supported with automatic cloud storage.  
- 🌍 **Feed section** displays posts from all users in real-time.  
- 🧾 **Ownership control** — only the uploader can delete their own posts.  
- ⚡ Built with **FastAPI** (backend) and **Streamlit** (frontend).  
- 🧩 Managed using **uv**, the modern Python package & environment manager.

---

## 🏗️ Architecture

```text
        ┌──────────────────────────────┐
        │          Streamlit UI        │
        │  ──────────────────────────  │
        │  - Login / Signup form       │
        │  - File uploader             │
        │  - Feed view (all posts)     │
        │  - Delete post (if owner)    │
        └──────────────┬───────────────┘
                       │ REST API calls (JWT)
        ┌──────────────┴───────────────┐
        │          FastAPI API         │
        │  - Auth endpoints            │
        │  - Upload/Filter/Delete      │
        │  - Database operations       │
        │  - NSFW moderation pipeline  │
        └──────────────┬───────────────┬──────────────┐
                       │               │              │
             ┌─────────┘         ┌─────┴────┐    ┌────┴─────┐
             │  NSFW Classifier  │  Database│    │ ImageKit │
             │ (ViT Transformer, │  (Users, │    │   CDN    │
             │  Content Filter)  │  Posts)  │    │ (Storage)│
             └───────────────────┘ └────────┘    └──────────┘

```
---
# 🚀 Getting Started
## 🧩 Prerequisites

Before you begin, make sure you have the following installed:

- 🐍 Python 3.9+
- ⚡ uv — a modern package & environment manager
- ☁️ ImageKit.io account — for cloud media uploads and CDN storage
- 🗝️ API credentials for ImageKit and a secret key for JWT authentication

## ⚙️ Environment Setup
1. Clone the repository
2. Create and sync environment with : uv sync
3. Set up environment variables in a .env file in the root directory
```text
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_project_id/
SECRET=your_jwt_secret
DATABASE_URL=sqlite+aiosqlite:///./media_share.db
   ```
## 🧠 Run the Application
1. Start the FastAPI backend
   ```
   uv run main.py
   ```
3. Start the Streamlit frontend
   ```
   uv run streamlit run app-frontend.py
   ```

## 🗂️ Project Structure
```text
media-share/
│
├── main.py                  # FastAPI backend entrypoint (upload, auth, moderation, etc.)
├── app-frontend.py          # Streamlit frontend (UI: upload, feed, delete)
│
├── app/
│   ├── __init__.py
│   ├── app.py               # FastAPI app setup (routers, middleware)
│   ├── db.py                # Async DB setup (SQLAlchemy models & session)
│   ├── filter.py            # NSFW filtering (Falconsai/nsfw_image_detection)
│   ├── images.py            # ImageKit upload client initialization
│   ├── schemas.py           # Pydantic models (User, Post)
│   ├── users.py             # JWT authentication, signup/login logic
│
├── .env                     # Environment variables (JWT, ImageKit, DB)
├── pyproject.toml           # Managed by uv (dependencies, entrypoints)
└── README.md

```

