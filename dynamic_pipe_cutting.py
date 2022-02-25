"""
Recursive problem to solve the rod cutting problem.
Use memorization to improve runtime.

author: Reis Gadsden
version: 25/02/2022
github: https://github.com/reismgadsden/DynamicPipeCutting

class: CS-5531 @ Appalachian State University
instructor: Mohammad Mohebbi
"""


# necessary imports
from datetime import datetime # used to generate dates for file saving
import timeit # used to time the methods (time did not work on my machine)
import re # used to validate user input
import matplotlib.pyplot as plt # used to generate graphs
import numpy as np # used to generate ranges for graphs


def run_time_tests(iters, samples) -> list:

    # price array contains prices for pipes
    #time_list is the container that holds the times for both methods
    #time_list[0] holds the time for the recursive method
    #time_list[1] holds the time for the recursive w/ memorization method
    price_arr = [1, 5, 8, 9, 10, 17, 17, 20]
    time_list = [[], [], []]

    # run this loop for every pipe length the user gave as input
    for n in iters:
        # values to hold the run time of both methods over each iteration
        recur_run_time = 0
        memo_run_time = 0
        dp_run_time = 0

        # run this loop for the total number of iterations given by the user
        for i in range(0, samples):

            # clear the memo array as to not effect the run time of the memorization method
            # we want the run time in a vacuum not using values computed in the last iteration
            memo_arr = []
            for i in range(0, n + 1):
                memo_arr.append(-1)

            # time the regular recursive method and add it to the run time
            start = timeit.default_timer()
            max_recur = cut_rod(n, price_arr)
            end = timeit.default_timer()
            recur_run_time += (end - start)

            # time the memorized method and add it to the run time
            start = timeit.default_timer()
            max_memo = cut_rod_memo(n, price_arr, memo_arr)
            end = timeit.default_timer()
            memo_run_time += (end - start)

            start = timeit.default_timer()
            max_dp = cut_rod_dp(n, price_arr)
            end = timeit.default_timer()
            dp_run_time += (end - start)

        # append the averages of the run times of both methods to their respective lists
        time_list[0].append(recur_run_time / samples)
        time_list[1].append(memo_run_time / samples)
        time_list[2].append(dp_run_time / samples)


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


def cut_rod_dp(n, price_arr) -> int:
    dp_arr = [0 for x in range(0, n)]

    q = -1
    for i in range(0, n):
        for j in range(min(i + 1, len(price_arr))):
            q = max(q, price_arr[j] + dp_arr[i - j - 1])
        dp_arr[i] = q

    return dp_arr[n - 1]


def compare_bars(time_list, labels, sample):
    fig, ax = plt.subplots()
    x = np.arange(len(labels))
    width = 0.7 / len(labels)

    recur_bar = ax.bar(x - width, time_list[0], width, label="Recursion")
    memo_bar = ax.bar(x, time_list[1], width, label="Recursion w/ Memorization")
    dp_bar = ax.bar(x + width, time_list[2], width, label="Dynamic Programming")

    ax.set_ylabel("Average run time over " + str(sample) + " total iterations")
    ax.set_xticks(x, labels)
    ax.set_title("Recursion vs. Recursion w/ Memorization vs. Dynamic Programming Run Times")
    ax.legend()
    plt.xlabel("Pipe length")

    ax.bar_label(recur_bar, padding=3)
    ax.bar_label(memo_bar, padding=3)
    ax.bar_label(dp_bar, padding=3)

    fig.tight_layout()
    plt.yscale("log")

    current_date = str(datetime.today()).strip().replace(" ", "_").replace("-", "_").replace(":", "_")
    plt.savefig("output/bar_" + current_date[0: current_date.index(".")] + ".png")



def compare_lines(time_list, labels, sample) -> None:
    x = np.arange(1, len(labels) + 1)

    plt.plot(x, time_list[0], label="Recursion")
    plt.plot(x, time_list[1], label="Recursion w/ Memorization")
    plt.plot(x, time_list[2], label="Dynamic Programming")
    plt.legend()
    plt.xlabel("Pipe length")
    plt.ylabel("Average run time over " + str(sample) + " total iterations")
    plt.title("Recursion vs. Recursion w/ Memorization vs. Dynamic Programming Run Times")
    plt.xticks(x)
    plt.yscale("log")

    current_date = str(datetime.today()).strip().replace(" ", "_").replace("-", "_").replace(":", "_")
    plt.savefig("output/line_" + current_date[0: current_date.index(".")] + ".png")


def main() -> None:
    print("Timing the \"Dynamic Pipe Cutting\" Problem!\n")
    iters = []
    chart_type = 0

    while True:
        user_in = input("1. Bar\n2. Line\nPlease enter the number of the graph you wish to generate: ")
        if user_in.strip()[0] == '1':
            while True:
                pattern = re.compile("^([0-9]*\\s)*[0-9]+$")
                user_in = input("Please enter the numbers (seperated by a space) you want to test for: ").strip()
                if re.fullmatch(pattern, user_in):
                    chart_type = 1
                    iters = user_in.split(" ")
                    break
                print("Invalid input, please try again!")
            for i in iters[:]:
                iters[iters.index(i)] = int(i)
            iters.sort()
            break
        elif user_in.strip()[0] == '2':
            print("The line test will test values between 1 and N")
            while True:
                pattern = re.compile("^[1-9]([0-9]*)$")
                user_in = input("Please enter the value of N: ").strip()
                if re.fullmatch(pattern, user_in):
                    chart_type = 2
                    iters = list(range(1, int(user_in) + 1))
                    break
                print("Invalid input, please try again!")
            break
        else:
            print("Invalid input, please try again.")

    sample = 0
    pattern = re.compile("^[1-9]([0-9]*)$")
    while True:
        user_in = input("Please enter the number of times you would like to test each number: ").strip()
        if re.fullmatch(pattern, user_in):
            sample = int(user_in)
            break
        print("Invalid input please try again!")

    time_list = run_time_tests(iters, sample)

    if chart_type == 1:
        compare_bars(time_list, iters, sample)
    elif chart_type == 2:
        compare_lines(time_list, iters, sample)
    else:
        print("wat")
        exit(-1)


if __name__ == "__main__":
    main()