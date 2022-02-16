from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from io import StringIO
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class Query():
    """
    Class for Querying GHRS data
    This class contains 4 wrapper functions
                                            -get_recent_data()
                                            -get_yearly_window()
                                            -get_monthly_window()
    The Base function of Class Query is
                                            -get_data()

    Note: Import the following package to specify the date format.
          Don't use leading 0s to years and months and day.

    from datetime import date
    date(2020,3,30) Args: date(year, month, day)

    All the above functions takes different time ranges as parameters.
    These wrapper functions return the GHRS Timesheet data in common
    The final DataFrame contains
                             - User Name
                             - Logged Man hours
                             - Job Id
                             - Cost_center details
                             - Company code.
    """

    def get_recent_data(self, cost_center, company_code):
        """
        This method returns the GHRS data for a 9 week range
        (4 weeks prior current week and 4 weeks post
        current week).

        Args:
            cost_center (str): A string object which specifies the cost
            center.

            company_code (str): A string object which specifies the
            company code.

        Return:
              pandas.DataFrame: returns a DataFrame object which contains the
              GHRS Timesheet details of the employees for a 9 week
              window (4 weeks past and post current week).

        """
        weekday = datetime.strptime(date.today().strftime("%V %G 1"),
                                    "%V %G %u").date()
        start_date = weekday - relativedelta(weeks=8)
        end_date = weekday + relativedelta(weeks=8)
        return self.get_data(start_date, end_date, cost_center,
                             company_code)


    def get_data_by_weeks(self, weeks, cost_center, company_code):

        """
        This method returns the GHRS data for specified months

        Args:
            no_of_months (int): A integer object which specifies
            no of weeks before, for which data has to be extracted.

            cost_center (str): A string object which specifies
            the cost center.

            company_code (str): A string object which specifies
            the company code.

        Return:
              pandas.DataFrame: Returns a DataFrame object which
              contains GHRS Timesheet details of the employees for a
              specified month range.
        """
        weekday = datetime.strptime(date.today().strftime("%V %G 1"),
                                    "%V %G %u").date()
        start_date = weekday - relativedelta(weeks=weeks)
        end_date = weekday + relativedelta(weeks=4)
        return self.get_data(start_date, end_date, cost_center,
                             company_code)

    def get_data_by_months(self, months, cost_center, company_code):

        """
        This method returns the GHRS data for specified months

        Args:
            no_of_months (int): A integer object which specifies
            no of months before, for which data has to be extracted.

            cost_center (str): A string object which specifies
            the cost center.

            company_code (str): A string object which specifies
            the company code.

        Return:
              pandas.DataFrame: Returns a DataFrame object which
              contains GHRS Timesheet details of the employees for a
              specified no of months.
        """
        weekday = datetime.strptime(date.today().strftime("%V %G 1"),
                                    "%V %G %u").date()
        start_date = weekday - relativedelta(months=months)
        end_date = weekday + relativedelta(weeks=4)
        return self.get_data(start_date, end_date, cost_center,
                             company_code)

    def get_data_by_year(self, year, cost_center, company_code):
        """
        This method returns the GHRS data for specified year range

        Args:
            no_of_year (int): A integer object which specifies no of
            years from which data has to be extracted.

            cost_center (str): A string object which specifies the cost
            center.

            company_code (str): A string object which specifies the
            company code.

        Return:
              pandas.DataFrame: Returns a DataFrame object which
              contains the GHRS Timesheet details of the employees for
              specified years.
        """
        weekday = datetime.strptime(date.today().strftime("%V %G 1"),
                                    "%V %G %u").date()
        start_date = weekday - relativedelta(year=year)
        end_date = weekday + relativedelta(weeks=4)
        return self.get_data(start_date, end_date, cost_center,
                             company_code)

    def get_data(self, start_date, end_date,
                 cost_center, company_code):
        """
        This method scraps the html content using
        BeautifulSoup when the response staus code is 200.

        The scrapped data is downloaded as xml and
        parsed using xml.etree and converted as a DataFrame.

        Args:
            start_date (date): A date object which specifies the
            starting date for extracting date.

            end_date (date): A date object which specifies the
            ending date for extracting date.

            cost_center (str): A string object which specifies the cost
            center.

            company_code (str): A string object which specifies the
            company code.

        Return:
              pandas.DataFrame: Returns a DataFrame object which
              contains the Timesheet details of the employees on
              specified timerange.

        """
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            if soup.form is None:
                return None
            data = {i.attrs.get('name', ''): i.attrs.get('value', '')
                    for i in soup.form.find_all('input')
                    if i.attrs.get('name', '') != ''}
            data.update({
                'ICAction': '#ICOK',
                'InputKeys_bind1': start_date.strftime('%Y/%m/%d'),
                'InputKeys_bind2': end_date.strftime('%Y/%m/%d'),
                'InputKeys_ACCT_CD': cost_center,
                'InputKeys_COMPANY': company_code})
            response = self.session.post(
                soup.form.attrs.get('action', ''),
                data=data,
                headers=self.header)
            if response.status_code != 200:
                return None
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.form is None:
                return None
            data = {i.attrs.get('name', ''): i.attrs.get('value', '')
                    for i in soup.form.find_all('input')
                    if i.attrs.get('name', '') != ''}
            data.update({'ICAction': '#ICQryDownloadXML'})
            response = self.session.post(
                soup.form.attrs.get('action', ''),
                data=data,
                headers=self.header)
            if response.status_code != 200:
                return None
            df = pd.DataFrame([
                {i.tag: i.text for i in r.iter() if i.tag != 'row'}
                for r in ET.parse(StringIO(response.text)).iter('row')])
            if not df.empty:
                df['DUR'] = [datetime.strptime(i, '%Y-%m-%d').date()
                    for i in df['DUR'].values]
                df['TL_QUANTITY'] = [float(i)
                    for i in df['TL_QUANTITY'].values]
                df['USER_FIELD_2'] = ['' if i is None else i
                    for i in df['USER_FIELD_2'].values]
                df['USER_FIELD_3'] = ['' if i is None else i
                    for i in df['USER_FIELD_3'].values]
                df['USER_FIELD_5'] = ['' if i is None else i
                    for i in df['USER_FIELD_5'].values]
            return df


    def summarize_by_week(self, df):
        """
        Given a daily data, this method returns the Weekly summarized
        GHRS data.

        Args:
            df (pandas.DataFrame): Daily GHRS report.

        Returns:
            pandas.DataFrame: Weekly summarized GHRS report.

        """

        df_summary = df.copy()
        df_summary.set_index(
            pd.DatetimeIndex(pd.to_datetime(df_summary['DUR'])),
            inplace=True)
        df_summary.fillna("", inplace=True)
        df_summary.drop("DUR", axis=1, inplace=True)
        df_summary = df_summary.groupby(
            ['EMPLID', 'EMPL_RCD', 'FIRST_NAME', 'LAST_NAME', 'ACCT_CD',
            'USER_FIELD_2', 'USER_FIELD_3', 'USER_FIELD_5']
            ).resample('W-MON', "DUR", closed='left', label='left').sum()
        df_summary.reset_index(inplace=True)
        df_summary["DUR"] = df_summary["DUR"].apply(lambda x: x.date())
        return df_summary