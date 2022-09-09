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
    author_email="phtools@bldgtyp.com",
    description="Plugin for Honeybee to enable Passive House modeling.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PH-Tools/honeybee_ph",
    packages=setuptools.find_packages(
        include=['*'],
        exclude=['tests*', 'honeybee_ph_rhino*', 'honeybee_grasshopper_ph'],
    ),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    license="GPLv3+"
)
