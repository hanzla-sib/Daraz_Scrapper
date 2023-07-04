from flask import Flask,request,jsonify
from flask import jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Enter your MySQL password
    database="product_data"
)
cursor = conn.cursor()

# Create a table to store all data with specified headers
cursor.execute('''CREATE TABLE IF NOT EXISTS all_data
                  (id INT AUTO_INCREMENT PRIMARY KEY,
                  search_type VARCHAR(255),
                  name VARCHAR(255),
                  price VARCHAR(255),
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS latest_data
                  (id INT AUTO_INCREMENT PRIMARY KEY,
                  search_type VARCHAR(255),
                  name VARCHAR(255),
                  price VARCHAR(255),
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# Set the path to the chromedriver executable
chromedriver_path = 'path_to_chromedriver'


@app.route('/scrape', methods=['GET'])
def scrape_data():
    search_type = request.args.get('search_type', default='mobile')  # Get the search_type query parameter
    print(search_type)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening a browser window)

    # Start the webdriver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    # Navigate to the URL of the page you want to scrape
    driver.get(f'https://www.daraz.pk/catalog/?q={search_type}')


    # Wait for the dynamic content to load (you may need to adjust the wait time)
    driver.implicitly_wait(10)

    # Find the specific elements you want to scrape using Selenium's find_element method
    names = driver.find_elements(By.CSS_SELECTOR, '.title--wFj93')
    prices = driver.find_elements(By.CSS_SELECTOR, '.price--NVB62')

     # Specify the search type (e.g., 'mobile', 'laptop')

    
    cursor.execute("TRUNCATE TABLE latest_data")
    for i in range(10):
        name = names[i].text
        price = prices[i].text
        # print(name, price)

        cursor.execute('''INSERT INTO all_data (search_type, name, price)
                            VALUES (%s, %s, %s)''',
                        (search_type, name, price))
        cursor.execute('''INSERT INTO latest_data (search_type, name, price)
                            VALUES (%s, %s, %s)''',
                        (search_type, name, price))

    # Quit the webdriver
    driver.quit()

    # Commit the changes to the database
    conn.commit()

    return jsonify({'message': 'Scraping completed successfully'})

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Connect to MySQL
       
        cursor = conn.cursor()

        # Execute the query
        query = "SELECT * FROM latest_data"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries
        result = []
        for row in rows:
            # Assuming your table has three columns: id, name, and age
            data = {
                'id': row[0],
                'search_type': row[1],
                'name': row[2], 
                'price': row[3],
                
            }
            result.append(data)

        # Close the cursor and connection
        cursor.close()
        

        # Return the data as JSON
        return jsonify(result)

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)})


@app.route('/id_data', methods=['GET'])
def get_data_id():
    search_id = request.args.get('search_id')  # Accessing search_id from query parameter
    print(search_id)
    
    try:
        # Connect to MySQL
    

        cursor = conn.cursor()

        # Execute the query
        query = "SELECT * FROM all_data WHERE id = %s"  # Use placeholder for the search_id
        cursor.execute(query, (search_id,))

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries
        result = []
        for row in rows:
            data = {
                'id': row[0],
                'search_type': row[1],
                'name': row[2],
                'price': row[3],
            }
            result.append(data)

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the data as JSON
        return jsonify(result)

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)})
    

    
if __name__ == '__main__':
    app.run()
    
    
