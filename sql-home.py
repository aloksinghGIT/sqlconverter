import boto3
import os
import json
from botocore.exceptions import ClientError
from pandasai.llm import google_gemini #Tried Gemini to see if GCP Architecture can be generated
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
#Reference local modules
from filehandler import validate_file,STORAGE_DIR, parse_uploaded_file
from data import load_data


#Design the Page
# Set the app title
st.set_page_config(page_title="smart-cloud2aws", layout="wide")

# Add a header
st.header("          SQL CONVERTER  :weight_lifter:          ")
st.write("           Automate your modernization journey          ")
st.divider()

# Instantiate LLMs
def generate_llm_response(runtime="bedrock", model_ID = "", user_prompt = "", source_option = "", target_option = ""):
  if runtime == "bedrock":
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    # Set the model ID, e.g., Claude 3 Haiku.
    if model_ID == "":
      model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    else:
      model_id = model_ID

    # Define the prompt for the model.
    if user_prompt == "":
      prompt = "SELECT * FROM MYTABLE WHERE MYTABLE.YOU = 'YOU'"
    else:
      prompt = user_prompt
      
    # Define the system prompt for the model.
    system_prompt = f"""Convert the {source_option} SQL code to {target_option} code with high precision"""
    # Format the request payload using the model's native structure.
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.5,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]
    return response_text

  elif runtime == "gemini":
    llm = google_gemini.GoogleGemini(api_key=os.environ.get('GEMINI_API_KEY'), max_tokens=10000)

  return llm


# Build the Page
with st.container(border=False):
  cols = st.columns([50, 50])
  
  #Create the options for uses
  with cols[0].container(border=True,height=200):
    st.subheader("SOURCE OPTIONS")
    source_option = st.selectbox("YOUR SOURCE", ["ORACLE", "MS SQL Server"])
  with cols[1].container(border=True, height=200):
    st.subheader("TARGET OPTIONS")
    target_option = st.selectbox("YOUR TARGET", ["PostgreSQL", "MySQL", ".NET C#"])
  
  cols = st.columns([50,50])
  user_prompt = ""
  converted_Sql = ""
  #Work on the right side
  with cols[0].container(border=True):
    st.header("CURRENT SET-UP", divider=True)
    st.write("Upload your SQL File here or paste SQL in the input Box")
    #Create a file uploader widget 
    with st.expander("Upload your SQL/TXT File"):
      uploaded_file = st.file_uploader("Choose a file", type=["sql", "txt"])

    # Check if a file was uploaded
    if uploaded_file is not None:
    #Validate the file for right format
      error_code = validate_file(uploaded_file=uploaded_file)
      if error_code == 200: 
        st.success(f"CURRENT WORKING FILE = '{uploaded_file.name}'")
        with st.expander("View your SQL"):
          user_prompt = parse_uploaded_file(uploaded_file=uploaded_file)
          st.code(user_prompt, language="sql", line_numbers=True)
      elif error_code == 400: 
        st.error("Invalid file format. Please upload a CSV or Excel file.")
    else:
      st.warning("No file uploaded yet.")
      st.stop()  
    
    if st.button("Submit"):
      if user_prompt == "":
        user_prompt = st.text_area("Paste your SQL here")
        st.error("Please either upload a SQL/TXT file or paste your SQL statement in this box")
        st.stop()
      else:
        modelID = "anthropic.claude-3-sonnet-20240229-v1:0"
        converted_Sql = generate_llm_response(runtime="bedrock", model_ID=modelID, 
                                              user_prompt=user_prompt, source_option=source_option,
                                              target_option=target_option)

  #Work with Right Side 
  with cols[1].container(border=True,height=800):
    st.header("Your converted code",divider=True)
    st.write("You can download the file as well, by clicking on download button")
    with st.expander("View your converted SQL"):
     st.code(converted_Sql, language="sql", line_numbers=True)

    

    