import requests

# Sample data in JSON format to send to the microservice
test_data = {
    "name": "Charlie",
    "date_of_visit": "2025-02-25",
    "vet_clinic": "Corvallis Veterinary Hostpital",
    "vet_name": "Dr. Murphy",
    "description": "Routine check-up and vaccination appointment",
    "medication": "Administered rabies vaccine"
}

# Send a POST request to the microservice
response = requests.post("http://localhost:8080/generate_pdf", json=test_data)

# If pdf was successfully generated and recieved, save the pdf
if response.status_code == 200:
    pdf_filename = "Charlie_visit_information.pdf"
    with open(pdf_filename, "wb") as f:
        f.write(response.content)
    # Let user know the pdf was generated successfully
    print(f"Test Passed: PDF received and saved as {pdf_filename}")
else:
    # Otherwise, let user know the pdf was not generated correctly
    print(f"Test Failed: Error {response.status_code} - {response.text}")
