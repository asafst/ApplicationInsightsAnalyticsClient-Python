from setuptools import setup, find_packages
from codecs import open 
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aianalytics-client',
    packages = find_packages(exclude=['contrib', 'docs', 'tests*']),
    version='0.1.5',
    description='This project enables quering the Application Insights Analytics API while parsing the results for furthur processing using data analysis tools (e.g. numpy).',
    long_description=long_description,

    url='https://github.com/asafst/ApplicationInsightsAnalyticsClient-Python',
    download_url='https://github.com/asafst/ApplicationInsightsAnalyticsClient-Python',

    author='Asaf Strassberg',
    author_email='asafst@microsoft.com',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Operating System :: OS Independent',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    install_requires=[
        'requests',
        'python-dateutil',
        'numpy'
    ],

    license='MIT',
    keywords='analytics applicationinsights telemetry appinsights numpy IPython'
)

