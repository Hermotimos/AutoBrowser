
def ask_number_pages():
    confirm = input('Enter number of pages to browse and confirm by ENTER:\n')
    try:
        confirm = int(confirm)
        assert confirm > 0
        return confirm
    except Exception as e:
        print('ERROR:', e)
        return ask_number_pages()


def yes_or_no(prompt):
    answer = input(prompt)
    if answer == 'y':
        return True
    elif answer == 'n':
        return False
    else:
        print("Wrong value entered. Please choose again.\n")
        return yes_or_no(prompt)


def ask_shutdown():
    choice = input("Choose shutdown mode after program finishes:\nshutdown - s\nhibernation - h\nnone - any key\n")
    mode = ''
    if choice == 's':
        mode = "shutdown /s /t 1"
    elif choice == 'h':
        mode = "shutdown /h"
    return mode



# todo: ask if start from start page or continue from current site?