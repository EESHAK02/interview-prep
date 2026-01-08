# import json
# import uuid
# import time
# from datetime import datetime
# import os
# from PyPDF2 import PdfReader  # new dependency

def build_context(resume, jd, interviewer=None):
    ctx = f"""
Resume:
{resume}

Job Description:
{jd}
"""
    if interviewer:
        ctx += f"\nInterviewer Info:\n{interviewer}"

    return ctx
