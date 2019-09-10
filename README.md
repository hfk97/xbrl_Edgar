# xbrl_Edgar

While I was working on a separate private project, crawling EDGAR to download SEC filings and parsing balance sheets, income and cash flow statements, I learned about xbrl and thought it might be worth looking into for data extraction purposes. 

This demo project extracts balance sheet data and basic information from the latest 10-K/Q filing of a randomly drawn SP500 company, by crawling EDGAR for the .xml filings and parsing them, looking for xbrl elements. The user can also specify the Ticker (must be SP500 company) and export the results to a .csv file.

Sadly, extracting conclusive data points, at the same abstraction level, from all filings proved harder then I anticipated. Companies often make extensive use of the extensibility of the standard, which makes writing a simple algorithm that extracts the same general information from all filings very complicated. This is why this project's primary purpose is to demonstrate some of my python skills.
