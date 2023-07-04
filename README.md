# Daraz_Scrapper
The purpose of this application is to scrape product data from the website daraz.pk based on the specified search type (e.g., "mobile", "laptop"). It uses Selenium to automate web browsing and extract information such as product names and prices. The scraped data is then stored in a MySQL database for further use or analysis.


Install the required Python packages:
bash
Copy code
pip install -r requirements.txt

//MYSQL Connection
Set up the MySQL database:
Start your MySQL server and create a new database named product_data.
In the project directory, open app.py using a text editor.
Update the MySQL connection settings in the conn variable (host, user, password).
Save the changes.
s

Usage
Start your MySQL server (e.g., using XAMPP).
Run the Flask application:
bash
Copy code
python app.py
The Flask application will start running on http://localhost:5000.

Use the following endpoints to interact with the application:

Endpoints
GET /scrape?search_type={search_type}: Scrapes product data from daraz.pk for the specified search_type (e.g., mobile, laptop). The scraped data is stored in the database.

Example: http://localhost:5000/scrape?search_type=mobile

GET /data: Retrieves the latest scraped product data from the database.

Example: http://localhost:5000/data

GET /id_data?search_id={id}: Retrieves the product data for the specified id from the database.

Example: http://localhost:5000/id_data?search_id=1

Access the endpoints using a web browser or API testing tool (e.g., Postman).
