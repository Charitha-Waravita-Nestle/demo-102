import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType
from PyPDF2 import PdfFileReader

# Set up your Azure AI Search service details
endpoint = "YOUR_SEARCH_SERVICE_ENDPOINT"
admin_key = "YOUR_ADMIN_KEY"
index_name = "YOUR_INDEX_NAME"

# Create a SearchIndexClient to manage the index
index_client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(admin_key))

# Define the index schema
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SimpleField(name="content", type=SearchFieldDataType.String)
]

index = SearchIndex(name=index_name, fields=fields)
index_client.create_index(index)

# Create a SearchClient to upload documents
search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(admin_key))

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extract_text()
        return text

# Path to your PDF file
pdf_path = "path/to/your/file.pdf"

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Create a document to upload
document = {
    "id": os.path.basename(pdf_path),
    "content": pdf_text
}

# Upload the document to the index
search_client.upload_documents(documents=[document])

print("Document indexed successfully!")
 