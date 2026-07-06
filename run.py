import os
import sys
import time
import subprocess
import signal

# Track child processes
processes = []

def cleanup():
    """Terminate all running subprocesses."""
    print("\nShutting down Personalized Networking Assistant processes...")
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=2)
            print(f"Terminated process with PID: {p.pid}")
        except Exception:
            try:
                p.kill()
                print(f"Killed process with PID: {p.pid}")
            except Exception:
                pass

def signal_handler(sig, frame):
    """Handle termination signals like Ctrl+C."""
    cleanup()
    sys.exit(0)

# Register signal handler for SIGINT (Ctrl+C) and SIGTERM
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Start FastAPI Backend
    print("Starting FastAPI Backend...")
    # Using python -m uvicorn ensures it uses the same python environment
    backend_cmd = [
        sys.executable, "-m", "uvicorn", 
        "backend.app.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000"
    ]
    
    try:
        backend_proc = subprocess.Popen(
            backend_cmd,
            cwd=workspace_dir,
            stdout=None,  # Inherit stdout so user can see backend logs
            stderr=None
        )
        processes.append(backend_proc)
        print(f"Backend started with PID: {backend_proc.pid}")
    except Exception as e:
        print(f"Error starting FastAPI backend: {e}")
        sys.exit(1)
        
    # Wait a moment for backend to initialize database
    time.sleep(2)
    
    # 2. Start Streamlit Frontend
    print("\nStarting Streamlit Frontend...")
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run", 
        "frontend/app.py", 
        "--server.port", "8501"
    ]
    
    try:
        frontend_proc = subprocess.Popen(
            frontend_cmd,
            cwd=workspace_dir,
            stdout=None,
            stderr=None
        )
        processes.append(frontend_proc)
        print(f"Frontend started with PID: {frontend_proc.pid}")
    except Exception as e:
        print(f"Error starting Streamlit frontend: {e}")
        cleanup()
        sys.exit(1)
        
    print("\n" + "="*50)
    print("Personalized Networking Assistant is running!")
    print("Backend API:   http://127.0.0.1:8000")
    print("Streamlit UI:  http://127.0.0.1:8501")
    print("Press Ctrl+C to stop both servers.")
    print("="*50 + "\n")
    
    # Keep the main thread alive and monitor processes
    try:
        while True:
            for p in processes:
                # Check if any process has exited unexpectedly
                poll = p.poll()
                if poll is not None:
                    print(f"\nProcess with PID {p.pid} exited with code {poll}.")
                    cleanup()
                    sys.exit(poll)
            time.sleep(1)
    except SystemExit:
        pass
    except Exception as e:
        print(f"Monitoring error: {e}")
        cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()
