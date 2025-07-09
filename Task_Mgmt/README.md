# 📋 Task Management System

A simple and efficient task management application built with **FastAPI** backend and **Streamlit** frontend.

## 🚀 Features

- ✅ **Create Tasks** - Add new tasks with titles
- ✅ **View Tasks** - Display all tasks in a clean interface
- ✅ **Update Tasks** - Mark tasks as complete/incomplete
- ✅ **Edit Tasks** - Modify task titles
- ✅ **Delete Tasks** - Remove tasks with confirmation
- ✅ **Statistics Dashboard** - Track completion progress
- ✅ **Real-time Updates** - Instant UI updates after actions

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for running FastAPI applications

### Frontend
- **Streamlit** - Rapid web app development framework
- **Requests** - HTTP library for API communication


### Running the Application

1. **Start the FastAPI backend server**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at: `http://localhost:8000`

2. **Start the Streamlit frontend** (in a new terminal)
   ```bash
   streamlit run streamlit_app.py
   ```
   The web interface will be available at: `http://localhost:8501`

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tasks` | Get all tasks |
| `POST` | `/tasks` | Create a new task |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |


