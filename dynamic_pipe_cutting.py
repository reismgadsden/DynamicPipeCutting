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


def run_time_tests(iters, samples) -> list:
    price_arr = [1, 5, 8, 9, 10, 17, 17, 20]
    time_list = []
    time_list.append([])
    time_list.append([])
    for n in iters:
        n = int(n)
        recur_run_time = 0
        memo_run_time = 0
        for i in range(0, samples):
            memo_arr = []
            for i in range(0, n + 1):
                memo_arr.append(-1)

            start = timeit.default_timer()
            max_recur = cut_rod(n, price_arr)
            end = timeit.default_timer()
            recur_run_time += (end - start)

            start = timeit.default_timer()
            max_memo = cut_rod_memo(n, price_arr, memo_arr)
            end = timeit.default_timer()
            memo_run_time += (end - start)

        time_list[0].append(recur_run_time / samples)
        time_list[1].append(memo_run_time / samples)


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


def compare_bars(time_list, labels, sample):
    fig, ax = plt.subplots()
    x = np.arange(len(labels))
    print(x)
    width = 0.7 / len(labels)

    recur_bar = ax.bar(x - width/2, time_list[0], width, label="Recursion")
    memo_bar = ax.bar(x + width/2, time_list[1], width, label="Recursion w/ Memoization")

    ax.set_ylabel("Average run time over " + str(sample) + " total iterations")
    ax.set_xticks(x, labels)
    ax.set_title("Recursion vs. Recursion w/ Memoization Timings")
    ax.legend()
    plt.xlabel("Pipe length")

    ax.bar_label(recur_bar, padding=3)
    ax.bar_label(memo_bar, padding=3)

    fig.tight_layout()

    plt.show()


def main() -> None:
    print("Timing the \"Dynamic Pipe Cutting\" Problem!\n")
    pattern = re.compile("^([0-9]*\\s)*[0-9]+$")
    iters = []
    while True:
        user_in = input("Please enter the numbers (seperated by a space) you want to test for: ").strip()
        if re.fullmatch(pattern, user_in):
            iters = user_in.split(" ")
            break
        print("Invalid input, please try again!")

    sample = 0
    pattern = re.compile("^[1-9]([0-9]*)$")
    while True:
        user_in = input("Please enter the number of times you would like to test each number: ").strip()
        if re.fullmatch(pattern, user_in):
            sample = int(user_in)
            break
        print("Invalid input please try again!")

    time_list = run_time_tests(iters, sample)
    compare_bars(time_list, iters, sample)


if __name__ == "__main__":
    main()