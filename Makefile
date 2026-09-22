.PHONY: install test lint eval dev

install:
	python3 -m pip install -e 'backend[dev]'
	cd apps/web && npm install

test:
	PYTHONPATH=backend/src pytest -q

lint:
	ruff check backend
	cd apps/web && npm run typecheck

eval:
	PYTHONPATH=backend/src python3 backend/scripts/evaluate.py --input data/gold/ccb_v0_1.jsonl --output artifacts/evaluation

dev:
	uvicorn buyermoment.api:app --app-dir backend/src --reload
