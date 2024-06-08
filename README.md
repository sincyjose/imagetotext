### Design an image server

This Python project extracts text from an image of a menu, processes the extracted text to identify menu items and their prices, 
and then stores the information in a MySQL database.

### prerequisites

- Python 3.x installed on your machine.
- Tesseract OCR installed on your machine. You can download it from [here](https://github.com/tesseract-ocr/tesseract).
- MySQL Server installed and running.
- Required Python libraries: `pytesseract`, `Pillow`, `mysql-connector-python`, `argparse`.

### MySql

Ensure you have MySQL server installed and running. Create a database and a table to store the menu items using the following SQL commands:

CREATE DATABASE menu_db;

USE menu_db;

CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    items VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL
);

### Connecting to MySql

Ensure you have the MySQL server running and you have created the necessary database and table as mentioned above. You'll need the following information to connect to the MySQL database:

 - Database host (e.g., localhost)
 - Database username
 - Database password
 - Database name (e.g., menu_db)


### Running the Script

Run the script using the following command:

python main.py --tesseract_cmd "C:\tesseract.exe" --image_path "c:\menu2.jpg" --db_host "localhost" --db_user "root" --db_password "your_mysql_password" --db_name "menu_items"

Make sure to replace the placeholder values with your actual paths and credentials.

