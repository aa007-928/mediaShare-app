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
             │  NSFW Classifier  │  Database │    │ ImageKit │
             │ (ViT Transformer) │  (Users,  │    │   CDN    │
             │  Content Filter)  │  Posts)   │    │ (Storage)│
             └───────────────────┘  └────────┘    └──────────┘
