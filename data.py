import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

DATABASE = 'senti.db'  
DEFAULT_PID = 39  

def query_product_feedback(pid):
    """Query the database to fetch product feedback."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        
        cursor.execute('''
            SELECT p.product, c.company, f.feedback, f.timestamp, u.fname, u.lname
            FROM products p
            JOIN companies c ON p.cid = c.cid
            JOIN feedback f ON p.pid = f.pid
            JOIN users u ON f.uid = u.uid
            WHERE p.pid = ?
        ''', (pid,))
        
        data = cursor.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def generate_pdf(pid):
    """Generate a PDF report of product feedback."""
    data = query_product_feedback(pid)
    if not data:
        print(f"No feedback found for product with ID {pid}")
        return

    
    pdf_path = f"product_{pid}_feedback.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)

    
    product_name = data[0][0]
    company_name = data[0][1]

    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, f"Feedback Report - {company_name}")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Product: {product_name}")
    c.drawString(50, 710, f"Date of Generation: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    
    y = 680
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Name")
    c.drawString(200, y, "Feedback")
    c.drawString(500, y, "Timestamp")
    y -= 20

    
    c.setFont("Helvetica", 10)
    for feedback in data:
        user_name = f"{feedback[4]} {feedback[5]}"
        feedback_text = feedback[2]
        timestamp = feedback[3]

        
        wrapped_feedback = simpleSplit(feedback_text, "Helvetica", maxWidth=250, fontSize=12)
        
        
        c.drawString(50, y, user_name)
        for line in wrapped_feedback:
            c.drawString(200, y, line)
            y -= 12
        
        c.drawString(500, y + 12, timestamp)  
        y -= 20

        
        if y < 50:
            c.showPage()
            y = 750
            
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, "Name")
            c.drawString(200, y, "Feedback")
            c.drawString(500, y, "Timestamp")
            y -= 20
            c.setFont("Helvetica", 10)

    c.save()
    print(f"PDF generated successfully: {pdf_path}")

if __name__ == '__main__':
    print("Generating PDF...")
    generate_pdf(DEFAULT_PID)
