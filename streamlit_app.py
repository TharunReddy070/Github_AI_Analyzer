import streamlit as st
import os
import sys

# Print debug information
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
print(f"Python path: {sys.path}")

# Add the current directory to the path to ensure proper importing
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
print(f"Added {current_dir} to sys.path")

try:
    # Import the main app
    from app.streamlit_app import main
    print("Successfully imported main function")
    
    # Run the main function
    if __name__ == "__main__":
        main()
except ImportError as e:
    st.error(f"Error importing main app: {e}")
    st.write(f"Current directory: {os.getcwd()}")
    st.write(f"Files in current directory: {os.listdir('.')}")
    if os.path.exists('app'):
        st.write(f"Files in app directory: {os.listdir('app')}")
    st.write(f"Python path: {sys.path}") 