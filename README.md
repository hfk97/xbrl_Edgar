# xbrl_Edgar

I was working on a seperate private project, crawling EDGAR to download SEC filings identify balance sheets, income and cashflow statements and extract information from them. I while trying to "standardize" the data I extracted I learned about xbrl and thought it might be worth looking into. 

This demo projects extracts balance sheet data and basic information about a filing from the last 20 10Q filings, by crawling EDGAR for the .xml filings and parssing them, looking for xbrl elements.

Sadly, extracting conclusive datapoints, at the same abstraction level, from all filings proved harder then I anticipated. Companies often make extensive use of the extensibility of the standard, which makes writing a simple algorithm that extracts  the same general information from all filings very complicated.
