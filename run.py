import subprocess
import sys

print("Starting the FastAPI server...")
subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--reload"])

