from pypdf import PdfReader


def extract_resume_text(resume_file):
    reader = PdfReader(resume_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    return resume_text