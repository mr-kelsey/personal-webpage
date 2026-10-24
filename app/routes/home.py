from fasthtml import common as Fast

from app.layout import site_layout

router = Fast.APIRouter()


@router("/")
def get():
    return site_layout(
        "Home",
        Fast.H1("I go where the failure mode is expensive."),
        Fast.P(
            "AI security engineer and machine learning engineer with a cybersecurity "
            "degree and a decade of contract work that didn't start anywhere near a "
            "computer. I've built the sensor-testing software the National Weather "
            "Service used for congressional approval, the computer vision system that "
            "catches $150K a month in medical waste before it happens, and the models "
            "underneath both.",
            cls="lede",
        ),
        Fast.P(
            Fast.A("See the work", href="/work"),
            " or ",
            Fast.A("read the résumé", href="/resume"),
            ".",
        ),
    )
