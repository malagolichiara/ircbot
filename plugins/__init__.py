from os.path import dirname, basename, isfile, join, isdir
from os import listdir
import glob
import imp


def init(comm_thread):  # @todo refactor the code
    initfilename = '__init__.py'
    # files
    modules = glob.glob(dirname(__file__) + "/*.py")
    for x in [f for f in modules if isfile(f) and basename(f) != initfilename]:
        with open(x, 'U') as ff:
            module = imp.load_module(x[:-3], ff, x, ('.py', 'U', 1))
            if not getattr(module, 'DISABLED', False):
                module.init(comm_thread)
    # folder
    modules = listdir(dirname(__file__))
    for x in [d for d in modules if isdir(join(dirname(__file__),d))]:
        with open(join(dirname(__file__), x, initfilename), 'U') as ff:
            module = imp.load_module(x, ff, join(x, initfilename), ('.py', 'U', 1))
            if not getattr(module, 'DISABLED', False):
                module.init(comm_thread)
