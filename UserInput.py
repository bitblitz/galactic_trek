# user input module.  Can use scripted input for testing.
import time
import Drawing
import Util
from datetime import timedelta, datetime

_input_queue = []
_query_queue = []

USE_CONSOLE_MODE = False


########################################################################################################################
# Input Queue - this is queue of input received to be consumed by the game
########################################################################################################################
def queue_input(new_input: list):
    global _input_queue
    _input_queue.extend(new_input)


def has_input():
    global _input_queue
    return len(_input_queue) != 0


def pop_next_input():
    global _input_queue
    if len(_input_queue) > 0:
        head, _input_queue = _input_queue[0], _input_queue[1:]
    else:
        head = None
    return head


def waitingInput():
    global _input_queue
    return len(_input_queue)


########################################################################################################################
# Query Queue - this is queue of questions to be asked of the user
########################################################################################################################
g_activeQuery = None


def waitingQuery():
    global _query_queue
    global g_activeQuery
    return len(_query_queue) + int(bool(g_activeQuery is not None))


def _clearActiveInput():
    global g_activeQuery
    g_activeQuery = None


def queue_query(new_query: list):
    global _query_queue
    # print("queueing query:", new_query)
    _query_queue.extend(new_query)


def has_query():
    global _query_queue
    return len(_query_queue) != 0 or g_activeQuery is not None


def pop_next_query():
    global _query_queue
    head, _query_queue = _query_queue[0], _query_queue[1:]
    return head


def clearQueryList():
    global _query_queue
    _query_queue = []


########################################################################################################################
# CONSOLE MODE
########################################################################################################################

def _console_text_input(prompt):
    if not has_input():
        return input(prompt)

    head = pop_next_input()
    print(prompt, end='? ')
    print(head)

    # pause after auto-input
    time.sleep(100 / 1000.0)

    return head


def console_num_input(prompt, low, high):
    val = 0
    while True:
        number = _console_text_input(prompt)

        try:
            val = int(number)
            if val < low or val > high:  # if not a positive int print message and ask for input again
                print("Invalid Value, try again!")
                continue
            break
        except ValueError:
            print("That's not a number!")
    return val


def console_command_input():
    return _console_text_input("Command?")


########################################################################################################################
# GUI (ASYNC) MODE
########################################################################################################################

# object representing a single prompt, reply, error set
class InputQuery:
    def __init__(self, prompt, validator, onComplete, onCancel=None, errMsg='bad input!', canRetry=True):
        self.prompt = prompt
        self.validator = validator
        self.errMsg = errMsg
        self.canRetry = canRetry
        self.currentInput = None
        self.showError = False
        self.errorTimeout = timedelta(seconds=5)
        self.inputTimeout = timedelta(microseconds=700 * 1000)
        self.inputAutoTime = datetime.now() + self.inputTimeout
        self.errorEndTime = datetime.now()
        self.onComplete = onComplete
        self.onCancel = onCancel
        self.takenInput = False  # has this query consumed any auto-input yet? limit to once
        self.errorInput = None

    def drawInput(self, left, top):
        rcPrompt = Drawing.print_at(left, top, self.prompt)

        autoInput = has_input() and not self.takenInput
        if autoInput:
            self.currentInput = pop_next_input()
            # print("Input Taken:", self.currentInput, datetime.now())
            self.takenInput = True
            try:
                self.preTransformInput()
            except AttributeError:
                pass

        rcInput = Drawing.print_at(left, rcPrompt.bottom + 5, '{0}', Util.ifNone(self.currentInput, ''))
        rcError = None
        if self.showError:
            # reset error if time has elapsed
            if datetime.now() > self.errorEndTime:
                self.showError = False
            else:
                text = Util.print_to_string(self.errMsg, '(', Util.ifNone(self.errorInput, 'none'), ')')
                rcError = Drawing.print_at(0, rcInput.bottom + 5, '{0}', text)

        # now that the input has been drawn at least once, check to see if there is input to consume
        if self.takenInput and datetime.now() > self.inputAutoTime:
            self.onReturn()

        # finally return the rectangle we consumed
        return Util.Rect.union([rcPrompt, rcInput, rcError])

    def onReturn(self):
        if self.currentInput is not None:
            if self.validator(self.currentInput):
                self.onComplete(self.currentInput)
                # done and move to the next prompt
                _clearActiveInput()
            else:
                self.showError = True
                self.errorEndTime = datetime.now() + self.errorTimeout
                self.inputAutoTime = self.errorEndTime + self.inputTimeout
                self.errorInput = self.currentInput
                self.currentInput = None

    def onBack(self):
        if self.currentInput is not None:
            self.currentInput = self.currentInput[:-1]
            if len(self.currentInput) == 0:
                self.currentInput = None

    def onEscape(self):
        clearQueryList()
        _clearActiveInput()
        if self.onCancel is not None:
            self.onCancel()

    def onText(self, event):
        if self.currentInput is None:
            self.currentInput = event.char
        else:
            self.currentInput = self.currentInput + event.char


class ChoiceQuery(InputQuery):
    def __init__(self, choices, **kwargs):
        super().__init__(validator=self.validate, **kwargs)
        self.choices = choices

    def validate(self, value):
        return value in self.choices

    def preTransformInput(self):
        self.currentInput = self.currentInput.upper()

    def onText(self, event):
        super().onText(event)
        self.currentInput = self.currentInput.upper()


class NumQuery(InputQuery):
    def __init__(self, minVal, maxVal, inclusive=True, **kwargs):
        super().__init__(validator=self.validate, **kwargs)
        self.minVal = minVal
        self.maxVal = maxVal
        self.inclusive = inclusive

    def validate(self, value):

        # print("validating: ", value, type(value))

        try:
            val = int(value)
            self.currentInput = val
        except ValueError:
            self.errMsg = "That's not a number!"
            return False

        self.errMsg = "Value out of Range!"

        valid = False
        if self.inclusive:
            valid = self.minVal <= val <= self.maxVal
        else:
            valid = self.minVal < val < self.maxVal

        if not valid:
            print("fail")
        return valid


########################################################################################################################
# Global Input Handling
########################################################################################################################

def InitializeInput():
    if USE_CONSOLE_MODE:
        return

    for c in Util.character_range('a', 'z', inclusive=True):
        Drawing.g_main_canvas.bind_all(c, gui_on_text)
    for c in Util.character_range('0', '9', inclusive=True):
        Drawing.g_main_canvas.bind_all(c, gui_on_text)

    Drawing.g_main_canvas.bind_all('<Return>', gui_on_return)
    Drawing.g_main_canvas.bind_all('<BackSpace>', gui_on_back)
    Drawing.g_main_canvas.bind_all('<Escape>', gui_on_escape)
    # Drawing.g_main_canvas.bind_all('<Return>', gui_on_return)
    Drawing.g_main_canvas.focus_set()


def drawInput(left, top):
    global g_activeQuery
    if g_activeQuery is None and has_query():
        g_activeQuery = pop_next_query()
    if g_activeQuery is not None:
        g_activeQuery.drawInput(left, top)


def gui_on_return(event):
    global g_activeQuery
    if g_activeQuery is not None:
        g_activeQuery.onReturn()


def gui_on_back(event):
    global g_activeQuery
    if g_activeQuery is not None:
        g_activeQuery.onBack()


def gui_on_escape(event):
    global g_activeQuery
    if g_activeQuery is not None:
        g_activeQuery.onEscape()


def gui_on_text(event):
    global g_activeQuery
    if g_activeQuery is not None:
        g_activeQuery.onText(event)
