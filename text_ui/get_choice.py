def get_user_choice(q_string: str = None,
                    parse_string: bool = False,
                    var_count: int = 0) -> str:
    if parse_string:
        var_count = max([int(i) for i in q_string if i.isdigit()])
    variants = [str(i) for i in range(1, var_count + 1)]
    user_input = input(">> ")
    while user_input not in variants:
        print("You need to type: ", end='')
        print(*variants, sep=' or ', end='!')
        print()
        user_input = input(">> ")
    return user_input


def get_user_input(symbols=('y', 'n')):
    symbols = [symbol.lower() for symbol in symbols]
    symbols_string = '/'.join(symbols)
    ui = input(f'Type [{symbols_string}]: ')
    while ui not in symbols:
        print(f"You need to type something of: {symbols_string}")
        print()
        ui = input(f'Type [{symbols_string}]: ')
    return ui


def is_integer(value):
    try:
        int(value)
        return True
    except Exception as exc:
        return False
