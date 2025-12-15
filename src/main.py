
# Entrypoint: Launch Streamlit app
import os
import sys
import subprocess

if __name__ == "__main__":
	# Launch Streamlit app (src/app.py) when running main.py
	app_path = os.path.join(os.path.dirname(__file__), "app.py")
	# Use sys.executable to ensure correct Python environment
	cmd = [sys.executable, "-m", "streamlit", "run", app_path]
	print("Launching Training Progress Dashboard in your browser...")
	subprocess.run(cmd)

