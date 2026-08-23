# Pin the Ollama CLI to the daemon Atticus uses, pull Qwen3 1.7B and SmolLM3-3B,
# then print the environment Atticus needs.
#
# Usage (from the repo root, in PowerShell):
#   powershell -ExecutionPolicy Bypass -File scripts\windows\setup-local-models.ps1
#
# Why OLLAMA_HOST is required: `ollama list` and
# `curl.exe http://localhost:11434/v1/models` can show different libraries on
# Windows. Atticus talks only to the HTTP daemon.

$ErrorActionPreference = "Stop"
$env:OLLAMA_HOST = "http://127.0.0.1:11434"

Write-Host "OLLAMA_HOST=$env:OLLAMA_HOST"
Write-Host ""
Write-Host "=== daemon tags before pull (this is what Atticus sees) ==="
curl.exe http://127.0.0.1:11434/api/tags
Write-Host ""
Write-Host "=== ollama list (must match the daemon after OLLAMA_HOST is set) ==="
ollama list
Write-Host ""

Write-Host "Pulling qwen3:1.7b (official Ollama library, ~1.4 GB)..."
ollama pull qwen3:1.7b

Write-Host "Pulling SmolLM3-3B GGUF (not in the Ollama library)..."
ollama pull hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M

Write-Host ""
Write-Host "=== daemon tags after pull ==="
curl.exe http://127.0.0.1:11434/api/tags
Write-Host ""
Write-Host "If SmolLM3's name differs from the pull tag, copy the exact 'name' from /api/tags into ATTICUS_MODEL."
Write-Host ""
Write-Host "Atticus (PowerShell, this session):"
Write-Host '  $env:ATTICUS_MODEL="qwen3:1.7b"'
Write-Host '  $env:ATTICUS_MODEL_NO_THINKING="1"'
Write-Host "  uv run python scripts/check_local_ollama.py"
Write-Host "  uv run python scripts/probe_model.py --model qwen3:1.7b --no-thinking"
Write-Host "  uv run --package atticus-control-plane atticus-demo --public"
Write-Host ""
Write-Host "Read the PLANNER: line. 'model planner via' means the model planned."
Write-Host "Anything else is a silent fallback to the fixture planner."
