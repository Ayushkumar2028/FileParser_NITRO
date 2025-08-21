File Upload & Parsing API :

This project is a Django REST API that allows you to upload large files in chunks, track upload progress, parse file content (CSV, Excel, PDF), and manage uploaded files.

Features :

📂 Chunked file upload (large files supported)

📊 Upload progress tracking

📝 File parsing:

CSV → JSON

Excel (.xls, .xlsx) → JSON

PDF → Extracted text per page

🔎 View parsed file content

❌ Delete uploaded files

Tech Stack :

Backend: Django, Django REST Framework

Parsing: pandas, pdfplumber

Database: SQLite (default)

Setup Instructions
1. Clone the repo
git clone [https://github.com/Ayushkumar2028/your-repo.git](https://github.com/Ayushkumar2028/FileParser_NITRO.git) 
cd your-repo

2. Install Python dependencies

Install the required libraries :

    pip install django djangorestframework pandas pdfplumber openpyxl xlrd


  Notes:

    openpyxl is required for reading .xlsx Excel files.

  -> xlrd is required for reading .xls Excel files.

  -> pandas is used for CSV/Excel parsing.

  -> pdfplumber is used for extracting text from PDF files.

3. Run migrations
    python manage.py migrate

4. Start the server
python manage.py runserver

API Endpoints
1. Upload File 

POST /files/

Handles chunked file uploads.

Returns file ID & progress.

2. Get All Files

GET /files/

3. Track Upload Progress

GET /files/<file_id>/progress/

4. Get File Content

GET /files/<file_id>/content/

5. Delete File

DELETE /files/<file_id>/delete/


Notes

Uploaded files are stored in media/uploads/.

Temporary chunks go into media/tmp/.

Background parsing is done using Python threads for async.
