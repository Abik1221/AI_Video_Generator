import os

def log(msg):
    with open("env_debug.txt", "a") as f:
        f.write(msg + "\n")

env_path = os.path.join(os.getcwd(), 'server', '.env')
log(f"Checking {env_path}")
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if "GOOGLE_GEMINI_API_KEY" in line:
                log(f"Found line: {line.strip()}")
else:
    log(".env file not found")
