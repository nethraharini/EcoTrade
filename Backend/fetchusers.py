from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import Flask
from flask_pymongo import PyMongo
from reportlab.lib import colors

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/role_portal'
mongo = PyMongo(app)

# Function to fetch data from all collections and generate PDF
def fetch_and_generate_pdf():
    # Fetching all data from Admins, Buyers, and Sellers collections
    admins = mongo.db.admins.find()
    buyers = mongo.db.buyers.find()
    sellers = mongo.db.sellers.find()

    # Preparing data for Admins, Buyers, and Sellers
    admin_data = []
    for admin in admins:
        admin_data.append([admin['username'], admin['email']])

    buyer_data = []
    for buyer in buyers:
        buyer_data.append([buyer['username'], buyer['email']])

    seller_data = []
    for seller in sellers:
        seller_data.append([seller['username'], seller['email']])

    # Tabulate the data for each role
    admin_table = tabulate(admin_data, headers=["Admin Username", "Admin Email"], tablefmt="grid")
    buyer_table = tabulate(buyer_data, headers=["Buyer Username", "Buyer Email"], tablefmt="grid")
    seller_table = tabulate(seller_data, headers=["Seller Username", "Seller Email"], tablefmt="grid")

    # Create a PDF file with the table data
    pdf_filename = "role_based_report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Set up font and size
    c.setFont("Helvetica", 10)
    c.drawString(30, height - 30, "Role-Based User Data Report")

    # Write Admin data to PDF
    y_position = height - 50
    c.drawString(30, y_position, "Admin Data:")
    y_position -= 15
    lines = admin_table.splitlines()
    for line in lines:
        c.drawString(30, y_position, line)
        y_position -= 15

    # Add space between tables
    y_position -= 30

    # Write Buyer data to PDF
    c.drawString(30, y_position, "Buyer Data:")
    y_position -= 15
    lines = buyer_table.splitlines()
    for line in lines:
        c.drawString(30, y_position, line)
        y_position -= 15

    # Add space between tables
    y_position -= 30

    # Write Seller data to PDF
    c.drawString(30, y_position, "Seller Data:")
    y_position -= 15
    lines = seller_table.splitlines()
    for line in lines:
        c.drawString(30, y_position, line)
        y_position -= 15

    # Save the PDF file
    c.save()

    print(f"PDF generated successfully: {pdf_filename}")

# Run the function
fetch_and_generate_pdf()
