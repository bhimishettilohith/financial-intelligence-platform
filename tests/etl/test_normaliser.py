import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.normaliser import normalize_year
from src.etl.normaliser import normalize_ticker


# ---------------------------
# YEAR TESTS
# ---------------------------

def test_year_1():
    assert normalize_year("2024") == 2024

def test_year_2():
    assert normalize_year("FY24") == 2024

def test_year_3():
    assert normalize_year("FY 24") == 2024

def test_year_4():
    assert normalize_year("FY2023") == 2023

def test_year_5():
    assert normalize_year(2022) == 2022

def test_year_6():
    assert normalize_year("2021") == 2021

def test_year_7():
    assert normalize_year("FY20") == 2020

def test_year_8():
    assert normalize_year("FY19") == 2019

def test_year_9():
    assert normalize_year("18") == 2018

def test_year_10():
    assert normalize_year("17") == 2017


# ---------------------------
# TICKER TESTS
# ---------------------------

def test_ticker_1():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_2():
    assert normalize_ticker("TCS") == "TCS"

def test_ticker_3():
    assert normalize_ticker(" tcs ") == "TCS"

def test_ticker_4():
    assert normalize_ticker("tcs.ns") == "TCS"

def test_ticker_5():
    assert normalize_ticker("tcs.bo") == "TCS"

def test_ticker_6():
    assert normalize_ticker("INFY") == "INFY"

def test_ticker_7():
    assert normalize_ticker("infy") == "INFY"

def test_ticker_8():
    assert normalize_ticker(" infy.ns ") == "INFY"

def test_ticker_9():
    assert normalize_ticker("RELIANCE") == "RELIANCE"

def test_ticker_10():
    assert normalize_ticker(" reliance.bo ") == "RELIANCE" 

    # ---------------------------
# ADDITIONAL YEAR TESTS
# ---------------------------

def test_year_11():
    assert normalize_year("FY18") == 2018

def test_year_12():
    assert normalize_year("FY17") == 2017

def test_year_13():
    assert normalize_year("FY16") == 2016

def test_year_14():
    assert normalize_year("FY15") == 2015

def test_year_15():
    assert normalize_year("FY14") == 2014

def test_year_16():
    assert normalize_year("FY13") == 2013

def test_year_17():
    assert normalize_year("FY12") == 2012

def test_year_18():
    assert normalize_year("FY11") == 2011

def test_year_19():
    assert normalize_year(" 2020 ") == 2020

def test_year_20():
    assert normalize_year("FY 2022") == 2022


# ---------------------------
# ADDITIONAL TICKER TESTS
# ---------------------------

def test_ticker_11():
    assert normalize_ticker("HDFCBANK") == "HDFCBANK"

def test_ticker_12():
    assert normalize_ticker("hdfcbank") == "HDFCBANK"

def test_ticker_13():
    assert normalize_ticker(" hdfcbank.ns ") == "HDFCBANK"

def test_ticker_14():
    assert normalize_ticker("SBIN") == "SBIN"

def test_ticker_15():
    assert normalize_ticker("sbin.bo") == "SBIN"

def test_ticker_16():
    assert normalize_ticker("ITC") == "ITC"

def test_ticker_17():
    assert normalize_ticker("itc.ns") == "ITC"

def test_ticker_18():
    assert normalize_ticker("LT") == "LT"

def test_ticker_19():
    assert normalize_ticker("lt.bo") == "LT"

def test_ticker_20():
    assert normalize_ticker(" axisbank.ns ") == "AXISBANK"