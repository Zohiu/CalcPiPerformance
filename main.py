# Digits of pi performance test thing
# Made by Zohiu

from queue import Queue
import decimal
import threading
import sys
import time


class Colors:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def compute_pi(n, q):
    decimal.getcontext().prec = n + 1
    C = 426880 * decimal.Decimal(10005).sqrt()
    K = 6.
    M = 1.
    X = 1
    L = 13591409
    S = L
    
    for i in range(1, n):
        M = M * (K ** 3 - 16 * K) / ((i + 1) ** 3)
        L += 545140134
        X *= -262537412640768000
        S += decimal.Decimal(M * L) / X
        q.put(i)
    
    pi = C / S
    q.put(n)
    return pi


def progressBar(name, value, endvalue, time, bar_length = 40, width = 20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '#'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(
        f"\r{Colors.BLUE}{name} {Colors.CYAN}: {Colors.BLUE}[{Colors.GREEN}{arrow + spaces}{Colors.BLUE}] {Colors.BLUE}{int(round(percent * 100))}% {Colors.CYAN}| {Colors.BLUE}({value}/{endvalue}) {Colors.CYAN}| {Colors.BLUE}{time}s"
    )
    sys.stdout.flush()
    if value == endvalue:
        sys.stdout.write('\n')


def main():
    digits = None
    queue = Queue()
    
    while digits is None:
        try:
            digits = int(input(f"{Colors.END}{Colors.MAGENTA}How many digits do you want to calculate?\n{Colors.CYAN}» {Colors.BOLD}"))
            if digits <= 0:
                print(f"{Colors.END}{Colors.RED}You have to pick a number higher than 0.{Colors.END}")
                digits = None
        except ValueError:
            print(f"{Colors.END}{Colors.RED}That's not a valid number!{Colors.END}")
    
    print(f"\n{Colors.END}{Colors.GREEN}Calculating {Colors.BOLD}{Colors.CYAN}{digits}{Colors.END}{Colors.GREEN} digits of pi.")
    
    thread = threading.Thread(target = compute_pi, args = (digits, queue))
    
    start = time.time()
    thread.start()
    
    while True:
        progress = queue.get()
        now = round(time.time() - start, 2)
        
        progressBar("Progress", progress, digits, now)
        
        if progress == digits:
            end = time.time()
            break
    
    execution_time = round(end - start, 5)
    dps = round(progress / execution_time, 2)
    
    print(f"\n{Colors.END}{Colors.GREEN}Calculated {Colors.CYAN}{Colors.BOLD}{progress}{Colors.END}{Colors.GREEN} digits of pi in {Colors.CYAN}{Colors.BOLD}{execution_time}{Colors.END}{Colors.GREEN} seconds. That's on average {Colors.CYAN}{Colors.BOLD}{dps}{Colors.END}{Colors.GREEN} digits per second.")
    
    again = input(f"{Colors.END}{Colors.MAGENTA}Run again? {Colors.BOLD}(y/n)\n{Colors.CYAN}» {Colors.BOLD}")
    if again == "y":
        print(f"\n{Colors.END}{Colors.BLUE}Restarting...\n")
        main()
    elif again == "n":
        print(f"\n{Colors.END}{Colors.YELLOW}Quitting...")
        exit(0)
    else:
        print(f"\n{Colors.END}{Colors.RED}Aborting...")
        exit(-1)


if __name__ == '__main__':
    main()