from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path

# Import the backtrader platform
import backtrader as bt
import pandas as pd
import file_definitions as fd


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    df_main = pd.DataFrame()
    root_path = '/home/user/Data'

    for root, dirs, files in os.walk(root_path):
        for csv in files:
            if csv.startswith('BTCUSDT_1m_'):
                csv_path = os.path.join(root, csv)

                df = pd.read_csv(
                    filepath_or_buffer="{}".format(csv_path),
                    header=0,
                    index_col=0,
                    parse_dates=True
                )

                if len(df_main) == 0:
                    df_main = df.rename(
                        columns={'o': 'open',
                                 'h': 'high',
                                 'c': 'close',
                                 'l': 'low',
                                 'v': 'volume',
                                 'nt': 'transcnt'}).copy()
                else:
                    df_main = pd.concat([df_main, df.rename(
                        columns={'o': 'open',
                                 'h': 'high',
                                 'c': 'close',
                                 'l': 'low',
                                 'v': 'volume',
                                 'nt': 'transcnt'})])

    df_main.index.names = ['datetime']
    df_main = df_main.sort_values(
        by="datetime",
        kind="mergesort",
        ascending=True)
    df_main = df_main.drop_duplicates()

    # print('Dumping data in csv...')
    # df_main.to_csv('/home/user/Data/bla.csv')

    # Add the Data Feed to Cerebro
    print('Creating a bt.feed...')
    data = fd.PandasData(dataname=df_main)

    print('Adding the bt.feed to cerebro...')
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    # cerebro.plot(style='bar')