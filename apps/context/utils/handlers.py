import packages

from context.utils import typer as t

print_hldr: t.Callable = print

def create_print_handler(
    destination: t.Literal["terminal"]="terminal",
    **kwargs
) -> t.Union[t.Callable, t.Any]:
    result = None

    if destination == "terminal":
        result = print

    return result