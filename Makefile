install-dev:
	python3 -m pip install --upgrade build twine

package:
	python3 -m build

upload:
	python3 -m twine upload --repository streaminguploadserver dist/*

clean:
	rm --recursive --force __pycache__/ build/ dist/ .pytest_cache/ streaminguploadserver.egg-info/ test-files/ test-temp/ venv-python3/ client.crt client.pem server.pem test.py uploadserver.zip

install-test:
	sudo apt-get update
	sudo apt-get install python3-pip python3-venv
	python3 -m venv venv-python3
	. venv-python3/bin/activate; python3 -m pip install pytest requests; python3 -m pip install -e .

download-test:
	wget --output-document="uploadserver.zip" https://github.com/NteRySin/uploadserver/archive/12229ac1ccaf1f60a4319ffba78bdb7f6c6b8e6f.zip
	unzip -j uploadserver.zip uploadserver-*/test.py
	unzip -j uploadserver.zip uploadserver-*/test-files/* -d test-files/

test: install-test download-test
	openssl req -x509 -out server.pem -keyout server.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=server'
	openssl req -x509 -out client.pem -keyout client.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=client'
	openssl x509 -in client.pem -out client.crt

	rm --recursive --force test-temp/
	. venv-python3/bin/activate; PROTOCOL=HTTP VERBOSE=1 python3 -u -m pytest --verbosity 2 --tb short --capture no test.py
	rm --recursive --force test-temp/
	. venv-python3/bin/activate; PROTOCOL=HTTPS VERBOSE=1 python3 -u -m pytest --verbosity 2 --tb short --capture no test.py
	rm --recursive --force test-temp/
