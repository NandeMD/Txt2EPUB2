import os

IS_POSIX = os.name == "posix"  # Check if os is a posix system
SPACING = 10                   # SPACING times blank space (" ")
COLORS = {                     # ANSI escape sequences
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "reset": "\u001b[0m"
}

# For colored printing in posix systems and spacings
def cprint(header: str, color: str, content: str):
    hdr = ""
    if IS_POSIX:
        hdr = f"{COLORS[color]}{header}{COLORS['reset']}"
        hdr = hdr + " " * (SPACING - len(header))
    else:
        hdr = header + " " * (SPACING - len(header))
        
    print(hdr + content)