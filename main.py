from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from app.input_handler import get_comand
from app.comands import HANDLERS, ADDRESS_BOOK
from app.Console.Console import Console, GreenConsole,RedConsole


def close():
    ADDRESS_BOOK.save_book()
    print("Thank you! Your dictionary is saved")

# створення підказок
def make_notes():
    from app.comands import CLOSE_COMANDS
    variants = {}
    for i in HANDLERS.keys():
        variants[i] = None
    for i in CLOSE_COMANDS:
        variants[i] = None
    # Створення об'єкта WordCompleter для автодоповнення
    return NestedCompleter.from_nested_dict(variants)

def main():
    GreenConsole.output('\r\nHello!!! \r\nYou can use "help" comand ')
    while True:
        try:
            enter_string = (prompt(">>>", completer=make_notes() )).strip()
            input_handler = get_comand(enter_string)
            is_close = next(input_handler)
            if is_close:
                close()
                break
            comand_exist, comand, args = next(input_handler)
            if comand_exist:
                data = HANDLERS[comand](args)
                GreenConsole.output(data)
            else:
                RedConsole.output(f'Comand "{comand}" not found')
        except KeyboardInterrupt:
            close()
            break

if __name__ == "__main__":
    main()



