from .main import settrace, getsourcelines, dis, Int_, Bool_
from .color import Style


s = Style()


class ALine:

    def __init__(self, line: int = 0, print: bool = True):
        self.line: Int_ = Int_(line)
        self.code = None
        self.func_name = None
        self.filename = None
        self.sourceLine = None
        self.__print: Bool_ = Bool_(print)



main_func_name: str = ''
def analyse(in_call: bool = True, set_line: int = -1):
    """
    Print logs from callable lines to debug
    :param in_call: Print logs from called functions. If ``false``, only the current function was logged.
    :return: Callable
    """

    def analyse_decorator(func):
        # Permet de récupérer la fonction liée au décorateur

        def get_infos(frame, event: str, arg):
            """
            Fonction appellé à chaque ligne pour loguer celle-ci.
            :param frame:
            :param event: L'évènement actuellement executé
            :param arg: les arguments retournés
            :return:
            """
            global main_func_name

            line = frame.f_lineno
            code = frame.f_code
            func_name = code.co_name
            filename = code.co_filename
            immutable_in_call: Bool_ = Bool_(in_call) # gère si de mauvais types sont entré en paramètre
            immutable_set_line: Int_ = Int_(set_line) # gère si de mauvais types sont entré en paramètre

            # Si la fonction principale n'est pas enregistré
            if not main_func_name:
                main_func_name = func_name

            # Si on ne demande que la fonction principale et que le nom de la fonction actuellement exec est différente que celle setup en premier
            if not immutable_in_call.bool_ and main_func_name != func_name:
                return get_infos

            # Si on définit une ligne à dépasser pour commencer à loguer et que cette ligne n'a pas encore été dépassé
            if immutable_set_line.int_ != -1 and line < immutable_set_line.int_:
                return get_infos

            source_lines, starting_line = getsourcelines(frame.f_code) # On récupère toutes les lignes du code
            sourceLine = source_lines[line - starting_line].strip() # On obtient le contenue de la ligne actuellement exec

            __print_infos(event, line, arg, func_name, filename, sourceLine) # On print les informations

            return get_infos  # Continuer le traçage

        def wrapper(*args, **kwargs):
            global main_func_name

            settrace(get_infos) # On lance le tracking du module sys

            result = func(*args, **kwargs) # On execute la fonction de base

            settrace(None) # On arrête le tracking

            main_func_name = None # On reset la fonction principale pour ne pas rentrer en conflict au prochain appel
            return result

        return wrapper

    return analyse_decorator



def __print_infos(event, line, arg, func_name, filename, sourceLine) -> None:
    """
    Print all debug infos
    :param event: the line event https://docs.python.org/3.9/library/sys.html?highlight=settrace#sys.settrace
    :return: None
    """

    print(f"Event: {s.color_arg(event, s.BLUE, s.SURROUND)}, "
            f"Ligne: {s.color_arg(line, s.YELLOW)}, "
            f"Fonction: {s.color_arg(func_name, s.RED)} "
            f"{s.ITALICS}(file {filename})", s.DEFAULT)

    print(f"Content line : {s.color_arg(sourceLine, s.LIGHT_GREY)}")

    if event == 'return': # On regarde si l'event est un "return" pour print l'argument associé
        print(f"Return value : {s.color_arg(arg, s.GREEN)}, Type : {s.color_arg(type(arg), s.LIGHT_GREEN)}")

    print('\n')