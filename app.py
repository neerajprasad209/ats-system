import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os


from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel("gemini-pro")
    """
    You are a an Experience Techinal Human Resource Manager, your task is to review the provided reume against the job description.
    Please share the professional evaluation on weather the candidate's profile alings with the role.
    Highlight the strengths and weakness of the applicant in the relation to the specified job requirements. 
    """
    response = model.generate_content([input,pdf_content,prompt])
    return response.text

def input_pdf_text(upload_file):
    reader = pdf.PdfReader(upload_file)
    
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Prompt Template


input_prompt1 = """
You are a an Experience Techinal Human Resource Manager, your task is to review the provided reume against the job description.
Please share the professional evaluation on weather the candidate's profile alings with the role.
Highlight the strengths and weakness of the applicant in the relation to the specified job requirements. 

"""


input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science and ATS functionality,
Your task is to evaluate the Resume against the provided job description. Give me the Percentage of match if the resume matches the 
job description. First the output should come as percentage and then the keywords missing and the final Thoughts
"""

## Streamlit App

st.title("Application Tracking System (ATS):")
st.text("Improve Your Resume With ATS")

jd = st.text_area("Paste the Job Description")

upload_file = st.file_uploader("Upload Your Resume", type=['pdf'])

submit1 = st.button("Tell me about the Resume")

submit2 = st.button("Percentage Match")

if submit1:
    if upload_file is not None:
        text = input_pdf_text(upload_file)
        response = get_gemini_response(text,jd,input_prompt1)
        st.subheader("The Response is :")
        st.write(response)
    else:
        st.subheader("Please upload your resume")
        

if submit2:
    if upload_file is not None:
        text = input_pdf_text(upload_file)
        response = get_gemini_response(text,jd,input_prompt2)
        st.subheader("The Response is :")
        st.write(response)
    else:
        st.subheader("Please upload your resume")
