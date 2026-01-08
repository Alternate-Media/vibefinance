import os
import subprocess
import sys
import shutil

# Cross-platform task runner to replace Makefile on Windows

BACKEND_DIR = "backend"
VENV_DIR = os.path.join(BACKEND_DIR, ".venv")

if sys.platform == "win32":
    PYTHON_EXE = os.path.join(VENV_DIR, "Scripts", "python.exe")
    pytest_cmd = [PYTHON_EXE, "-m", "pytest"]
    uvicorn_cmd = [PYTHON_EXE, "-m", "uvicorn"]
else:
    PYTHON_EXE = os.path.join(VENV_DIR, "bin", "python")
    pytest_cmd = [os.path.join(VENV_DIR, "bin", "pytest")]
    uvicorn_cmd = [os.path.join(VENV_DIR, "bin", "uvicorn")]

def run(cmd, cwd=None, env=None):
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd, env=env)

def setup_backend():
    print("Installing Backend dependencies with uv...")
    # Check if uv is installed
    subprocess.call(["uv", "--version"])
    run(["uv", "venv", VENV_DIR])
    # Install deps
    run(["uv", "pip", "install", "--python", PYTHON_EXE, "-r", os.path.join(BACKEND_DIR, "pyproject.toml"), "--extra", "test", "--extra", "lint"])

def setup_frontend():
    print("Frontend setup is currently a stub. Skipping npm install.")

def setup_project():
    setup_backend()
    setup_frontend()

def run_tests(target="unit"):
    base_cmd = pytest_cmd
    if target == "unit":
        run(base_cmd + [os.path.join(BACKEND_DIR, "tests", "unit")])
    elif target == "integration":
        run(base_cmd + [os.path.join(BACKEND_DIR, "tests", "integration")])
    elif target == "mutation":
        print("Mutation tests not yet fully ported to dev.py - using pytest for now or manual command")
    elif target == "all":
        run(base_cmd + [os.path.join(BACKEND_DIR, "tests")])
    elif target == "backend":
         run(base_cmd + [os.path.join(BACKEND_DIR, "tests")])

def run_backend():
    run(uvicorn_cmd + ["main:app", "--app-dir", BACKEND_DIR, "--reload"])

def run_frontend():
    print("Frontend run is currently a stub (npm run dev).")

def docker_manage(action):
    if action == "up":
        run(["docker", "compose", "up", "-d"])
    elif action == "down":
        run(["docker", "compose", "down"])

def format_code():
    print("Formatting code...")
    run([PYTHON_EXE, "-m", "ruff", "check", BACKEND_DIR, "--fix"])
    run([PYTHON_EXE, "-m", "ruff", "format", BACKEND_DIR])

def lint_code():
    print("Linting code...")
    run([PYTHON_EXE, "-m", "ruff", "check", BACKEND_DIR])
    run([PYTHON_EXE, "-m", "mypy", BACKEND_DIR])

def git_ops(action, msg=None):
    if action == "status":
        run(["git", "status"])
    elif action == "commit":
        if not msg:
            print("Error: Commit message required. Use: python scripts/dev.py git-commit \"message\"")
            sys.exit(1)
        run(["git", "add", "."])
        run(["git", "commit", "-m", msg])
    elif action == "push":
        # Push current branch to origin
        # Get current branch
        try:
            branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
            run(["git", "push", "origin", branch])
        except subprocess.CalledProcessError:
             print("Error: Could not determine branch or push failed.")

def clean():
    print("Cleaning up...")
    for root, dirs, files in os.walk(BACKEND_DIR):
        for d in dirs:
            if d in ["__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"]:
                shutil.rmtree(os.path.join(root, d))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/dev.py [setup|...|git-status|git-commit|git-push]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "setup":
        setup_project()
    elif command == "setup-backend":
        setup_backend()
    elif command == "setup-frontend":
        setup_frontend()
    elif command == "test":
        target = sys.argv[2] if len(sys.argv) > 2 else "all"
        run_tests(target)
    elif command == "run-backend":
        run_backend()
    elif command == "run-frontend":
        run_frontend()
    elif command == "format":
        format_code()
    elif command == "docker-up":
        docker_manage("up")
    elif command == "docker-down":
        docker_manage("down")
    elif command == "clean":
        clean()
    elif command == "git-status":
        git_ops("status")
    elif command == "git-commit":
        msg = sys.argv[2] if len(sys.argv) > 2 else "Default Commit"
        git_ops("commit", msg)
    elif command == "git-push":
        git_ops("push")
    else:
        print(f"Unknown command: {command}")
