# user input module.  Can use scripted input for testing.
import time

g_input_queue = []

def queue_input(new_input:list):
    g_input_queue.extend(new_input)


def text_input(prompt):
    global g_input_queue
    if len(g_input_queue) == 0:
        return input(prompt)

    head, g_input_queue = g_input_queue[0], g_input_queue[1:]
    print(prompt, end='? ')
    print(head)

    # pause after auto-input
    time.sleep(500/1000.0)

    return head


def num_input(prompt, low, high):
    val = 0
    while True:
        number = text_input(prompt)

        try:
            val = int(number)
            if val < low or val > high:  # if not a positive int print message and ask for input again
                print("Invalid Value, try again!")
                continue
            break
        except ValueError:
            print("That's not a number!")
    return val

def command_input():
    return text_input('(W)arp, (I)mpulse, (G)alaxy Map:')