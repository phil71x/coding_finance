import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Go to the website and read the html page
url = urlopen("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
# Parse the webpage using the BeautifulSoup Library
# We will save it to the soup variable
soup = BeautifulSoup(url.read(), 'lxml')
# Get the correct data table, 
# We want the table which has
# the constituents
tbody = soup.tbody
tr = tbody.find_all('tr')
# After getting the correct data
# We will need to iterate over it to
# extract just the text
# We will save it to the empty data list
data = []
for t in tr:
    data.append(t.text.split('\n'))
# Convert the list into a DataFrame
raw_df = pd.DataFrame(data)
# Change the column names to First Column
raw_df.columns = raw_df.iloc[0,:]
# Delete the first row data
raw_df = raw_df.iloc[1:,:]
# Read the head of the data table
print(raw_df)

sectors = raw_df.groupby('GICS Sector').count().iloc[:,0].sort_values()
sectors.plot(kind='bar')
plt.ylabel('Number of Constituents')
plt.xlabel('Sectors', fontsize=2)
plt.title('Sector Constituents in S&P 500')
plt.show()
