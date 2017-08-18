# city_wiki

Create an online tool that takes a city name as an input and scrapes Wikipedia for information about their type of government, current mayor, website URL, and a photo; stores that information in a database; and displays that information as a profile.

## Programs

### server.py

Python script that uses flask to serve the front-end and handle the API requests. 

### scraper.py

Python script that searches wikipedia for user provided city name, scrapes the html, and stores the information in a postgres database.

### templates/index.html (name should change)

HTML code that gets the scraped city data from flask and displays it. 
Provides functionality for choosing other cities to display.

### templates/new_city.html

HTML code that allows the user to submit a city name that does not currently exist in the database. Passes the name back to server.py which runs scraper.py and redirects to the new page.

### sql_connect.py

Standarized function for creating Postgres connection string.

Most of the development for the project was done on a remote Ubuntu server. Some, however was done on a train with poor WiFi connection so I used a virtual ubuntu box. I'm not sure what the difference between the setups is but the server needs the connection string to be Postgresql://localhost:5432/govex while the box needs Postgresql:///govex. I didn't dig too deeply into the issue because this fix was easy enough (and I guess makes the code more robust to possible postgres setups!)
