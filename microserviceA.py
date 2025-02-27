import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create directory to store PDFs
DIRECTORY = "generated_pdfs"
os.makedirs(DIRECTORY, exist_ok=True)

def generate_pdf(data):
    '''Generate a PDF for the user'''
    # Specify naming convention of new PDF
    filename = f"{data.get('name', 'pet')}_visit_information.pdf"
    pdf_path = os.path.join(DIRECTORY, filename)

    # Specify size of document and font/size
    doc = canvas.Canvas(pdf_path, pagesize=letter)
    doc.setFont("Times-Roman", 12)
    y = 700

    # Write the specified information to the document and save it
    doc.drawString(100, y, f"Name: {data.get('name', 'N/A')}")
    y -= 20
    doc.drawString(100, y, f"Date of Visit: {data.get('date_of_visit', 'N/A')}")
    y -= 20
    doc.drawString(100, y, f"Vet Clinic Name: {data.get('vet_clinic', 'N/A')}")
    y -= 20
    doc.drawString(100, y, f"Vet Name: {data.get('vet_name', 'N/A')}")
    y -= 20
    doc.drawString(100, y, "Description of Visit:")
    y -= 20
    doc.drawString(120, y, data.get('description', 'N/A'))
    y -= 20
    doc.drawString(100, y, "Medication Prescribed/Procedures Completed:")
    y -= 20
    doc.drawString(120, y, data.get('medication', 'N/A'))

    doc.save()
    return pdf_path

class PDFRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        '''Handles requests for a pdf'''
        if self.path == "/generate_pdf":
            # If request is to make a pdf, get the length of the data and read it
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            
            try:
                # parse JSON data and create pdf
                data = json.loads(post_data)
                pdf_path = generate_pdf(data)
                
                # If file is opened and read successfully, send 'success' respose (code = 200)
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
                self.end_headers()
                
                # Open the generated pdf and send it as a response
                with open(pdf_path, "rb") as pdf_file:
                    self.wfile.write(pdf_file.read())
            except Exception as e:
                # If an error occurs, send an error message as a response (code = 500)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())

def run_server():
    # Start the server so it can watch for requests to generate a pdf
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, PDFRequestHandler)
    print("Microservice A running on port 8080...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
