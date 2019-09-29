clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.log

prepare:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements/dev.txt

test_unit:
	. venv/bin/activate && pytest tests/unit/

test_e2e:
	. venv/bin/activate && pytest tests/e2e/

run_server:
	. venv/bin/activate && python app/app.py