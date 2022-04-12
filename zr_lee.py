
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2019 http://www.backtrader.cn  3952700@qq.com
#
###############################################################################

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects

import backtrader as bt
from backtrader import (date2num, num2date, time2num, TimeFrame, dataseries, metabase)
import file_definitions as fd
import os.path
import pandas as pd


# Create a Stratey
class HedgeSameInstrumentStrategy1(bt.Strategy):
    params = (
        # ('exitbars', 5),
        ('maperiod', 25),
        ('printlog', True),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(len(self), ' HedgeSameInstrumentStrategy1 %s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)


        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS, %.2f, NET, %.2f' %
                 (trade.pnl, trade.pnlcomm))


    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f, %.2f' % (self.dataclose[0] , 0))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        if len(self) == 10:
            self.order = self.buy(data=self.data0, exectype=bt.Order.Market)

        if len(self) == 101:
            self.order = self.close(data=self.data0, exectype=bt.Order.Market)


    def stop(self):
        # cash is amount of money on the broker's account, value is cash available plus cost of all open positions
        # Return is equal to value minus starting capital.
        # If all positions are closed than, yes, value and cash should be the same.
        # if short position still open, cash = value + abs(position value)
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)




class HedgeSameInstrumentStrategy2(bt.Strategy):
    params = (
        # ('exitbars', 5),
        ('maperiod', 25),
        ('printlog', True),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(len(self), ' HedgeSameInstrumentStrategy2 %s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)


        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS, %.2f, NET, %.2f' %
                 (trade.pnl, trade.pnlcomm))


    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f, %.2f' % (self.dataclose[0] , 0))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        if len(self) == 55:
            self.order = self.sell(data=self.data1, exectype=bt.Order.Market)

        if len(self) == 205:
            self.order = self.close(data=self.data1, exectype=bt.Order.Market)

    def stop(self):
        # cash is amount of money on the broker's account, value is cash available plus cost of all open positions
        # Return is equal to value minus starting capital.
        # If all positions are closed than, yes, value and cash should be the same.
        # if short position still open, cash = value + abs(position value)
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)

if __name__ == '__main__':
    cerebro = bt.Cerebro(maxcpus = 1 )
    cerebro.broker.setcash(100000.0)

    # Add a strategy
    cerebro.addstrategy(HedgeSameInstrumentStrategy1)
    cerebro.addstrategy(HedgeSameInstrumentStrategy2)

    df_main = pd.DataFrame()
    root_path = '/home/user/Data/loadme'

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
    df_copy = df_main.copy()

    # print('Dumping data in csv...')
    # df_main.to_csv('/home/user/Data/bla.csv')

    # Add the Data Feed to Cerebro
    # print('Creating a bt.feed...')
    data = fd.PandasData(dataname=df_main)
    data_copy = fd.PandasData(dataname=df_copy)

    # Add the 1st data to cerebro
    cerebro.adddata(data)

    # Add the 2nd data to cerebro
    cerebro.adddata(data_copy)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Set the commission
    cerebro.broker.setcommission(commission=0.0)

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.plot(style='candlestick')
    cerebro.plot()