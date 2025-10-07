# NeuroCare for All 

This is a Python-based web application for the NeuroCare for All project. It uses Flask to serve a web page that captures video from your webcam, sends it to a Python backend for analysis, and displays a "Focus Score" in real-time.

## Getting Started

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**
    -   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    -   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  Open your web browser and navigate to `http://127.0.0.1:5000`.
