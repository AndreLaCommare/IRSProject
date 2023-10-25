# IRS Tax Preparer Search

This project is a simple Flask web application that allows users to search for tax preparers based on zip codes. It fetches the tax preparers' data from the IRS website and can display it sorted by either phone number or last name.

## Features

- Search tax preparers by zip code.
- Sort the displayed results by last name or phone number.
- Utilizes web scraping techniques to fetch data from the IRS website.

## Functionality

The core functionality is based on the Flask framework and web scraping techniques using BeautifulSoup4.

When a user submits a zip code and a sorting option, the application sends a request to the IRS website to fetch tax preparers' data corresponding to that zip code. It then parses this data to extract the relevant details, which are the last name and phone number of each tax preparer. The data is then sorted based on the chosen option and displayed on the web page.


