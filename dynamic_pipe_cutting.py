"""
Recursive problem to solve the rod cutting problem.
Use memoization to improve runtime.

author: Reis Gadsden
version: 22/02/2022

class: CS-5531 @ Appalachian State University
instructor: Mohammad Mohebbi
"""


import timeit
import re
import matplotlib.pyplot as plt
import numpy as np


def main(iters) -> list:
    price_arr = [1, 5, 8, 9, 10, 17, 17, 20]
    time_list = []
    time_list.append([])
    time_list.append([])
    for n in iters:
        n = int(n)
        memo_arr = []
        for i in range(0, n + 1):
            memo_arr.append(-1)

        start = timeit.default_timer()
        max_recur = cut_rod(n, price_arr)
        end = timeit.default_timer()
        recur_run_time = end - start
        time_list[0].append(recur_run_time)

        start = timeit.default_timer()
        max_memo = cut_rod_memo(n, price_arr, memo_arr)
        end = timeit.default_timer()
        memo_run_time = end - start
        time_list[1].append(memo_run_time)

    return time_list


def cut_rod(n, price_arr) -> int:
    if n == 0:
        return 0
    val = 0
    for i in range(0, min(n, len(price_arr))):
        val = max(val, price_arr[i] + cut_rod(n - i - 1, price_arr))
    return val


def cut_rod_memo(n, price_arr, memo_arr) -> int:
    if memo_arr[n - 1] >= 0:
        return memo_arr[n - 1]
    if n == 0:
        return n
    q = 0
    for i in range(0, min(n, len(price_arr))):
        q = max(q, price_arr[i] + cut_rod_memo(n - i - 1, price_arr, memo_arr))
    memo_arr[n - 1] = q
    return q


def compare_bars(time_list, labels):
    fig, ax = plt.subplots()
    x = np.arange(len(labels))
    print(x)
    width = 0.7 / len(labels)

    recur_bar = ax.bar(x - width/2, time_list[0], width, label="Recursion")
    memo_bar = ax.bar(x + width/2, time_list[1], width, label="Recursion w/ Memoization")

    ax.set_ylabel("Run Time")
    #ax.set_xlabel("Input Size (n)")
    ax.set_xticks(x, labels)
    ax.set_title("Recursion vs. Recursion w/ Memoization Timings")
    ax.legend()

    ax.bar_label(recur_bar, padding=3)
    ax.bar_label(memo_bar, padding=3)

    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    print("Timing the \"Dynamic Pipe Cutting\" Problem!\n")
    pattern = re.compile("^([0-9]*\\s)*[0-9]+$")
    iters = []
    while True:
        user_in = input("Please enter the numbers (seperated by a space) you want to test for: ").strip()
        if re.fullmatch(pattern, user_in):
            iters = user_in.split(" ")
            break
        print("Invalid input, please try again!")
    time_list = main(iters)
    compare_bars(time_list, iters)

