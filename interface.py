import os


def title(txt: str):
    """Prints the title in the menu.

    Args:
        txt (str): Title to be printed.
    """
    print("\033[1;34m-\033[m" * 35, end="\n\033[1;32m")
    print(f"{txt}".center(35), end="\033[m\n")
    print("\033[1;34m-\033[m" * 35)


def options(platforms: list, msg: str = ""):
    """Prints the platforms to be chosen by the user.

    Args:
        platforms (list): list of available platforms.
        msg (str, optional): error message. Defaults to "".
    """
    print("\033[1;90mAfter choosing the platform and \nthe logs are being displayed, to \nstop press 'CTRL + C'.\033[m\n")
    print("Choose the platform:")
    for i, item in enumerate(platforms):
        print(f"[{i}] - {item}")
    print(msg)
    

def clear_screen():
    """Clear the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")


def verbose_custom():
    """Prints text describing the purpose of the script.
    """
    text = "Use this script to immediately \nobserve the triggering of events, \nhelping you to verify that events \nare being sent. The script only \nenables detailed logging, allowing \nyou to check that events are being \nlogged correctly by the SDK. This \nincludes both manually and \nautomatically logged events.\n\nColor pattern:\n    \033[1;34mblue log\033[m - screenview\n    \033[1;33myellow log\033[m - event\n    \033[1;90mgray log\033[m - automatic\n"
    print(text)

if __name__ == "__main__":
    title("Debug Logs")