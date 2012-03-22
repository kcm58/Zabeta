all:

docs/mora.db.html: db/__init__.py
	docco db/__init__.py
	sed -e 's/__init__\.py/mora\/db\/__index__.py/g' < docs/__init__.html > docs/mora.db.html

docs/mora.rest.html: rest/__init__.py
	docco rest/__init__.py
	sed -e 's/__init__\.py/mora\/rest\/__index__.py/g' < docs/__init__.html > docs/mora.rest.html

docs: docs/mora.db.html docs/mora.rest.html
	rm docs/__init__.html
