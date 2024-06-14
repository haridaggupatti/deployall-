from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF
import logging
import os

router = APIRouter()
logger = logging.getLogger(__name__)

def convert_resume_to_prompt(resume_text):
    # Example of converting resume text to a structured prompt
    prompt = "Here is the resume information:\n\n"
    
    sections = {
        'personal_info': "Personal Information:\n",
        'education': "Education:\n",
        'work_experience': "Work Experience:\n",
        'skills': "Skills:\n",
        'projects': "Projects:\n",
        'others': "Other Information:\n"
    }
    
    current_section = 'others'
    
    for line in resume_text.split('\n'):
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if 'education' in stripped_line.lower():
            current_section = 'education'
        elif 'work experience' in stripped_line.lower():
            current_section = 'work_experience'
        elif 'skills' in stripped_line.lower():
            current_section = 'skills'
        elif 'projects' in stripped_line.lower():
            current_section = 'projects'
        elif 'personal' in stripped_line.lower() or 'contact' in stripped_line.lower():
            current_section = 'personal_info'
        sections[current_section] += f"  {stripped_line} "
    
    for key, value in sections.items():
        prompt += value + "\n"
    
    # Remove excess newlines and ensure the formatting is clean
    prompt = prompt.replace('\n\n', '\n').replace('  ', ' ').replace('• ', '•')

    return prompt

@router.post("/upload_resume", tags=["Resume"])
async def upload_resume(file: UploadFile = File(...)):
    temp_file_path = "temp_resume.pdf"
    try:
        # Read the resume content
        resume_content = await file.read()
        
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as f:
            f.write(resume_content)
        
        # Open the PDF file with PyMuPDF
        doc = fitz.open(temp_file_path)
        resume_text = ""
        
        # Extract text from each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            resume_text += page.get_text()
        
        # Convert the resume text to a structured prompt
        resume_prompt = convert_resume_to_prompt(resume_text)
        
        logger.info(f"Resume processed successfully: {resume_prompt}")
        return {"message": "Resume uploaded and processed successfully", "resume_prompt": resume_prompt}
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
