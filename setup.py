from setuptools import setup, find_packages


setup(
    name="Affirm Python Example",
    version="0.1.0",
    author_email="developer@affirm.com",
    packages=find_packages(exclude=["tests"]),
    url="https://github.com/Affirm/affirm-example-python",
    license="LICENSE.txt",
    description="An example integration of the Affirm V2 API",
    long_description=open('README.md').read(),
    install_requires=[
        "Flask >=0.10",
        "Flask-Script >= 0.6.6",
        "requests >= 1.2.0"
    ],
    test_requires=[
        "nose",
        "lxml",
        "blinker",
        "Flask-Testing"
    ]
)