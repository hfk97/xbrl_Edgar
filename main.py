#This code gets the last 10-Q or 10-K filings from a random Fortune 500 company via the SEC "EDGAR" Database
import random

import pip

try:
	import sys

except ImportError:
	pip.main(['install', "sys"])
	import sys


import subprocess
import importlib



# function that imports a library if it is installed, else installs it and then imports it
def getpack(package):
    try:
        return (importlib.import_module(package))
        # import package
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package])
        return (importlib.import_module(package))
        # import package




bs4=getpack("bs4")
from bs4 import BeautifulSoup
urllib=getpack("urllib")
request=getpack("urllib.request")

from urllib.request import Request




def make_soup(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url, headers=headers)

    try:
        page = urllib.request.urlopen(req)  # conntect to website

    except:
        print("An error occured.")

    soup = BeautifulSoup(page, 'html.parser')
    return soup



def draw_comp():
    SP500 = ["MMM", "ABT", "ABBV", "ABMD", "ACN", "ATVI", "ADBE", "AMD", "AAP", "AES", "AMG", "AFL", "A", "APD", "AKAM",
             "ALK", "ALB", "ARE", "ALXN", "ALGN", "ALLE", "AGN", "ADS", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN",
             "AMCR", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "APC", "ADI",
             "ANSS", "ANTM", "AON", "AOS", "APA", "AIV", "AAPL", "AMAT", "APTV", "ADM", "ARNC", "ANET", "AJG", "AIZ",
             "ATO", "T", "ADSK", "ADP", "AZO", "AVB", "AVY", "BHGE", "BLL", "BAC", "BK", "BAX", "BBT", "BDX", "BRK.B",
             "BBY", "BIIB", "BLK", "HRB", "BA", "BKNG", "BWA", "BXP", "BSX", "BMY", "AVGO", "BR", "BF.B", "CHRW", "COG",
             "CDNS", "CPB", "COF", "CPRI", "CAH", "KMX", "CCL", "CAT", "CBOE", "CBRE", "CBS", "CE", "CELG", "CNC",
             "CNP", "CTL", "CERN", "CF", "SCHW", "CHTR", "CVX", "CMG", "CB", "CHD", "CI", "XEC", "CINF", "CTAS", "CSCO",
             "C", "CFG", "CTXS", "CLX", "CME", "CMS", "KO", "CTSH", "CL", "CMCSA", "CMA", "CAG", "CXO", "COP", "ED",
             "STZ", "COO", "CPRT", "GLW", "CTVA", "COST", "COTY", "CCI", "CSX", "CMI", "CVS", "DHI", "DHR", "DRI",
             "DVA", "DE", "DAL", "XRAY", "DVN", "FANG", "DLR", "DFS", "DISCA", "DISCK", "DISH", "DG", "DLTR", "D",
             "DOV", "DOW", "DTE", "DUK", "DRE", "DD", "DXC", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA",
             "EMR", "ETR", "EOG", "EFX", "EQIX", "EQR", "ESS", "EL", "EVRG", "ES", "RE", "EXC", "EXPE", "EXPD", "EXR",
             "XOM", "FFIV", "FB", "FAST", "FRT", "FDX", "FIS", "FITB", "FE", "FRC", "FISV", "FLT", "FLIR", "FLS", "FMC",
             "FL", "F", "FTNT", "FTV", "FBHS", "FOXA", "FOX", "BEN", "FCX", "GPS", "GRMN", "IT", "GD", "GE", "GIS",
             "GM", "GPC", "GILD", "GPN", "GS", "GWW", "HAL", "HBI", "HOG", "HIG", "HAS", "HCA", "HCP", "HP", "HSIC",
             "HSY", "HES", "HPE", "HLT", "HFC", "HOLX", "HD", "HON", "HRL", "HST", "HPQ", "HUM", "HBAN", "HII", "IDXX",
             "INFO", "ITW", "ILMN", "IR", "INTC", "ICE", "IBM", "INCY", "IP", "IPG", "IFF", "INTU", "ISRG", "IVZ",
             "IPGP", "IQV", "IRM", "JKHY", "JEC", "JBHT", "JEF", "SJM", "JNJ", "JCI", "JPM", "JNPR", "KSU", "K", "KEY",
             "KEYS", "KMB", "KIM", "KMI", "KLAC", "KSS", "KHC", "KR", "LB", "LHX", "LH", "LRCX", "LW", "LEG", "LEN",
             "LLY", "LNC", "LIN", "LKQ", "LMT", "L", "LOW", "LYB", "MTB", "MAC", "M", "MRO", "MPC", "MKTX", "MAR",
             "MMC", "MLM", "MAS", "MA", "MKC", "MXIM", "MCD", "MCK", "MDT", "MRK", "MET", "MTD", "MGM", "MCHP", "MU",
             "MSFT", "MAA", "MHK", "TAP", "MDLZ", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "MYL", "NDAQ", "NOV",
             "NKTR", "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI", "NBL", "JWN", "NSC",
             "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "ORLY", "OXY", "OMC", "OKE", "ORCL", "PCAR", "PKG", "PH",
             "PAYX", "PYPL", "PNR", "PBCT", "PEP", "PKI", "PRGO", "PFE", "PM", "PSX", "PNW", "PXD", "PNC", "PPG", "PPL",
             "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM", "PVH", "QRVO", "PWR", "QCOM", "DGX", "RL", "RJF",
             "RTN", "O", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "ROL", "ROP", "ROST", "RCL", "CRM", "SBAC",
             "SLB", "STX", "SEE", "SRE", "SHW", "SPG", "SWKS", "SLG", "SNA", "SO", "LUV", "SPGI", "SWK", "SBUX", "STT",
             "SYK", "STI", "SIVB", "SYMC", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TGT", "TEL", "FTI",
             "TFX", "TXN", "TXT", "TMO", "TIF", "TWTR", "TJX", "TMK", "TSS", "TSCO", "TDG", "TRV", "TRIP", "TSN", "UDR",
             "ULTA", "USB", "UAA", "UA", "UNP", "UAL", "UNH", "UPS", "URI", "UTX", "UHS", "UNM", "VFC", "VLO", "VAR",
             "VTR", "VRSN", "VRSK", "VZ", "VRTX", "VIAB", "V", "VNO", "VMC", "WAB", "WMT", "WBA", "DIS", "WM", "WAT",
             "WEC", "WCG", "WFC", "WELL", "WDC", "WU", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN", "XEL", "XRX", "XLNX",
             "XYL", "YUM", "ZBH", "ZION", "ZTS"]

    return SP500[random.randint(0,len(SP500))]


def get_tex(comp):

    if "." in comp:
        comp=comp.replace(".","")

        url = "https://sec.report/Ticker/"+ comp

        soup = make_soup(url)



        for table in soup.findAll('table'):
            allrows = []
            # print(table)
            for row in table.findAll('tr'):
                rowdata = []
                for column in row.findAll('td'):
                    if len(column.findAll('a', href=True)) != 0:
                        rowdata.append("https://www.sec.gov/" + column.findAll('a', href=True)[0]['href'])
                    else:
                        rowdata.append(column.text)
                    # print(column.text)
                allrows.append(rowdata)

            for i in allrows:
                try:
                    if i[0] == '10-K' | i[0] == '10-Q':

                            minisoup = make_soup(i[1])

                            # print("level 2")

                            for table in minisoup.findAll('table'):
                                allrows = []
                                # print(table)
                                for row in table.findAll('tr'):
                                    if "10-K" in row.text:
                                        # print("https://www.sec.gov/" + row.findAll('a', href=True)[0]["href"])
                                        newlink="https://www.sec.gov/" + row.findAll('a', href=True)[0]["href"]

                                        #print(c, int(i[3][0:4]) - 1,newlink)


                except IndexError as e:
                    print(e)
                    continue






        #ToDo navigate to xml file of 10-K/10-Q


    try:
        tex
    except:
        tex="testphase"

    return tex
