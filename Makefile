install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

package-force-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 src

fast-check:
	echo "\n\n\n ! Build process...\n"
	make build
	echo "\n\n\n ! Package-force-reinstall process...\n"
	make package-force-reinstall
	echo "\n\n\n ! Lint checkup process...\n"
	make lint
