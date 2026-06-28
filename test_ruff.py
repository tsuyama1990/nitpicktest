import subprocess
import os

print("Current directory:", os.getcwd())
print("Files in current directory:", os.listdir("."))
print("Running ruff...")
result = subprocess.run(["uv", "run", "ruff", "check", "."], capture_output=True, text=True)
print("Return code:", result.returncode)
print("Stdout:", result.stdout)
print("Stderr:", result.stderr)
