from fasthtml import common as Fast
from starlette.responses import FileResponse

from app.layout import site_layout

RESUME_PDF_PATH = "static/resume.pdf"

router = Fast.APIRouter()


@router("/resume")
def get():
    return site_layout(
        "Resume",
        Fast.H1("Resume"),
        Fast.P("Placeholder resume content — real copy comes in the content pass."),
        Fast.A("Download PDF", href="/resume.pdf"),
    )


@router("/resume.pdf")
def get():
    return FileResponse(
        RESUME_PDF_PATH, filename="resume.pdf", media_type="application/pdf"
    )
