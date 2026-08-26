.PHONY: bootstrap doctor demo local-models-check feeds-refresh bakeoff bakeoff-json replay-site belief-site belief-recovery serve docs-check program-check open-check domain-check schema-check public-check public-release-check verify format lint typecheck test security build manifest dev clean

bootstrap:
	uv sync --all-packages --locked
	pnpm install --frozen-lockfile

doctor:
	@uv --version
	@uv run python --version
	@docker --version || echo "Docker not found; required only for container workflows."
	@node --version || echo "Node not found; required for web workspaces."
	@pnpm --version || echo "pnpm not found; required for web workspaces."

demo:
	uv run --package atticus-control-plane atticus-demo --public

local-models-check:
	uv run python scripts/check_local_ollama.py

feeds-refresh:
	uv run python scripts/refresh_public_feeds.py --print-changes

bakeoff:
	uv run python scripts/run_bakeoff.py

replay-site:
	uv run python scripts/build_replay_site.py --out site/replays --metadata

belief-site:
	uv run python scripts/build_belief_site.py --out site/beliefs --metadata

belief-recovery:
	uv run python scripts/run_belief_recovery.py

bakeoff-json:
	uv run python scripts/run_bakeoff.py --json

serve:
	uv run --package atticus-control-plane atticus-server

docs-check:
	uv run python scripts/validate_foundation.py

program-check:
	uv run python scripts/validate_program.py

open-check:
	uv run python scripts/validate_open_identity.py

domain-check:
	uv run python scripts/validate_domain_wix.py

schema-check:
	uv run python scripts/validate_foundation.py

public-check:
	uv run python scripts/validate_public_repository.py

public-release-check:
	uv run python scripts/validate_public_repository.py --release

verify: docs-check program-check open-check domain-check public-check test

format:
	uv run ruff format scripts tests packages services apps/atticus-local-runner

lint:
	uv run ruff check scripts tests packages services apps/atticus-local-runner

typecheck:
	uv run mypy scripts packages services apps/atticus-local-runner

test:
	uv run pytest
	pnpm -r test

security:
	uv run bandit -q -r scripts packages services apps/atticus-local-runner

build:
	pnpm -r build
	uv build --package atticus-control-plane

manifest:
	uv run python scripts/generate_manifest.py

dev:
	docker compose up -d
	uv run --package atticus-control-plane atticus-server

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache dist build coverage htmlcov
