import os.path

try:
    import BigWorld
except ImportError:
    BigWorld = None


def exec_file(filename, exec_globals=None):
    '''
    Execute file
    Try to find file named `filename` and execute it. If `exec_globals` is
    specified it is used as globals-dict in exec context.
    '''
    if exec_globals is None:
        exec_globals = {}

    if not os.path.isfile(filename) and BigWorld is not None:
        filename = BigWorld.wg_resolveFileName(filename)

    with open(filename, 'r') as f:
        code = f.read()

    exec code in exec_globals
