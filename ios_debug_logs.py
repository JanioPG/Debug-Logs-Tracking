import sys
import argparse
from platforms_ios import firebase_ios, universal_analytics_ios
from interface import title, options, clear_screen, verbose_custom


def receive_arguments():
    """Receives and handles the arguments passed in the call to execute the script.

    Returns:
        [argparse.Namespace]: All arguments received.
    """
    parser = argparse.ArgumentParser(description="Activate detailed logging and immediately see the events being sent. Use arguments to filter events or other information.")
    parser.add_argument("-t1", "--term1", type=str, help="First search term/correspondence.")
    parser.add_argument("-t2", "--term2", type=str, help="Second search term/correspondence.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    return parser.parse_args()


def user_choice(verbose: bool):
    """It displays the platforms (options) and receives the user's choice.

    Args:
        verbose (bool): Determines whether the programme description will be displayed to the user in the platform's choice menu.

    Returns:
        action (str): Index related to the platform option chosen by the user.
    """
    platforms = ["Firebase/GA4", "GA Universal", "Quit"] # remember to add "AppsFlyer" and "Google Tag Manager".
    action = ""
    msg = ""

    while action not in ["0", "1", "2"]:
        clear_screen()
        title("Debug Logs - iOS")
        if verbose:
            verbose_custom()
        options(platforms, msg)

        action = input(str("Option: ")).strip()
        msg = "\033[31mInvalid option. Choose between 0, 1 or 2.\033[m"
        
    return action


if __name__ == "__main__":
    args = receive_arguments()
    description = False
    
    if args.verbose:
            description = True

    action = user_choice(description)
    
    if (len(sys.argv) == 1):
        if action == "0":
            firebase_ios.get_event_log(number_arguments=0)
        elif action == "1":
            universal_analytics_ios.no_arguments()
        elif action == "2":
            pass
        # Add AppsFlyer and GTM.
    else:
        if action == "0":
            if args.term1 == None and args.term2 == None: # Only -v exists in the call
                firebase_ios.get_event_log(number_arguments=0)

            elif args.term1 != None and args.term2 != None:
                firebase_ios.get_event_log(number_arguments=2, term1=args.term1, term2=args.term2)

            elif args.term1 != None or args.term2 != None:
                term = args.term1 if args.term1 != None else args.term2
                firebase_ios.get_event_log(number_arguments=1, term1=term)

        elif action == "1":
            universal_analytics_ios.with_arguments(args)
        elif action == "2":
            pass

        # Add AppsFlyer and GTM.
    
    print("\033[1;32mFinished.\033[m")
    sys.exit(0)
