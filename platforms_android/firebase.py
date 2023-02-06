import io
import re
import subprocess
import sys
import argparse


def enable_verbose_logging():
    """Enable verbose logging mode.

    Returns:
        proc (Popen): Instance of the Popen class. 
    """
    try:
        #subprocess.run("adb shell setprop log.tag.FA VERBOSE".split(" "))
        subprocess.run("adb shell setprop log.tag.FA-SVC VERBOSE".split(" "))
        proc = subprocess.Popen("adb logcat -v time -s FA FA-SVC".split(" "), stdout=subprocess.PIPE)
    except:
        print(f"Oops. There was an error. Make sure 'adb' is installed.")
        sys.exit(1)
    else:
        return proc


def edit_log(log: str):
    """Edits the log to better organize key values.

    Args:
        log (str): log/record to be edited.

    Returns:
        log (str): edited log/record.
    """
    log = re.sub(r"\w+\[\{", r"Bundle[{\n", log)
    log = re.sub(r"\}\]", r"\n}]", log)
    log = re.sub(r", |,", r"\n", log)

    return log


def no_arguments():
    """Displays logs of events being logged. 
    """
    proc = enable_verbose_logging()

    re_registered_event = re.compile(r"Logging\ event:")
    screenview_event = re.compile(r'name=screen_view')
    automatic_event = re.compile(r'origin=auto')

    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):

        if re_registered_event.search(line, re.IGNORECASE):
            line = edit_log(line)

            if screenview_event.search(line) and not automatic_event.search(line):
                print(f"\033[1;34m{line}\033[m")

            elif automatic_event.search(line):
                print(f"\033[1;90m{line}\033[m")
            else:
                print(f"\033[1;33m{line}\033[m")


def with_arguments(args: argparse.Namespace):
    """Filters the logs/records based on arguments given by the user.

    Args:
        args (argparse.Namespace): Arguments passed by the user in the call to execute the script.
    """
    if args.term1 == None and args.term2 == None: # Only -v exists in the call
        no_arguments()

    elif args.term1 != None and args.term2 != None:
        proc = enable_verbose_logging()
        re_terms = re.compile(rf"{args.term1}|{args.term2}")

        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            check_terms = list(set(re_terms.findall(line, re.IGNORECASE)))
            
            if len(check_terms) == 2:
                check_terms.sort() # sort - alphabetically
                line = edit_log(line)

                line = re.sub(f"{check_terms[0]}", f"\033[1;32;40m{check_terms[0]}\033[m", line)
                line = re.sub(f"{check_terms[1]}", f"\033[1;34;40m{check_terms[1]}\033[m", line)
                print(line)

    elif args.term1 != None or args.term2 != None:
        proc = enable_verbose_logging()
        term = args.term1 if args.term1 != None else args.term2
        re_terms = re.compile(rf"{term}")
        
        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            term_match = re_terms.search(line, re.IGNORECASE)         
            if term_match:
                line = edit_log(line)
                line = re.sub(term_match.group(), f"\033[1;32;40m{term_match.group()}\033[m", line)
                print(line)