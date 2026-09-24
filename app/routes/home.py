from fasthtml import common as Fast

from app.layout import site_layout

router = Fast.APIRouter()


@router("/")
def get():
    return site_layout(
        "Home",
        Fast.H1("Hi, I'm building something here."),
        Fast.P("Placeholder home page — real copy comes in the content pass."),
    )
