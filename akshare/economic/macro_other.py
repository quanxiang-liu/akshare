#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/6/1 16:36
Desc: 金十数据-其他-加密货币实时行情
"""
import time
from datetime import datetime

import pandas as pd
import requests


def crypto_js_spot() -> pd.DataFrame:
    """
    主流加密货币的实时行情数据, 一次请求返回具体某一时刻行情数据
    https://datacenter.jin10.com/reportType/dc_bitcoin_current
    :return: pandas.DataFrame
    """
    url = "https://datacenter-api.jin10.com/crypto_currency/list"
    params = {
        "_": int(time.time() * 1000),
    }
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'origin': 'https://datacenter.jin10.com',
        'referer': 'https://datacenter.jin10.com/',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'x-app-id': 'rU6QIu7JHe2gOUeR',
        'x-version': '1.0.0'
    }
    r = requests.get(url, params=params, headers=headers)
    r.encoding = 'utf-8'
    data_json = r.json()
    data_df = pd.DataFrame(data_json["data"])
    data_df["reported_at"] = pd.to_datetime(data_df["reported_at"])
    data_df.columns = [
        "市场",
        "交易品种",
        "最近报价",
        "涨跌额",
        "涨跌幅",
        "24小时最高",
        "24小时最低",
        "24小时成交量",
        "更新时间",
    ]
    data_df["最近报价"] = pd.to_numeric(data_df["最近报价"])
    data_df["涨跌额"] = pd.to_numeric(data_df["涨跌额"])
    data_df["涨跌幅"] = pd.to_numeric(data_df["涨跌幅"])
    data_df["24小时最高"] = pd.to_numeric(data_df["24小时最高"])
    data_df["24小时最低"] = pd.to_numeric(data_df["24小时最低"])
    data_df["24小时成交量"] = pd.to_numeric(data_df["24小时成交量"])
    data_df["更新时间"] = data_df["更新时间"].astype(str)
    return data_df


def macro_fx_sentiment(
    start_date: str = "20200422", end_date: str = "20200422"
) -> pd.DataFrame:
    """
    金十数据-外汇-投机情绪报告
    外汇投机情绪报告显示当前市场多空仓位比例，数据由8家交易平台提供，涵盖11个主要货币对和1个黄金品种。
    报告内容: 品种: 澳元兑日元、澳元兑美元、欧元兑美元、欧元兑澳元、欧元兑日元、英镑兑美元、英镑兑日元、纽元兑美元、美元兑加元、美元兑瑞郎、美元兑日元以及现货黄金兑美元。
             数据: 由Shark - fx整合全球8家交易平台（ 包括 Oanda、 FXCM、 Insta、 Dukas、 MyFxBook以及FiboGroup） 的多空投机仓位数据而成。
    名词释义: 外汇投机情绪报告显示当前市场多空仓位比例，数据由8家交易平台提供，涵盖11个主要货币对和1个黄金品种。
    工具使用策略: Shark-fx声明表示，基于“主流通常都是错误的”的事实，当空头头寸超过60%，交易者就应该建立多头仓位； 同理，当市场多头头寸超过60%，交易者则应该建立空头仓位。此外，当多空仓位比例接近50%的情况下，我们则倾向于建议交易者不要进场，保持观望。
    https://datacenter.jin10.com/reportType/dc_ssi_trends
    :param start_date: 具体交易日
    :type start_date: str
    :param end_date: 具体交易日, 与 end_date 相同
    :type end_date: str
    :return: 投机情绪报告
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "https://datacenter-api.jin10.com/sentiment/datas"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "currency_pair": "",
        "_": int(time.time() * 1000),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_ssi_trends",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    res = requests.get(url, params=params, headers=headers)
    return pd.DataFrame(res.json()["data"]["values"]).T


def index_vix(
    start_date: str = "20210401", end_date: str = "20210402"
) -> pd.DataFrame:
    """
    金十数据-市场异动-恐慌指数; 只能获取当前交易日近一个月内的数据
    https://datacenter.jin10.com/market
    :param start_date: 具体交易日, 只能获取当前交易日近一个月内的数据
    :type start_date: str
    :param end_date: 具体交易日, 与 end_date 相同, 只能获取当前交易日近一个月内的数据
    :type end_date: str
    :return: 恐慌指数
    :rtype: pandas.DataFrame
    """
    import warnings

    warnings.warn("由于目标网站未更新数据，该接口即将移除", DeprecationWarning)
    url = "https://datacenter-api.jin10.com/vix/datas"
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "_": int(time.time() * 1000),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_ssi_trends",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    res = requests.get(url, params=params, headers=headers)
    temp_df = pd.DataFrame(
        res.json()["data"]["values"], index=["开盘价", "当前价", "涨跌", "涨跌幅"]
    ).T
    temp_df = temp_df.astype(float)
    return temp_df


if __name__ == "__main__":
    crypto_js_spot_df = crypto_js_spot()
    print(crypto_js_spot_df)

    test_date = datetime.now().date().isoformat().replace("-", "")

    macro_fx_sentiment_df = macro_fx_sentiment(
        start_date=test_date, end_date=test_date
    )
    print(macro_fx_sentiment_df)

    index_vix_df = index_vix(start_date="20220501", end_date="20220517")
    print(index_vix_df)
