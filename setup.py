from distutils.core import setup

setup(
    name='aianalytics-client',
    version='0.1.0',
    description='This project enables quering the Application Insights Analytics API while parsing the results for furthur processing using data analysis tools, such as numpy',

    # The project's main homepage.
    url='https://github.com/Microsoft/AppInsights-Python',
    download_url='https://github.com/Microsoft/AppInsights-Python',

    # Author details
    author='Microsoft',
    author_email='aiengdisc@microsoft.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # operating systems
        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='analytics applicationinsights telemetry appinsights development',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    test_suite='tests.applicationinsights_tests'
)
