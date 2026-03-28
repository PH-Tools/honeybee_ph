## Building the Documentation

### Install dependencies

```shell
pip install Sphinx sphinxcontrib-fulltoc sphinx_bootstrap_theme
```

### Generate the docs

From the **repository root folder**, run:

```shell
# Generate .rst files for each package
sphinx-apidoc -f -e -d 4 -o ./docs/api_docs ./honeybee_ph
sphinx-apidoc -f -e -d 4 -o ./docs/api_docs ./honeybee_energy_ph
sphinx-apidoc -f -e -d 4 -o ./docs/api_docs ./honeybee_phhvac
sphinx-apidoc -f -e -d 4 -o ./docs/api_docs ./honeybee_ph_utils
sphinx-apidoc -f -e -d 4 -o ./docs/api_docs ./honeybee_ph_standards

# Build the HTML documentation
sphinx-build -b html ./docs/api_docs ./docs/api_docs/_build/docs
```

Or use the convenience script:

```shell
./docs/build_docs.sh
```

### View the docs

Open `./docs/api_docs/_build/docs/index.html` in a browser.
