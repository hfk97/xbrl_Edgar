import re

class xbrl_filing:

    elements=[]

    def __init__(self, path):

        lookup_balancesheet = {
            "Cash & Cash Equivalents": "us-gaap:CashAndCashEquivalentsAtCarryingValue",
            "ST Investments": "us-gaap:ShortTermInvestments",
            "Accounts & Notes Receiv": "us-gaap:AccountsAndNotesReceivableNet",
            "Inventories": "us-gaap:InventoryNet",
            "Total Current Assets": "us-gaap:Assets",
            "Property, Plant & Equip, Net": "us-gaap:PropertyPlantAndEquipmentNet",
            "LT Investments & Receivables": "us-gaap:LongTermInvestmentsAndReceivablesNet",
            "Total Noncurrent Assets": "us-gaap:OtherAssetsNoncurrent",
            "ST Debt": "us-gaap:ShorttermDebtFairValue",
            "Other ST Liabilities": "us-gaap:OtherLiabilitiesCurrent",
            "Total Current Liabilities": "us-gaap:LiabilitiesCurrent",
            "LT Debt": "us-gaap:LongTermDebtFairValue",
            "Other LT Liabilities": "us-gaap:OtherLiabilitiesNoncurrent",
            "Total Noncurrent Liabilities": "us-gaap:LiabilitiesNoncurrent",
            "Total Liabilities": "us-gaap:Liabilities",
            "Preferred Equity and Hybrid Capital": "us-gaap:PreferredStockValue",
            "Common Stock": "us-gaap:CommonStockValue",
            "Additional Paid in Capital": "us-gaap:AdditionalPaidInCapital",
            "Treasury Stock": "us-gaap:TreasuryStockCommonValue",
            "Retained Earnings": "us-gaap:RetainedEarningsAccumulatedDeficit",
            "Minority/Non Controlling Interest": "us-gaap:MinorityInterest",
            "Total Equity": "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
            "Total Liabilities & Equity": "us-gaap:LiabilitiesAndStockholdersEquity"
        }

        lookup_basics = {
            "Name": "dei:EntityRegistrantName",
            "Ticker": "dei:TradingSymbol",
            "Exchange": "dei:SecurityExchangeName",
            "Filing": "dei:DocumentType",
            "Period end date": "dei:DocumentPeriodEndDate",
            "CommonStockOutstanding": "dei:EntityCommonStockSharesOutstanding"
        }

        problems = []

        with open(path) as file:
            text = file.read().replace("\n", "")


        for i in lookup_basics.values():
            entry = re.compile("<" + i + "[^<]*</" + i + ">")
            if entry.search(text) is not None:
                self.elements.append(xbrl_basic(entry.search(text).group(0)))
            else:
                # print(i)
                problems.append(i)

        for i in lookup_balancesheet.values():
            entry = re.compile("<" + i + "[^<]*</" + i + ">")
            if entry.search(text) is not None:
                while entry.search(text) is not None:
                    self.elements.append(xbrl_element(entry.search(text).group(0)))
                    text = text.replace(entry.search(text).group(0), ' ')


            else:
                # print(i)
                problems.append(i)



        print("The following xbrl elements could not be found in file " + path + " :" + str(problems)+". \n")

    def print(self):
        for i in self.elements:
            i.print()





class xbrl_basic:

    name=""
    context="basics"
    value=""

    def __init__(self,load):

        load = load.replace('>', ' ')
        load = load.replace('=', ':')
        load = load.replace("<", "")
        load = load.replace("/", " ")
        load=load.split()


        for n, string in enumerate(load):
            #print(string)
            if "dei:" in string:
                self.name = string

            if n == len(load) - 2:
                self.value=string

    def print(self):
        print(self.name, self.value, self.context)



class xbrl_element:

    name=""
    context=""
    value=""

    def __init__(self,rawtext):
        main_load = re.compile(r'^\s*<.*:.*"?>([-a-zA-Z\d])+')

        number = re.compile("(-?\d+|INF)")
        cont = re.compile("[1-3][0-9]{3}(?:Q[1-4])?(?:YTD)?")


        load = main_load.match(rawtext).group(0)


        load = load.replace('>', ' ')
        load = load.replace('=', ':')
        load = load.replace("<", "")
        load=load.split()


        decimal = float(0)
        for n, string in enumerate(load):
            if "us-gaap:" in string:
                self.name = string

            if "contextRef:" in string:
                self.context = cont.findall(string)[0]

            if "decimals:" in string:
                if number.findall(string)[0] == "INF":
                    decimal=0.0
                else:
                    decimal = float(number.findall(string)[0])

            if n == len(load) - 1:
                try:
                    if self.name=="dei:EntityCentralIndexKey":
                        raise ValueError
                    self.value = round(float(string) * (10 ** decimal),2)
                except ValueError:
                    self.value = string

    def print(self):
        print(self.name, self.value, self.context)



testrun=xbrl_filing("/Users/Felix/Desktop/xml/form10qq219_htm.xml")

testrun.print()



#Todo write print funcitons for the classes


import sys

sys.exit()



class xbrl_filing:

    elements=[]

    def __init__(self, tex):

        lookup_balancesheet = {
            "Cash & Cash Equivalents": "us-gaap:CashAndCashEquivalentsAtCarryingValue",
            "ST Investments": "us-gaap:ShortTermInvestments",
            "Accounts & Notes Receiv": "us-gaap:AccountsAndNotesReceivableNet",
            "Inventories": "us-gaap:InventoryNet",
            "Total Current Assets": "us-gaap:Assets",
            "Property, Plant & Equip, Net": "us-gaap:PropertyPlantAndEquipmentNet",
            "LT Investments & Receivables": "us-gaap:LongTermInvestmentsAndReceivablesNet",
            "Total Noncurrent Assets": "us-gaap:OtherAssetsNoncurrent",
            "ST Debt": "us-gaap:ShorttermDebtFairValue",
            "Other ST Liabilities": "us-gaap:OtherLiabilitiesCurrent",
            "Total Current Liabilities": "us-gaap:LiabilitiesCurrent",
            "LT Debt": "us-gaap:LongTermDebtFairValue",
            "Other LT Liabilities": "us-gaap:OtherLiabilitiesNoncurrent",
            "Total Noncurrent Liabilities": "us-gaap:LiabilitiesNoncurrent",
            "Total Liabilities": "us-gaap:Liabilities",
            "Preferred Equity and Hybrid Capital": "us-gaap:PreferredStockValue",
            "Common Stock": "us-gaap:CommonStockValue",
            "Additional Paid in Capital": "us-gaap:AdditionalPaidInCapital",
            "Treasury Stock": "us-gaap:TreasuryStockCommonValue",
            "Retained Earnings": "us-gaap:RetainedEarningsAccumulatedDeficit",
            "Minority/Non Controlling Interest": "us-gaap:MinorityInterest",
            "Total Equity": "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
            "Total Liabilities & Equity": "us-gaap:LiabilitiesAndStockholdersEquity"
        }

        lookup_basics = {
            "Name": "dei:EntityRegistrantName",
            "Ticker": "dei:TradingSymbol",
            "Exchange": "dei:SecurityExchangeName",
            "Filing": "dei:DocumentType",
            "Period end date": "dei:DocumentPeriodEndDate",
            "CommonStockOutstanding": "dei:EntityCommonStockSharesOutstanding"
        }

        problems = []

        text = tex.replace("\n", "")


        for i in lookup_basics.values():
            entry = re.compile("<" + i + "[^<]*</" + i + ">")
            if entry.search(text) is not None:
                self.elements.append(xbrl_basic(entry.search(text).group(0)))
            else:
                # print(i)
                problems.append(i)

        for i in lookup_balancesheet.values():
            entry = re.compile("<" + i + "[^<]*</" + i + ">")
            if entry.search(text) is not None:
                while entry.search(text) is not None:
                    self.elements.append(xbrl_element(entry.search(text).group(0)))
                    text = text.replace(entry.search(text).group(0), ' ')

            else:
                # print(i)
                problems.append(i)



        print("The following xbrl elements could not be found in file " + path + " :" + str(problems))

    def print(self):
        for i in self.elements:
            i.print()

