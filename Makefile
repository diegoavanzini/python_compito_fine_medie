.PHONY: run test clean compile_mo compile_mo_it compile_mo_en compile_mo_es

run_it:
	python main.py -l it

run_en:
	python main.py -l en

run_es:
	python main.py -l es

run_page:
	python SitoFlask/app.py

test:
	pytest -q

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete
	
translate_it:
	xgettext -d main -o locale/main.pot main.py
# 	msginit -l it -i locale/main.pot -o locale/it/LC_MESSAGES/main.po
	msgfmt locale/it/LC_MESSAGES/main.po -o locale/it/LC_MESSAGES/main.mo 

translate_en:
	xgettext -d main -o locale/main.pot main.py
# 	msginit -l en -i locale/main.pot -o locale/en/LC_MESSAGES/main.po
	msgfmt locale/en/LC_MESSAGES/main.po -o locale/en/LC_MESSAGES/main.mo 

translate_es:
	xgettext -d main -o locale/main.pot main.py
# 	msginit -l es -i locale/main.pot -o locale/es/LC_MESSAGES/main.po
	msgfmt locale/es/LC_MESSAGES/main.po -o locale/es/LC_MESSAGES/main.mo 

compile_mo: compile_mo_it compile_mo_en compile_mo_es

compile_mo_it:
	msgfmt locale/it/LC_MESSAGES/main.po -o locale/it/LC_MESSAGES/main.mo

compile_mo_en:
	msgfmt locale/en/LC_MESSAGES/main.po -o locale/en/LC_MESSAGES/main.mo

compile_mo_es:
	msgfmt locale/es/LC_MESSAGES/main.po -o locale/es/LC_MESSAGES/main.mo