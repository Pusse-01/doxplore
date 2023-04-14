# from utils import bot, set_key
# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.responses import HTMLResponse
# from utils import bot
# import os

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Welcome to Doxplore!"}

# pdf_file_location = ""

# @app.post("/upload")
# async def upload_pdf(API_KEY:str, pdf_file: UploadFile = File(...)):
#     set_key(API_KEY)
#     global pdf_file_location
#     # Save the uploaded file to disk
#     pdf_file_location = f"{pdf_file.filename}"
#     with open(pdf_file_location, "wb") as file_object:
#         file_object.write(pdf_file.file.read())
#     return {"message": "PDF uploaded successfully!"}

# @app.post("/query")
# async def query_pdf(query: str):
#     global pdf_file_location
#     if not pdf_file_location:
#         return {"message": "Please upload a PDF file first!"}

#     # Call the bot function with the path to the saved file
#     answer = bot(pdf_file_location, query)

#     return {"answer": answer}

# @app.post("/delete")
# async def delete_pdf():
#     global pdf_file_location
#     global api_key

#     os.remove(pdf_file_location)
#     pdf_file_location = ""
#     api_key = ""
#     os.environ.pop("OPENAI_API_KEY", None)

#     return {"message": "PDF and API key deleted successfully!"}


# app = FastAPI()

# @app.post("/upload")
# async def upload(pdf_file: UploadFile = File(...), query: str = Form(...), api_key: str = Form(...)):
#     answer = bot(pdf_file.file, query, api_key)
#     return {"answer": answer}

# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/upload" method="post" enctype="multipart/form-data">
# <input name="pdf_file" type="file">
# <input name="query" type="text">
# <input name="api_key" type="text">
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)



from utils import bot, set_key
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

pdf_file_location = ""
api_key = ""

@app.route("/")
def read_root():
    return "Welcome to Doxplore!"

@app.route("/upload", methods=["POST"])
def upload_pdf():
    global pdf_file_location
    global api_key
    
    API_KEY = request.form.get("API_KEY")
    set_key(API_KEY)

    # Save the uploaded file to disk
    pdf_file = request.files["pdf_file"]
    filename = secure_filename(pdf_file.filename)
    pdf_file_location = os.path.join(os.getcwd(), filename)
    pdf_file.save(pdf_file_location)

    return {"message": "PDF uploaded successfully!"}

@app.route("/query", methods=["POST"])
def query_pdf():
    global pdf_file_location
    
    query = request.form.get("query")

    if not pdf_file_location:
        return {"message": "Please upload a PDF file first!"}

    # Call the bot function with the path to the saved file
    answer = bot(pdf_file_location, query)

    return {"answer": answer}

@app.route("/delete", methods=["POST"])
def delete_pdf():
    global pdf_file_location
    global api_key

    os.remove(pdf_file_location)
    pdf_file_location = ""
    api_key = ""
    os.environ.pop("OPENAI_API_KEY", None)

    return {"message": "PDF and API key deleted successfully!"}

if __name__ == "__main__":
    app.run(debug=True)
