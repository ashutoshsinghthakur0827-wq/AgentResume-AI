from pathlib import Path

import fitz
import pytesseract

from PIL import Image

from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel


from backend.app.services.resume_parser import parse_resume
from backend.app.services.ats_analyzer import analyze_resume
from backend.app.services.job_matcher import match_resume_with_job


app = FastAPI(
    title="AgentResume AI API",
    description=(
        "Multi-Agent Resume Intelligence, ATS Optimization "
        "and Career Recommendation Platform"
    ),
    version="1.0.0",
)


# ---------------------------------------
# CORS
# ---------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------
# Directories
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------
# Tesseract
# ---------------------------------------

TESSERACT_PATH = Path(
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if TESSERACT_PATH.exists():
    pytesseract.pytesseract.tesseract_cmd = str(
        TESSERACT_PATH
    )


# ---------------------------------------
# Request Models
# ---------------------------------------

class ResumeTextRequest(BaseModel):
    text: str


class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str


class CareerRecommendationRequest(BaseModel):
    parsed_resume: dict
    job_description: str = ""


# ---------------------------------------
# Basic Routes
# ---------------------------------------

@app.get("/")
def root():
    return {
        "success": True,
        "message": "AgentResume AI backend is running.",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {
        "success": True,
        "status": "healthy",
    }


@app.get("/api/project")
def project_info():
    return {
        "success": True,
        "project": "AgentResume AI",
        "features": [
            "PDF Upload",
            "OCR",
            "Resume Parsing",
            "ATS Analysis",
            "Job Matching",
            "Career Recommendation",
        ],
    }


# ---------------------------------------
# PDF Extraction
# ---------------------------------------

def extract_normal_pdf_text(
    file_path: Path,
) -> str:
    extracted_text = []

    try:
        document = fitz.open(str(file_path))

        for page in document:
            page_text = page.get_text()

            if page_text:
                extracted_text.append(page_text)

        document.close()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"PDF text extraction failed: {error}",
        )

    return "\n".join(extracted_text).strip()


def extract_ocr_text(
    file_path: Path,
) -> str:
    extracted_text = []

    try:
        document = fitz.open(str(file_path))

        for page in document:
            matrix = fitz.Matrix(2, 2)

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            image = Image.frombytes(
                "RGB",
                [
                    pixmap.width,
                    pixmap.height,
                ],
                pixmap.samples,
            )

            page_text = pytesseract.image_to_string(
                image
            )

            if page_text:
                extracted_text.append(page_text)

        document.close()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"OCR extraction failed: {error}",
        )

    return "\n".join(extracted_text).strip()


# ---------------------------------------
# Upload Resume
# ---------------------------------------

@app.post("/api/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is missing.",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    content = await file.read()

    max_size = 5 * 1024 * 1024

    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="PDF must be smaller than 5 MB.",
        )

    safe_filename = Path(
        file.filename
    ).name

    file_path = UPLOAD_DIR / safe_filename

    try:
        with open(file_path, "wb") as saved_file:
            saved_file.write(content)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not save file: {error}",
        )

    normal_text = extract_normal_pdf_text(
        file_path
    )

    if len(normal_text.strip()) >= 30:
        extracted_text = normal_text
        extraction_method = "normal_text_extraction"
    else:
        extracted_text = extract_ocr_text(
            file_path
        )
        extraction_method = "ocr"

    return {
        "success": True,
        "filename": safe_filename,
        "extracted_text": extracted_text,
        "extraction_method": extraction_method,
        "text_length": len(extracted_text),
        "message": "Resume uploaded successfully.",
    }


# ---------------------------------------
# Parse Resume
# ---------------------------------------

@app.post("/api/resume/parse")
def parse_resume_endpoint(
    request: ResumeTextRequest,
):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text is empty.",
        )

    try:
        parsed_data = parse_resume(
            request.text
        )

        return {
            "success": True,
            "data": parsed_data,
            "name": parsed_data.get("name", ""),
            "email": parsed_data.get("email", ""),
            "phone": parsed_data.get("phone", ""),
            "skills": parsed_data.get("skills", []),
            "education": parsed_data.get("education", ""),
            "experience": parsed_data.get("experience", ""),
            "projects": parsed_data.get("projects", ""),
            "certifications": parsed_data.get(
                "certifications",
                "",
            ),
            "summary": parsed_data.get(
                "summary",
                "",
            ),
            "raw_text": parsed_data.get(
                "raw_text",
                request.text,
            ),
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Resume parsing failed: {error}",
        )


# ---------------------------------------
# ATS Analysis
# ---------------------------------------

@app.post("/api/resume/analyze")
def analyze_resume_endpoint(
    request: ResumeTextRequest,
):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text is empty.",
        )

    try:
        result = analyze_resume(
            request.text
        )

        return {
            "success": True,
            "ats_score": result.get("ats_score", 0),
            "score": result.get("score", 0),
            "word_count": result.get("word_count", 0),
            "keyword_count": result.get(
                "keyword_count",
                0,
            ),
            "detected_skills": result.get(
                "detected_skills",
                [],
            ),
            "strengths": result.get(
                "strengths",
                [],
            ),
            "improvements": result.get(
                "improvements",
                [],
            ),
            "message": result.get(
                "message",
                "ATS analysis completed.",
            ),
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {error}",
        )


# ---------------------------------------
# Job Matching
# ---------------------------------------

@app.post("/api/resume/job-match")
def job_match_endpoint(
    request: JobMatchRequest,
):
    if not request.resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text is empty.",
        )

    if not request.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description is empty.",
        )

    try:
        result = match_resume_with_job(
            resume_text=request.resume_text,
            job_description=request.job_description,
        )

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Job matching failed: {error}",
        )


# ---------------------------------------
# Career Recommendation
# ---------------------------------------

@app.post("/api/resume/career-recommendation")
def career_recommendation_endpoint(
    request: CareerRecommendationRequest,
):
    """
    Basic safe response.
    You can connect your AI agents here later.
    """

    parsed_resume = request.parsed_resume

    skills = parsed_resume.get(
        "skills",
        [],
    )

    recommendations = []

    if "Python" in skills:
        recommendations.append("Python Developer")

    if "JavaScript" in skills:
        recommendations.append("Frontend Developer")

    if "React" in skills:
        recommendations.append("React Developer")

    if "SQL" in skills:
        recommendations.append("Data Analyst")

    if not recommendations:
        recommendations = [
            "Full Stack Developer",
            "Python Developer",
            "Data Analyst",
        ]

    return {
        "success": True,
        "candidate_profile": parsed_resume,
        "skill_gap": [],
        "recommendations": recommendations,
        "final_report": (
            "Your career recommendations were generated "
            "based on the detected resume skills."
        ),
    }