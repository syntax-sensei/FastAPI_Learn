import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Task Manager",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE = "http://localhost:8000"

def main():
    # Header
    st.title("✅ Task Manager")
    st.markdown("---")
    
    # Sidebar for adding tasks
    with st.sidebar:
        st.header("➕ Add New Task")
        
        # Task input form
        with st.form("add_task_form"):
            task_title = st.text_input("Task Title", placeholder="Enter your task here...")
            submit_button = st.form_submit_button("Add Task", use_container_width=True)
        
        if submit_button and task_title.strip():
            add_task(task_title.strip())
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("📋 Your Tasks")
        
        # Load and display tasks
        tasks = load_tasks()
        
        if not tasks:
            st.info("No tasks yet! Add your first task using the sidebar.")
        else:
            display_tasks(tasks)
    
    with col2:
        st.header("📊 Statistics")
        if tasks:
            total_tasks = len(tasks)
            completed_tasks = sum(1 for task in tasks if task.get('completed', False))
            pending_tasks = total_tasks - completed_tasks
            
            st.metric("Total Tasks", total_tasks)
            st.metric("Completed", completed_tasks)
            st.metric("Pending", pending_tasks)
            
            if total_tasks > 0:
                completion_rate = (completed_tasks / total_tasks) * 100
                st.progress(completion_rate / 100)
                st.caption(f"Completion Rate: {completion_rate:.1f}%")

def load_tasks():
    """Load tasks from the API"""
    try:
        response = requests.get(f"{API_BASE}/tasks")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to load tasks: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the backend server. Make sure your FastAPI server is running on http://localhost:8000")
        return []
    except Exception as e:
        st.error(f"Error loading tasks: {str(e)}")
        return []

def add_task(title):
    """Add a new task"""
    try:
        response = requests.post(
            f"{API_BASE}/tasks",
            json={"title": title}
        )
        if response.status_code == 200:
            st.success(f"✅ Task '{title}' added successfully!")
            st.rerun()
        else:
            st.error(f"Failed to add task: {response.status_code}")
    except Exception as e:
        st.error(f"Error adding task: {str(e)}")

def update_task(task_id, title, completed):
    """Update a task"""
    try:
        response = requests.put(
            f"{API_BASE}/tasks/{task_id}",
            json={"title": title, "completed": completed}
        )
        if response.status_code == 200:
            st.success("✅ Task updated successfully!")
            st.rerun()
        else:
            st.error(f"Failed to update task: {response.status_code}")
    except Exception as e:
        st.error(f"Error updating task: {str(e)}")

def delete_task(task_id):
    """Delete a task"""
    try:
        response = requests.delete(f"{API_BASE}/tasks/{task_id}")
        if response.status_code == 200:
            st.success("🗑️ Task deleted successfully!")
            st.rerun()
        else:
            st.error(f"Failed to delete task: {response.status_code}")
    except Exception as e:
        st.error(f"Error deleting task: {str(e)}")

def display_tasks(tasks):
    """Display tasks in a nice format"""
    for i, task in enumerate(tasks):
        task_id = task.get('id')
        title = task.get('title', '')
        completed = task.get('completed', False)
        
        # Create a container for each task
        with st.container():
            col1, col2, col3, col4 = st.columns([0.1, 3, 1, 1])
            
            with col1:
                # Checkbox for completion status
                new_completed = st.checkbox(
                    "✓" if completed else "☐",
                    value=completed,
                    key=f"check_{task_id}",
                    label_visibility="collapsed"
                )
                if new_completed != completed:
                    update_task(task_id, title, new_completed)
            
            with col2:
                # Task title with styling
                if completed:
                    st.markdown(f"~~**{title}**~~")
                    st.caption(f"Task #{task_id} • Completed")
                else:
                    st.markdown(f"**{title}**")
                    st.caption(f"Task #{task_id} • Pending")
            
            with col3:
                # Edit button - simplified to just trigger edit mode
                if st.button("✏️", key=f"edit_{task_id}", help="Edit task"):
                    st.session_state[f"editing_{task_id}"] = True
                    st.rerun()
            
            with col4:
                # Delete button
                if st.button("🗑️", key=f"delete_{task_id}", help="Delete task"):
                    if st.session_state.get(f"confirm_delete_{task_id}", False):
                        delete_task(task_id)
                        st.session_state[f"confirm_delete_{task_id}"] = False
                    else:
                        st.session_state[f"confirm_delete_{task_id}"] = True
                        st.warning(f"Click delete again to confirm deletion of '{title}'")
        
        # Show edit form if in edit mode
        if st.session_state.get(f"editing_{task_id}", False):
            with st.container():
                st.markdown("---")
                st.subheader(f"✏️ Edit Task #{task_id}")
                
                with st.form(f"edit_form_{task_id}"):
                    new_title = st.text_input("New task title:", value=title, key=f"edit_input_{task_id}")
                    
                    # Use buttons without columns
                    save_button = st.form_submit_button("💾 Save Changes")
                    cancel_button = st.form_submit_button("❌ Cancel")
                    
                    if save_button:
                        if new_title.strip():
                            update_task(task_id, new_title.strip(), completed)
                            st.session_state[f"editing_{task_id}"] = False
                        else:
                            st.error("Task title cannot be empty!")
                    
                    if cancel_button:
                        st.session_state[f"editing_{task_id}"] = False
                        st.rerun()
        
        # Add some spacing between tasks
        st.markdown("---")

if __name__ == "__main__":
    main() 