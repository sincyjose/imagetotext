import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import mysql.connector
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MenuImageProcessor:
    def __init__(self, tesseract_cmd, image_path, db_host, db_user, db_password, db_name):
        self.tesseract_cmd = tesseract_cmd
        self.image_path = image_path
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd

    def load_image(self):
        try:
            # Open the image file
            image = Image.open(self.image_path)
            logging.info("Image loaded successfully.")

            # Enhance the image (optional)
            image = image.convert('L')  # Convert to grayscale
            image = image.filter(ImageFilter.SHARPEN)  # Apply sharpening filter
            return image
        except FileNotFoundError:
            logging.error("The specified image file was not found.")
            return None

    def connect_to_db(self):
        try:
            # Connect to MySQL database
            conn = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            logging.info("Connected to the database successfully.")
            return conn
        except mysql.connector.Error as err:
            logging.error(f"MySQL Error: {err}")
            return None

    def extract_text(self, image):
        try:
            # Perform OCR using PyTesseract
            text = pytesseract.image_to_string(image)
            
            # Print the extracted text
            logging.info("Extracted text:")
            logging.info(text)
            return text
        except Exception as e:
            logging.error(f"An error occurred during OCR: {e}")
            return None

    def preprocess_text(self, text):
        items_and_prices = []
        lines = text.split('\n')
        for line in lines:
            if 'Rs.' in line:
                parts = line.rsplit(' Rs. ', 1)
                if len(parts) == 2:
                    item = parts[0].strip()
                    try:
                        # Clean up the price string
                        price_str = parts[1].strip().replace('O', '0').replace('o', '0').replace(' ', '')
                        price = float(price_str)
                        items_and_prices.append((item, price))
                    except ValueError:
                        logging.warning(f"Skipping line due to invalid price: {line}")
        return items_and_prices

    def insert_data(self, items_and_prices, conn):
        try:
            if not items_and_prices or conn is None:
                return

            cursor = conn.cursor()

            # Insert data into the table
            for item, price in items_and_prices:
                cursor.execute('INSERT INTO menu (items, price) VALUES (%s, %s)', (item, price))

            # Commit the transaction and close the connection
            conn.commit()
            conn.close()
            logging.info("Data inserted successfully into the database.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Process an image to extract menu items and prices and store them in a MySQL database.')
    parser.add_argument('--tesseract_cmd', type=str, required=True, help='Path to the Tesseract executable')
    parser.add_argument('--image_path', type=str, required=True, help='Path to the image file')
    parser.add_argument('--db_host', type=str, required=True, help='MySQL database host')
    parser.add_argument('--db_user', type=str, required=True, help='MySQL database user')
    parser.add_argument('--db_password', type=str, required=True, help='MySQL database password')
    parser.add_argument('--db_name', type=str, required=True, help='MySQL database name')
    args = parser.parse_args()

    # Create an instance of MenuImageProcessor
    processor = MenuImageProcessor(args.tesseract_cmd, args.image_path, args.db_host, args.db_user, args.db_password, args.db_name)

    # Load the image
    image = processor.load_image() 

    # Connect to the database
    conn = processor.connect_to_db()

    # Extract text from the image
    text = processor.extract_text(image)

    # Preprocess the extracted text
    items_and_prices = processor.preprocess_text(text)

    # Insert preprocessed data into the database
    processor.insert_data(items_and_prices, conn)

if __name__ == "__main__":
    main()
