from pypdf import PdfReader
from pypdf.generic import EncodedStreamObject

# Create a PDF reader object
reader = PdfReader('Test Master.pdf')

# Get the number of pages in the PDF
print(f"Number of pages: {len(reader.pages)}")

# Extract text from the first page
page = reader.pages[7]
print(page.extract_text())

