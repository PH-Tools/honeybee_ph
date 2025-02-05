import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="honeybee_ph",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
)
