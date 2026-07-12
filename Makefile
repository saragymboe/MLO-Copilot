.PHONY: backend-venv frontend-install backend-test frontend-test sam-validate seed

backend-venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -U pip && pip install -r backend/requirements.txt

frontend-install:
	cd frontend && npm install

backend-test:
	cd backend && PYTHONPATH=src pytest -q tests/unit

frontend-test:
	cd frontend && npm test -- --run

sam-validate:
	cd backend && sam validate --lint

seed:
	cd backend && PYTHONPATH=src python src/functions/products/app.py --seed ../data/mortgage_product_finder_data.json
