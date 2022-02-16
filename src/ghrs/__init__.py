from .ghrs import GHRS  # noqa

__doc__ = """

GHRS Data Connector
=======================

GHRS Data Connector helps in extracting the Timesheet details
of the Employees.

Purpose: GHRS Data Connector serves as  an automated pipeline
to write the employee's timesheet details, to the estimate database.

GHRS data Connector, is capable of extracting employee's

- User Name
- Logged Man hours
- Job Id
- Cost_center details
- Company code

Usage Example
-------------

Installation
------------

GHRS package can be installed using pip from the internal PyPI
server using the following command::

    pip install --upgrade --extra-index-url http://sasv04ek:8008/simple --trusted-host sasv04ek ghrs

Initialization
--------------

The package can be easily initialized by following the below example
::

    # Import the package
    from ghrs import GHRS

    # Initialize a GHRS object for creating user credentials and setting up the session. 
    obj = GHRS()

Extracting recent data.
---------------------------------------------------

**get_recent_data()** method takes2 positional arguments namely 
cost_center and company_code::

    df = obj.get_recent_data('F94170',102)
    print(df)

**get_recent_data()** method will return a dataframe of Timesheet details.

Extracting data in yearly timeframe.
--------------------------------------------------

Timesheet details for past years can be extracted with
ending date as current date by following the below example.

Note: Timesheet data is available from 2017,
so no. of. years data available as of 01-06-2021 is 4 years.

**get_data_by_year()** method takes 3 positional arguments namely,
past no of years, cost_center and company_code::

    get_data_by_year = obj.get_data_by_year(1,'F94170','102')

    print(get_data_by_year)

**get_data_by_year()** method will return a dataframe of yearly Timesheet details.

Extracting data in monthly timeframe.
--------------------------------------------------

Timesheet details for past months can be extracted with
ending date as current date by following the below example:

Note: Timesheet data is available from 2017,

**get_data_by_months()** method takes 3 positional arguments namely,
past no of months, cost_center and company_code::

    get_data_by_months = obj.get_data_by_weeks(1,'F94170','102')

    print(get_data_by_months)

**get_data_by_months()** method will return a dataframe of monthly Timesheet details.

Extracting data in weekly timeframe.
--------------------------------------------------

Timesheet details for past weeks can be extracted with
ending date as current date by following the below example:

Note: Timesheet data is available from 2017,

**get_data_by_weeks()** method takes 3 positional arguments namely,
past no of weeks, cost_center and company_code::

    get_data_by_weeks = obj.get_data_by_weeks(1,'F94170','102')

    print(get_data_by_weeks)

**get_data_by_weeks()** method will return a dataframe of weekly Timesheet details.

Extracting data in custom timeframe.
--------------------------------------------------

Timesheet details for custom date range (say for example between 1-1-2020 to 10-10-2020) 
can be extracted by following the below example:

Note: Timesheet data is available from 2017,

**get_data()** method takes 4 positional arguments namely,start date, end date, cost_center and company_code
 
Note: Import the following package to specify the date format. Don't use leading 0s to years months and day


from datetime import date

Example:    date(2020,3,30) 

Args:       date(year, month, day)::

    get_data = obj.get_data(self,date(2020,1,1),date(2021,10,10),'F94170','102')

    print(get_data)

**get_data()** method will return a dataframe of specified dates, Timesheet details.

GHRS Data Summarisation
------------------------

Daily timesheet details are summarized on weekly basis.

**summarize_data()** method takes a dataframe of daily timesheet details as input
and summarizes the details on weekly basis::

    summarize_data = obj.summarize_by_week(df)

    print(summarize_data)

**summarize_data()** method will return a summarized dataframe on weekly basis.


"""

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
