# Pin the Ollama CLI to the daemon Atticus uses, make sure Qwen3 1.7B GGUF
# and SmolLM3-3B are on that daemon, then print the Atticus environment.
#
# Usage (from the repo root, in PowerShell):
#   powershell -ExecutionPolicy Bypass -File scripts\windows\setup-local-models.ps1
#
# Why OLLAMA_HOST is required: `ollama list` and
# `curl.exe http://localhost:11434/v1/models` can show different libraries on
# Windows. Atticus talks only to the HTTP daemon.

$ErrorActionPreference = "Stop"
$env:OLLAMA_HOST = "http://127.0.0.1:11434"
$QwenTag = "hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0"
$SmolTag = "hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M"

Write-Host "OLLAMA_HOST=$env:OLLAMA_HOST"
Write-Host ""
Write-Host "=== daemon tags before pull (this is what Atticus sees) ==="
curl.exe http://127.0.0.1:11434/api/tags
Write-Host ""
Write-Host "=== ollama list (must match the daemon after OLLAMA_HOST is set) ==="
ollama list
Write-Host ""

Write-Host "Pulling $QwenTag (the Qwen3 1.7B GGUF already on the CLI library)..."
ollama pull $QwenTag

Write-Host "Pulling $SmolTag (SmolLM3-3B; not in the official Ollama library)..."
ollama pull $SmolTag

Write-Host ""
Write-Host "=== daemon tags after pull ==="
curl.exe http://127.0.0.1:11434/api/tags
Write-Host ""
Write-Host "If SmolLM3's name differs from the pull tag, copy the exact 'name' from /api/tags into ATTICUS_MODEL."
Write-Host ""
Write-Host "Atticus (PowerShell, this session):"
Write-Host "  `$env:ATTICUS_MODEL=`"$QwenTag`""
Write-Host '  $env:ATTICUS_MODEL_NO_THINKING="1"'
Write-Host "  uv run python scripts/check_local_ollama.py"
Write-Host "  uv run python scripts/probe_model.py --model $QwenTag --no-thinking"
Write-Host "  uv run --package atticus-control-plane atticus-demo --public"
Write-Host ""
Write-Host "Switch to SmolLM3 by setting ATTICUS_MODEL to the exact SmolLM3 name from /api/tags."
Write-Host "Read the PLANNER: line. 'model planner via' means the model planned."
Write-Host "Anything else is a silent fallback to the fixture planner."
