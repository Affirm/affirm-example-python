import os.path
from setuptools import setup, find_packages


setup(
    name="Affirm Python Example",
    version="0.1.0",
    author_email="developer@affirm.com",
    packages=find_packages(exclude=["tests"]),
    url="https://github.com/Affirm/affirm-example-python",
    license="LICENSE.txt",
    description="An example integration of the Affirm V2 API",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    install_requires=[
        "Flask >=0.10",
        "Flask-Script >= 0.6.6",
        "requests >= 1.2.0"
    ],
    tests_require=[
        "nose",
        "lxml",
        "blinker",
        "Flask-Testing"
    ],
    test_suite='nose.collector'
)