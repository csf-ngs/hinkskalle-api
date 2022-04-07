#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests', 'PyYAML', 'click_log', 'humanize' ]

test_requirements = [ 'coverage', 'nose2', 'nose2-html-report', 'nose2[coverage_plugin]' ]

setup(
    author="Heinz Axelsson-Ekker",
    author_email='heinz.ekker@vbcf.ac.at',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="API and CLI for Hinkskalle",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='hinkskalle_api',
    name='hinkskalle_api',
    packages=find_packages(include=['hinkskalle_api', 'hinkskalle_api.*']),
    test_suite='tests',
    url='https://github.com/h3kker/hinkskalle_api',
    version='0.3.4',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'hinkli = hinkskalle_api.cli:cli',
        ],
    },
    extras_require={
        'test': test_requirements,
    }
)
