#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ["pyyaml >= 5.3", "pyspark"]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Leo Qin",
    author_email='leozqin@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A spark-native tool for doing ETL in a sustainable, reproducible, and low-code manner",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='etl_markup_toolkit',
    name='etl_markup_toolkit',
    packages=find_packages(include=['etl_markup_toolkit', 'etl_markup_toolkit.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/leozqin/etl-markup-toolkit',
    version='0.1.0',
    zip_safe=False,
)
