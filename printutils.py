"""The library provides a wrapper for built-it print() function

   Adds additional sub-methods for print()
   such as 'error', 'warn', 'info', 'success', 'log'

   Provides ability to pre customize messages to contain
   timestamps and arbitrary message title
   (for example file name or module name)

   Provides ability to control existing prints in the module
   Prints can be restricted in production mode via library config
"""
import builtins
import colorama
from copy import deepcopy
from datetime import datetime
from functools import wraps
from inspect import stack, getmodule, getmodulename

from bunch import Bunch

colorama.init()

DEFAULT_CONFIG = Bunch(
    allow_print=True,  # if False then any prints will not be executed
    decorate_pure_print=False,
    timestamp=True,  # if True then all the prints will be timestamped
    timestamp_format='%H:%M:%S',
    title=True
)

# colorama shortcuts
ERROR = colorama.Fore.RED
SUCCESS = colorama.Fore.GREEN
WARNING = colorama.Fore.YELLOW
INFO = colorama.Fore.CYAN
WHITE = colorama.Fore.WHITE

BRIGHT = colorama.Style.BRIGHT
RESET = colorama.Style.RESET_ALL


def print_utils_behavior(func):
    """
    This decorator applies configured printutils
    behavior to the PrintUtils functions
    :param func: Function to be decorated
    :return: Decorated function
    """
    @wraps(func)
    def decorated(instance, *args, **kwargs):
        if not instance.config.allow_print:  # prints not allowed in config
            return None
        if instance.config.timestamp:  # building timestamp string
            now = datetime.now()
            timestamp_format = instance.config.timestamp_format
            timestamp_string = '[' + now.strftime(timestamp_format) + '] :'
            args = (timestamp_string, ) + args  # adding timestamp to args
        if instance.config.title and instance.name:
            title = instance.name
            args = (title, ) + args  # adding title to args
        return func(instance, *args, **kwargs)
    return decorated


class Config:
    """
    Returns default config object copy
    that can be modified by the user
    """
    def __new__(cls):
        return deepcopy(DEFAULT_CONFIG)


class PrintUtils:
    """
    The built-in print() of the calling module
    will be changed to an instance of this class
    then printutils.init() is called
    """
    def __init__(self, *, python_print, name, config):
        self.python_print = python_print
        self.name = name
        self.config = config

    @staticmethod
    def _build_contains(iterable):
        return ' '.join([i.__str__() for i in iterable])

    @print_utils_behavior
    def decorated_pure_print(self, *args, **kwargs):
        self.python_print(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.config.decorate_pure_print:
            self.decorated_pure_print(*args, **kwargs)
        else:
            self.python_print(*args, **kwargs)

    @print_utils_behavior
    def log(self, *args, **kwargs):
        args = ('[L]', ) + args
        self.python_print(*args)

    @print_utils_behavior
    def info(self, *args, **kwargs):
        args = ('[I]', ) + args
        self.python_print(INFO + self._build_contains(args) + RESET)

    @print_utils_behavior
    def success(self, *args, **kwargs):
        args = ('[S]', ) + args
        self.python_print(SUCCESS + self._build_contains(args) + RESET)

    @print_utils_behavior
    def warning(self, *args, **kwargs):
        args = ('[W]', ) + args
        self.python_print(WARNING + self._build_contains(args) + RESET)

    @print_utils_behavior
    def error(self, *args, **kwargs):
        args = ('[E]', ) + args
        self.python_print(BRIGHT + ERROR + self._build_contains(args) + RESET)


def init(*, name=None, config=DEFAULT_CONFIG, explicit=False):
    """
    This method is initializing printutils behavior.
    Only calling module __dict__ will be changed.
    All the other modules will keep initial print built-in method.

    If no config was passed then DEFAULT_CONFIG will be used.
    :param name: identifier of the calling module to use in output
    :param config: printutils config object
    :param explicit: returns PrintUtils instance if True was passed
    Caller print() function stays unchanged. Else change callers print().
    :return: None if explicit=False else PrintUtils instance
    """
    python_print = deepcopy(builtins.print)
    caller_module = (getmodule(stack()[1][0]))
    if not name:
        name = caller_module.__name__
    utils_instance = PrintUtils(python_print=python_print,
                                name=name,
                                config=config)
    if explicit:
        return utils_instance
    else:
        caller_module.__dict__['print'] = utils_instance
        return None
