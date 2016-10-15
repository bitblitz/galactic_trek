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
    return range(a, b + 1)


def ifNone(var, value):
    if var is None:
        return value
    return var


class Rect:
    # initializer based on Tk's bounding boxes as lists
    def __init__(self, li):
        self.left = li[0]
        self.top = li[1]
        self.right = li[2]
        self.bottom = li[3]

    @staticmethod
    def fromCoord(l, t, r, b):
        return Rect((l, t, r, b))

    @staticmethod
    def fromRect(rc):
        return Rect.fromCoord(rc.left, rc.top, rc.right, rc.bottom)

    @staticmethod
    def union(rectList:list):
        r = None
        for rc in rectList:
            if r is None:
                r = rc
            elif rc is not None:
                r.inflate(rc)
        return r

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def inflate(self, rect):
        self.left = min(self.left, rect.left)
        self.top = min(self.top, rect.top)
        self.right = max(self.right, rect.right)
        self.bottom = max(self.bottom, rect.bottom)

