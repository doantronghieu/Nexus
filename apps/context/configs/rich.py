# Colors: https://rich.readthedocs.io/en/stable/appendix/colors.html

from rich.console import Console
from rich.theme import Theme


UNIVERSAL_THEME = {
  "info": "blue bold",
  "path": "orange_red1 bold",
  "warning": "yellow bold",
  "error": "red bold",
  "success": "green bold",
  "header": "deep_sky_blue1 bold",
  "border": "navajo_white1",
  "title": "orange_red1 bold",
}

theme = Theme({
    "pretty": "bright_white",
    "type": "bright_yellow",
    "title": "bright_blue",
    "none": "bright_red"
})
console = Console(theme=theme)