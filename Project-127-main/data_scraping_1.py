from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


bright_stars_url = 'https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars'

page = requests.get(bright_stars_url)
print(page)

soup = bs(page.text,'html.parser')

star_table = soup.find('table')

temp_list= []
table_rows = star_table.find_all('tr')
for tr in table_rows:
  td = tr.find_all('td')
  row = [i.text.rstrip() for i in td]
  temp_list.append(row)

Star_names = []
Distance =[]
Mass = []
Radius =[]
Lum = []

for i in range(1,len(temp_list)):
  Star_names.append(temp_list[i][1])
  Distance.append(temp_list[i][3])
  Mass.append(temp_list[i][5])
  Radius.append(temp_list[i][6])
  Lum.append(temp_list[i][7])
  
df2 = pd.DataFrame(list(zip(Star_names,Distance,Mass,Radius,Lum)),columns=['Star_name','Distance','Mass','Radius','Luminosity'])
print(df2)

df2.to_csv('bright_stars.csv')

def extract_table_data(url):
  """Extracts table data from a specified URL.

  Args:
      url (str): The URL of the webpage to scrape.

  Returns:
      list: A list of lists, where each inner list represents a row of data in the table.
  """

  try:
      response = requests.get(url)
      response.raise_for_status()  # Raise an exception for HTTP errors

      soup = BeautifulSoup(response.text, 'html.parser')

      # Get all tables on the page
      tables = soup.find_all('table')

      table_data = []
      for table in tables:
          rows = table.find_all('tr')
          for row in rows:
              cells = row.find_all('td')
              row_data = [cell.text.strip() for cell in cells]
              table_data.append(row_data)

      return table_data

  except requests.exceptions.RequestException as e:
      print(f"Error making request: {e}")
      return []

# Example usage
url = "Wikipedia-Brown Dwarf stars"
table_data = extract_table_data(url)

if table_data:
  print("Table data:")
  for row in table_data:
    print(row)
else:
  print("No table data found.")

# Assuming you have the table_data list from the function
df = pd.DataFrame(table_data)

# Save the DataFrame to a CSV file
df.to_csv("table_data.csv", index=False)

# Now you can use the table_data and handle potential IndexError
if table_data:
  # Assuming you want to use my_list to store a specific subset of table_data
  my_list = table_data[1:]  # Exclude the first row (header)

  try:
    # Make sure the index is within the valid range of my_list
    print(my_list[index])
  except IndexError:
    print("Index out of range")

# Load the CSV file into a DataFrame
df = pd.read_csv("brown_dwarf_stars.csv")

# Clean the data by removing NaN values
df.dropna(inplace=True)

df['Mass'] = pd.to_numeric(df['Mass'])
df['Radius'] = pd.to_numeric(df['Radius'])

# Assuming your DataFrame is named 'df'
df['Radius'] = df['Radius'] * 0.102763
df['Mass'] = df['Mass'] * 0.000954588

# Load the CSV files
df1 = pd.read_csv("brown_dwarf_stars.csv")  # Replace with the actual path
df2 = pd.read_csv("brightest_stars.csv")  # Replace with the actual path

# Merge the dataframes
merged_df = pd.concat([df1, df2], ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv("merged_stars.csv", index=False)