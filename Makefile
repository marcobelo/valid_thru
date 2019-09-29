clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.log

test:
	. venv/bin/activate
	pytest