import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="honeybee-ph",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="PH-Tools",
    author_email="info@ladybug.tools",
    description=" ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PH-Tools/honeybee_ph",
    packages=setuptools.find_packages(
        exclude=["tests", "diagrams", "docs", "honeybee_grasshopper_ph", "honeybee_ph_rhino"]),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent"
    ],
    license="AGPL-3.0"
)
