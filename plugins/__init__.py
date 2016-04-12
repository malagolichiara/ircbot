from os.path import dirname, basename, isfile
import glob
import imp


def init(comm_thread):
    modules = glob.glob(dirname(__file__) + "/*.py")
    for x in [f for f in modules if isfile(f) and basename(f) != '__init__.py']:
        with open(x, 'U') as ff:
            module = imp.load_module(x[:-3], ff, x, ('.py', 'U', 1))
            if not getattr(module, 'DISABLED', False):
                module.init(comm_thread)
