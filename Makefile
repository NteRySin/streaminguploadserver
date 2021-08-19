install-dev:
	python3 -m pip install --upgrade build twine

package:
	python3 -m build

upload:
	python3 -m twine upload --repository streaminguploadserver dist/*

clean:
	rm --recursive --force build dist streaminguploadserver/__pycache__ streaminguploadserver.egg-info __pycache__
