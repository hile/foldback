
all: build

clean:
	@rm -rf build
	@rm -rf dist
	@find . -name '*.egg-info' -print0|xargs -0 rm -rf
	@find . -name '*.pyc' -print0|xargs -0 rm -rf

build:
	python setup.py build

ifdef PREFIX
install_modules: build
	python setup.py --no-user-cfg install --prefix=${PREFIX}
install: install_modules
else
install_modules: build
	python setup.py install
install: install_modules
endif

register:
	python setup.py register sdist upload

