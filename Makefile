
all: build

clean:
	@rm -rf build
	@rm -rf dist
	@find . -name '*.egg-info' -print0|xargs -0 rm -rf
	@find . -name '*.pyc' -print0|xargs -0 rm -rf

build:
	python setup.py build sdist

ifdef PREFIX
install_modules: build
	python setup.py --no-user-cfg install --prefix=${PREFIX}
install: install_modules
else
install_modules: build
	python setup.py install
install: install_modules
endif

register-test:
	python setup.py sdist
	python setup.py register -r test sdist upload

register:
	python setup.py register sdist upload

