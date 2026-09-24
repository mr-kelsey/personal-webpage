from fasthtml import common as Fast

NAV_LINKS: tuple[tuple[str, str], ...] = (
    ("Home", "/"),
    ("About", "/about"),
    ("Resume", "/resume"),
    ("Work", "/work"),
    ("Blog", "/blog"),
    ("Contact", "/contact"),
)


class Layout:
    """Wraps page content in the site's shared nav and footer shell."""

    def __init__(self, site_title: str = "mr-kelsey") -> None:
        self.site_title = site_title

    def _nav(self) -> Fast.Nav:
        return Fast.Nav(*(Fast.A(label, href=href) for label, href in NAV_LINKS))

    def _footer(self) -> Fast.Footer:
        return Fast.Footer(f"© {self.site_title}")

    def __call__(self, page_title: str, *content) -> tuple:
        return (
            Fast.Title(f"{page_title} — {self.site_title}"),
            Fast.Link(rel="stylesheet", href="/static/css/site.css"),
            self._nav(),
            Fast.Main(Fast.Div(*content, cls="page")),
            self._footer(),
        )


site_layout = Layout()
