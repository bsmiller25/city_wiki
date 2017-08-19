# city_wiki

Create an online tool that takes a city name as an input and scrapes Wikipedia for information about their type of government, current mayor, website URL, and a photo; stores that information in a database; and displays that information as a profile.

Hosted at: https://shrouded-mesa-37896.herokuapp.com/

## Programs

### app.py

Python script that uses flask to serve the front-end and handle the API requests. 

### scraper.py

Python script that searches wikipedia for user provided city name, scrapes the html, and stores the information in a postgres database.

### templates/index.html (name should change)

HTML code that gets the scraped city data from flask and displays it. 
Provides functionality for choosing other cities to display.

### templates/new_city.html

HTML code that allows the user to submit a city name that does not currently exist in the database. Passes the name back to server.py which runs scraper.py and redirects to the new page.

### Other notes:

When setting up, run the manual scraper at the CLI at least once (example: python scraper.py "New York City") in order to populate the table with at least one record. 
