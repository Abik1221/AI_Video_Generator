import subprocess
import time
import requests
import os
import signal
import sys
import json

def log(msg):
    print(f"[Portal Setup] {msg}")

def kill_process_by_name(name):
    subprocess.run(["pkill", "-f", name])

def main():
    log("Cleaning up old processes...")
    kill_process_by_name("ngrok")
    kill_process_by_name("vite")
    kill_process_by_name("npm run dev")
    
    time.sleep(2)
    
    # Detect ngrok command
    ngrok_cmd = "ngrok"
    if subprocess.call("which ngrok", shell=True) != 0:
        log("ngrok not found in PATH, trying npx ngrok...")
        ngrok_cmd = "npx -y ngrok"
    
    # 1. Start Ngrok with Config
    log(f"Starting Ngrok Tunnels using '{ngrok_cmd}'...")
    
    # We use full shell command to redirect output
    full_cmd = f"{ngrok_cmd} start --all --config=ngrok.yml > ngrok_multi.log 2>&1 &"
    subprocess.Popen(full_cmd, shell=True)
    
    log("Waiting 10 seconds for tunnels to initialize...")
    time.sleep(10)
    
    # 2. Get Public URLs
    backend_url = None
    frontend_url = None
    
    try:
        # Ngrok provides a local API to inspect tunnels
        response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=5)
        data = response.json()
        
        tunnels = data.get("tunnels", [])
        log(f"Found {len(tunnels)} active tunnels.")
        
        for t in tunnels:
            addr = t.get("config", {}).get("addr", "")
            public_url = t.get("public_url", "")
            
            if "8000" in addr:
                backend_url = public_url
            elif "3000" in addr:
                frontend_url = public_url
                
    except Exception as e:
        log(f"Error fetching tunnel info: {e}")
        log("Dumping ngrok_multi.log:")
        try:
            with open("ngrok_multi.log", "r") as f:
                print(f.read())
        except:
            print("Could not read ngrok_multi.log")
        return

    if not backend_url or not frontend_url:
        log("FAILED to get both URLs.")
        log(f"Backend: {backend_url}")
        log(f"Frontend: {frontend_url}")
        return

    log(f"Backend Live: {backend_url}")
    log(f"Frontend Live: {frontend_url}")
    
    # 3. Restart Frontend with Backend URL
    log("Configuring Frontend...")
    
    cwd = os.path.join(os.getcwd(), "client/estatevision-ai---professional-property-video-generator")
    env = os.environ.copy()
    env["VITE_API_URL"] = backend_url
    
    # Start npm
    npm_cmd_str = "nohup npm run dev -- --host --port 3000 > frontend_debug.log 2>&1 &"
    subprocess.Popen(npm_cmd_str, shell=True, cwd=cwd, env=env)
    
    log("Frontend restarting...")
    time.sleep(5)
    
    # Write final link to a file we can easily read
    with open("final_link.txt", "w") as f:
        f.write(frontend_url)

    print("\n" + "="*60)
    print("🎉 SHARE THIS LINK WITH YOUR CLIENT 🎉")
    print(f"👉 {frontend_url}")
    print("="*60)

if __name__ == "__main__":
    main()
