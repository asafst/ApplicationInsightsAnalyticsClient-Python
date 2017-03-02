Application Insights Analytics Client for Python
================================================

This project enables quering the Application Insights Analytics API while parsing the results for furthur processing in a simple manner. `Application Insights Analytics <https://docs.microsoft.com/en-us/azure/application-insights/app-insights-analytics>`_ is a powerful search feature of Application Insights, which allows to query your Applciation Insights telemetry.
This module is meant to be used with other data analysis packages, such as `numpy <http://www.numpy.org/>`_ and `matplotlib <http://matplotlib.org/>`_. The query result are numpy arrays.

    **Note**: this package is not for sending telemetry to the Application Insights serivce. For that you can use the `official python sdk repo <https://github.com/Microsoft/ApplicationInsights-Python>`_.


Requirements
------------

This module was tested on Python 2.7 and Python 3.5. Older versions of Python 3 probably work as well. 

For opening the project in Microsoft Visual Studio you will need `Python Tools for Visual Studio <http://pytools.codeplex.com/>`_.

Installation
------------

To install the latest release you can use `pip <http://www.pip-installer.org/>`_.

::

    $ pip install aianalytics-client

Usage
-----

Once installed, you can query your Application Insights telemetry. Here are a few samples.

**Query exceptions from the last 24 hours and print them**

.. code:: python

    from analytics.client import AnalyticsClient
    client = AnalyticsClient('<Your app id goes here>', '<You app key goes here>')
    result = client.query('exceptions | where timestamp > ago(24h) | project timestamp, type, outerMessage') 
    for row in result.row_iterator():
        print ("at {0} there was an exception of type {1} with message {2}".format(row['timestamp'], row['type'], row['outerMessage']))
        # Indexes can also be used instead of column names, e.g.:
        print ("at {0} there was an exception of type {1} with message {2}".format(row[0], row[1], row[2]))


**Query average request duration from the last week and plot using matplotlib**

.. code:: python

    from analytics.client import AnalyticsClient
    client = AnalyticsClient('<Your app id goes here>', '<You app key goes here>')
    result = client.query('requests | where timestamp > ago(7d) | summarize Duration = avg(duration/1000) by bin(timestamp, 1h) | order by timestamp asc') 

    import matplotlib.pyplot as plt
    plt.plot(result["timestamp"], result["Duration"])
    plt.show()


