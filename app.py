from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    taxPreparers = []
    zipCode = ""
    # Check if the request method is POST.
    if request.method == 'POST':
         # Retrieve the zip code and the field to sort by from the form data.
        zipCode = request.form['zip_code']
        sortBy = request.form['field']
        taxPreparers = getTaxPreparers(zipCode)
        
        # Sort tax preparers based on the provided field.
        if sortBy == 'lastname':
            taxPreparers.sort(key=lambda x: x['last_name'].lower())
            # print([prep['last_name'] for prep in preparers])
        elif sortBy == 'phone':
            taxPreparers.sort(key=lambda x: x['phone'])
    # Render the HTML template and send the tax preparers data.
    return render_template('index.html', preparers=taxPreparers, zip_code = zipCode)

# Get all tax preparers using the IRS website based on a given zip code.
def getTaxPreparers(zipCode):
    url = 'https://www.irs.gov/efile-index-taxpayer-search'
    searchParameters = {'zip': zipCode, 'state': 'All'}
    
    # Make a GET request with the search parameters.
    response = requests.get(url, params=searchParameters)
    soup = BeautifulSoup(response.content, 'html.parser')

    taxPreparers = []
    # Extract relevant data based on html element.
    preparersData = soup.find_all('td', class_='views-field views-field-nothing-1 views-align-left')

    # Extract phone and last name for each tax preparer and store it in a list.
    taxPreparers = [parsePhoneAndLastName(preparer.text.strip()) for preparer in preparersData]
    for i, prep in enumerate(taxPreparers):
        prep["full_entry"] = preparersData[i].text.strip()

    return taxPreparers

# Extract phone number and last name from a string containing tax preparer data.
def parsePhoneAndLastName(taxPreparer):
    # Find the phone number based on the position of parentheses.
    startParenthese = taxPreparer.find('(')
    endParenthese = taxPreparer.find(')', startParenthese) + 10  
    phone = taxPreparer[startParenthese:endParenthese]

    taxPreparerInfo = taxPreparer.split(' ')

    # Find the index of the last name based on the position of the phone number.
    # print(elements)  

    lastNameIndex = None

    for i, word in enumerate(taxPreparerInfo):
        if '(' in word:
            lastNameIndex = i
            #print(word)
            break

    if lastNameIndex is not None:
        lastName = taxPreparerInfo[lastNameIndex]
    else:
        lastName = None

    return {
        'last_name': lastName,
        'phone': phone
    }

if __name__ == "__main__":
    # The host and port may need to change to match PC running program
    app.run(debug= True, host='127.0.0.1', port=5000)