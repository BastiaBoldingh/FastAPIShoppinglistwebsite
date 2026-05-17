import subprocess

if __name__ == "__main__":
    print("Starting the FastAPI server...")
    subprocess.run(["uvicorn", "app.main:app", "--reload"])

