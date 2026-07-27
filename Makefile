.PHONY: bootstrap doctor demo serve docs-check open-check domain-check schema-check verify format lint typecheck test security build manifest dev clean

bootstrap:
	uv sync --all-packages
	@echo "Install Node through Corepack, then run: corepack enable && pnpm install"

doctor:
	@uv --version
	@python --version
	@docker --version || echo "Docker not found; required only for container workflows."
	@node --version || echo "Node not found; required for web workspaces."

demo:
	uv run --package atticus-control-plane atticus-demo --public

serve:
	uv run --package atticus-control-plane atticus-server

docs-check:
	uv run python scripts/validate_foundation.py

open-check:
	uv run python scripts/validate_open_identity.py

domain-check:
	uv run python scripts/validate_domain_wix.py

schema-check:
	uv run python scripts/validate_foundation.py

verify: docs-check open-check domain-check test

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
