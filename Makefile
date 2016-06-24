# .PHONY: docs

setup:
	python setup.py install

init:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	py.test -n auto tests --doctest-modules --pep8 what3words -v --cov what3words --cov-report term-missing

ci: init
		py.test --junitxml=junit.xml

clean:
	python setup.py clean --all
	rm -rf build-*
	rm -rf *egg*
	rm -rf dist

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload

register:
	python setup.py register

# docs:
# 	make -C docs html
