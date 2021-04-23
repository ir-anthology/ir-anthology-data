SHELL = /bin/bash
.PHONY: make
make: .venv
	source .venv/bin/activate && cd scripts && pip3 install .
	@(echo -e '#!/bin/bash'"\n"'source .venv/bin/activate && ir-anthology-data $$@' | tee ir-anthology-data) > /dev/null
	@chmod +x ir-anthology-data

.venv:
	python3 -m venv .venv

