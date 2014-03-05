import os.path
import shutil
import sys
from setuptools import setup, find_packages
from setuptools.command import develop as _develop


class develop(_develop.develop):
    """copies over the app.yml.tmpl to app.yml"""

    def run(self):
        if '--uninstall' not in sys.argv:
            setup_filedir = os.path.dirname(__file__)
            config_dir = os.path.join(setup_filedir, "affirm_example", "config")

            if not os.path.exists(os.path.join(config_dir, "app.yml")):
                shutil.copyfile(os.path.join(config_dir, "app.yml.tmpl"),
                                os.path.join(config_dir, "app.yml"))
        _develop.develop.run(self)

setup(
    name="affirm_example",
    version="0.1.0",
    author_email="developer@affirm.com",
    packages=find_packages(exclude=["tests"]),
    url="https://github.com/Affirm/affirm-example-python",
    license="LICENSE.txt",
    description="An example integration of the Affirm V2 API",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    install_requires=[
        "PyYAML",
        "Flask >=0.10",
        "Flask-Script >= 0.6.6",
        "requests >= 1.2.0"
    ],
    tests_require=[
        "nose",
        "mock",
        "lxml",
        "blinker",
        "Flask-Testing"
    ],
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'affirm_example_manage = affirm_example.manage:main',
        ]},
    cmdclass={'develop': develop}
)
