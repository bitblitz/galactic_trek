import io


# Helper functions
def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents


def character_range(a, b, inclusive=False):
    back = chr
    # if isinstance(a,unicode) or isinstance(b,unicode):
    #    back = unicode
    for c in range(ord(a), ord(b) + int(bool(inclusive))):
        yield back(c)

def inclusive_range(a, b):
    return range(a,b+1)

def ifNone(var, value):
    if var is None:
        return value
    return var
