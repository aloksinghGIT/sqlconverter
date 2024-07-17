#USE THIS FILE FOR ALL FILE HANDLING RELATED FUNCTION
#TBD: Validate the CSV Template for missing Columns
#TBD: Understand each columns for the data it contains
#TBD: Handle for multi-file upload

import os
from io import StringIO

STORAGE_DIR = "data"

def validate_file(uploaded_file):

    file_name = uploaded_file.name
    file_extension = os.path.splitext(file_name)[1]
    if not (file_extension == ".sql" or file_extension == ".txt"):
        return 400

    # Save the file to the current working directory
    save_path = os.path.join(os.getcwd(),STORAGE_DIR, file_name)
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    if os.path.exists(save_path):
        os.remove(save_path)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return 200

def parse_uploaded_file(uploaded_file):
   # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # To read file as string:
    string_data = stringio.read()
    return string_data
