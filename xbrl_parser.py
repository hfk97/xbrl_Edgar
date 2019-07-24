import re

class xbrl_filing:

    elements=[]

    def __init__(self, path):

        starttagopen = re.compile('\s*<(us-gaap|dei):')
        #starttagopen = re.compile('\s*<(?!plt)(?!/?xbrli)(?!/?xbrldi).*:')
        endtagfind = re.compile(r'.*</\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\s*>$')
        oneliner = [starttagopen, endtagfind]


        for i in open(path):
            if all(pattern.match(i) is not None for pattern in oneliner):

                try:
                    #xbrl_element(i)
                    self.elements.append(xbrl_element(i))
                except AttributeError as e:
                    if "TextBlock" not in i:
                        print(str(e),i)



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
            if "dei:" in string or "us-gaap:" in string:
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




paths=["/Users/Felix/Desktop/0000002488-19-000045-xbrl/amd-20190330.xml"]

for i in paths:
    d=xbrl_filing(i)



for i in d.elements:
    print(i.name,i.value,i.context)


test="""<us-gaap:AccretionAmortizationOfDiscountsAndPremiumsInvestments contextRef="D2013Q3YTD" decimals="-3" id="Fact-304EE17EF9393141C8EF3E3D746D1DBB" unitRef="usd">-858000</us-gaap:AccretionAmortizationOfDiscountsAndPremiumsInvestments>"""

bla=xbrl_element(test)

starttagopen = re.compile('\s*<(us-gaap|dei):')

a="<us-gaap:AccretionAmortizationOfDiscountsAndPr"

print(starttagopen.match(a) is not None)