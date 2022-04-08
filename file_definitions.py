from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt


class PandasData(bt.feeds.PandasData):
    linesoverride = True
    lines = ('datetime', 'open', 'high', 'low', 'close', 'volume', 'transcnt',)

    params = (
      # Possible values for datetime (must always be present)
      #  None : datetime is the "index" in the Pandas Dataframe
      #  -1 : autodetect position or case-wise equal name
      #  >= 0 : numeric index to the colum in the pandas dataframe
      #  string : column name (as index) in the pandas dataframe
      ('datetime', None),

      # Possible values below:
      #  None : column not present
      #  -1 : autodetect position or case-wise equal name
      #  >= 0 : numeric index to the colum in the pandas dataframe
      #  string : column name (as index) in the pandas dataframe
      ('open', 'open'),
      ('high', 'high'),
      ('low', 'low'),
      ('close', 'close'),
      ('volume', 'volume'),
      ('transcnt', 'transcnt'),
      ('openinterest', None),
    )