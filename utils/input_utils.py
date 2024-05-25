import logging


def input_yn(question: str) -> bool:
    while True:
        user_input = input(question).strip().lower()
        if user_input == "y":
            logging.debug(f"Input yn == True")
            return True
        if user_input == "n":
            logging.debug(f"Input yn == False")
            return False
        print("\nInvalid input! Please enter 'y' or 'n'!")
