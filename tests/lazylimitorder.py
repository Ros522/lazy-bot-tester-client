import unittest
from backtestlob import OrderType, Side

import numpy as np

from lazybacktestlob import LazyBackTestEnv


class Simple(unittest.TestCase):
    def test_lazy_simplelimit(self):
        test = np.datetime64('now')

        env = LazyBackTestEnv(last_timestamp=test)
        # 1枚買い
        orderid = env.entry(OrderType.LIMIT, Side.BUY, 1, 500000, lag=1)
        for k, o in env.get_orders().items():
            print(f"Order{k}", o.side, o.size, o.price)

        # Low,Highで約定判定
        profit, trade = env.step(test, 480000, 510000)
        # 遅延してるので、約定しない
        self.assertEqual(trade, 0)
        # オーダーもない
        self.assertEqual(len(env.get_orders()), 0)

        # 2秒後の約定しないTick
        profit, trade = env.step(test + np.timedelta64(2, 's'), 510000, 520000)
        # オーダーは認識する
        self.assertEqual(len(env.get_orders()), 1)

        # 3秒後の約定するTick
        profit, trade = env.step(test + np.timedelta64(3, 's'), 480000, 520000)

        # 本stepでの収支0,ポジション買い　1枚　平均単価50万
        # profit=0,trade=1
        # position=1.0 side=0.0 price=500000.0
        self.assertEqual(profit, 0)
        self.assertEqual(env.size, 1.0)
        self.assertEqual(env.side, Side.BUY)
        self.assertEqual(env.price, 500000)

        # 1枚売り
        orderid = env.entry(OrderType.LIMIT, Side.SELL, 1.5, 520000, lag=1)

        # 約定判定
        profit, trade = env.step(test + + np.timedelta64(60, 's'), 510000, 530000)

        # 本stepでの収支20000,ポジション売り　0.5枚　平均単価52万
        # profit=20000,trade=1
        # position=0.5 side=1.0 price=520000.0
        self.assertEqual(profit, 20000)
        self.assertEqual(env.size, 0.5)
        self.assertEqual(env.side, Side.SELL)
        self.assertEqual(env.price, 520000)

    def test_lazy_cancel_simplelimit(self):
        test = np.datetime64('now')

        env = LazyBackTestEnv(last_timestamp=test)
        # 1枚買い
        orderid = env.entry(OrderType.LIMIT, Side.BUY, 1, 500000, lag=1)

        # Low,Highで約定判定
        profit, trade = env.step(test, 480000, 510000)
        # 遅延してるので、約定しない
        self.assertEqual(trade, 0)
        # オーダーもない
        self.assertEqual(len(env.get_orders()), 0)

        # cancelする
        env.cancel(orderid, lag=2)

        # 1秒後の約定するTick
        profit, trade = env.step(test + np.timedelta64(1, 's'), 480000, 520000)

        # 本stepでの収支0,ポジション買い　1枚　平均単価50万 ( キャンセル失敗）
        # profit=0,trade=1
        # position=1.0 side=0.0 price=500000.0
        self.assertEqual(profit, 0)
        self.assertEqual(env.size, 1.0)
        self.assertEqual(env.side, Side.BUY)
        self.assertEqual(env.price, 500000)

        # 1枚売り
        orderid = env.entry(OrderType.LIMIT, Side.SELL, 1.5, 520000)

        # cancelする
        env.cancel(orderid, lag=2)

        # 約定判定
        profit, trade = env.step(test + np.timedelta64(60, 's'), 510000, 530000)

        # キャンセルされてるので約定しない
        self.assertEqual(trade, 0)



if __name__ == '__main__':
    unittest.main()
