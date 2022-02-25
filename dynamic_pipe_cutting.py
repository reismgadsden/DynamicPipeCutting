"""
Recursive problem to solve the rod cutting problem.
Use memorization to improve runtime.

:author - Reis Gadsden
:version - 25/02/2022
:github - https://github.com/reismgadsden/DynamicPipeCutting

:class - CS-5531 @ Appalachian State University
:instructor - Mohammad Mohebbi
"""


# necessary imports
from datetime import datetime # used to generate dates for file saving
import timeit # used to time the methods (time did not work on my machine)
import re # used to validate user input
import matplotlib.pyplot as plt # used to generate graphs
import numpy as np # used to generate ranges for graphs


'''
This method takes the user input gathered from main and runs the methods for the specified values
for the specified amount of time.

:return time_list - a list of lists that contain the average run time of the methods over n iterations.
'''
def run_time_tests(iters, samples) -> list:

    # price array contains prices for pipes
    #time_list is the container that holds the times for the methods
    #time_list[0] holds the time for the recursive method
    #time_list[1] holds the time for the recursive w/ memorization method
    #time list[2] holds the time for the dynamic programming method
    price_arr = [1, 5, 8, 9, 10, 17, 17, 20]
    time_list = [[], [], []]

    # run this loop for every pipe length the user gave as input
    for n in iters:
        # values to hold the run time of the methods over each iteration
        recur_run_time = 0
        memo_run_time = 0
        dp_run_time = 0

        # run this loop for the total number of iterations given by the user
        for i in range(0, samples):

            # clear the memo array as to not affect the run time of the memorization method
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

            # time the dynamic method and add it to the run time
            start = timeit.default_timer()
            max_dp = cut_rod_dp(n, price_arr)
            end = timeit.default_timer()
            dp_run_time += (end - start)

        # append the averages of the run times of the methods to their respective lists
        time_list[0].append(recur_run_time / samples)
        time_list[1].append(memo_run_time / samples)
        time_list[2].append(dp_run_time / samples)

    return time_list

'''
The normal recursive solution to the pipe cutting problem.

:return - the best possible price for a pipe of length n.
'''
def cut_rod(n, price_arr) -> int:
    # base case
    if n == 0:
        return 0

    # value to hold the best possible value
    val = 0

    # this loop runs through every possible configuration to make a pipe of length n.
    # val will hold the max value of this loop
    for i in range(0, min(n, len(price_arr))):
        val = max(val, price_arr[i] + cut_rod(n - i - 1, price_arr))
    return val


"""
The recursive w/ memorization solution to the pipe cutting problem.

:return - the best possible price for rod of length n
"""
def cut_rod_memo(n, price_arr, memo_arr) -> int:
    # if the best solution for a certain length has already been calculated return it
    if memo_arr[n - 1] >= 0:
        return memo_arr[n - 1]

    # base case
    if n == 0:
        return n

    # value to hold the best possible price
    q = 0

    # this loop runs through all possible configurations of prices and sets q to the best one
    for i in range(0, min(n, len(price_arr))):
        q = max(q, price_arr[i] + cut_rod_memo(n - i - 1, price_arr, memo_arr))

    # assign value to the backtracking table
    memo_arr[n - 1] = q

    return q


"""
The dynamic programming solution to the pipe cutting problem.

:return - best price for pipe length n
"""
def cut_rod_dp(n, price_arr) -> int:
    # initialize an empty array of length n
    dp_arr = [0 for x in range(0, n)]

    # value to hold the best possible price of the cut
    q = -1

    # this outer loop runs through every possible pipe length
    # the end of this loop assigns the best value for a cut to q
    # in order to have it saved for future access
    for i in range(0, n):

        # the inner loop runs through all possible configurations of a cut
        for j in range(min(i + 1, len(price_arr))):
            q = max(q, price_arr[j] + dp_arr[i - j - 1])
        dp_arr[i] = q

    return dp_arr[n - 1]


"""
This method creates a bar chart that shows the average run time of each method for the provided sizes.
"""
def compare_bars(time_list, labels, sample) -> None:
    # create subplots and axes
    fig, ax = plt.subplots()

    # calculate x, this will be useful for placing the bars
    x = np.arange(len(labels))

    # the width of the bars dynamically updates with the amount of pipes cit
    width = 0.7 / len(labels)

    # create the bars for each of the methods
    recur_bar = ax.bar(x - width, time_list[0], width, label="Recursion")
    memo_bar = ax.bar(x, time_list[1], width, label="Recursion w/ Memorization")
    dp_bar = ax.bar(x + width, time_list[2], width, label="Dynamic Programming")

    # set labels, legends, and ticks
    ax.set_ylabel("Average run time over " + str(sample) + " total iterations")
    ax.set_xticks(x, labels)
    ax.set_title("Recursion vs. Recursion w/ Memorization vs. Dynamic Programming Run Times")
    ax.legend()
    plt.xlabel("Pipe length")
    plt.yscale("log")
    ax.bar_label(recur_bar, padding=3)
    ax.bar_label(memo_bar, padding=3)
    ax.bar_label(dp_bar, padding=3)

    # apply tight layout just to make sure everything fits nicely
    fig.tight_layout()

    # save an image of the graph to the output folder
    # using the date to make sure every graph has unique name, name goes down to the second
    current_date = str(datetime.today()).strip().replace(" ", "_").replace("-", "_").replace(":", "_")
    plt.savefig("output/bar_" + current_date[0: current_date.index(".")] + ".png")


'''
This method generates a line graph that shows the change of runtime over pipe length.
This is useful for seeing how the methods' run times compare to each other
and for guessing at the big o of each method.
'''
def compare_lines(time_list, labels, sample) -> None:
    # create a range x, this will be used to assign the x ticks
    x = np.arange(1, len(labels) + 1)

    # plot each of the methods run times
    plt.plot(x, time_list[0], label="Recursion")
    plt.plot(x, time_list[1], label="Recursion w/ Memorization")
    plt.plot(x, time_list[2], label="Dynamic Programming")

    # set labels, legends, and ticks
    plt.legend()
    plt.xlabel("Pipe length")
    plt.ylabel("Average run time over " + str(sample) + " total iterations")
    plt.title("Recursion vs. Recursion w/ Memorization vs. Dynamic Programming Run Times")
    plt.xticks(x)
    plt.yscale("log")

    # save an image of the graph to the output folder
    # using the date to make sure every graph has unique name, name goes down to the second
    current_date = str(datetime.today()).strip().replace(" ", "_").replace("-", "_").replace(":", "_")
    plt.savefig("output/line_" + current_date[0: current_date.index(".")] + ".png")


"""
Main method of the program. Gathers and validates all user input. Passes input to run_time_tests method. Passes output
from that method to the graphing methods in order to generate graphs.
"""
def main() -> None:
    print("Timing the \"Dynamic Pipe Cutting\" Problem!\n")

    # iters holds the values of the length of pipes to cut
    # chart type is used later to determine which method to pass the run_time_tests output to
    iters = []
    chart_type = 0

    # outer loop gathers the user's choice of graph
    # the type of graph chosen will result in different prompts
    while True:
        user_in = input("1. Bar\n2. Line\nPlease enter the number of the graph you wish to generate: ")

        # this loop will execute if the user chooses a bar graph
        # the user is prompted to enter multiple numbers separated by spaces
        if user_in.strip()[0] == '1':
            while True:
                pattern = re.compile("^([0-9]*\\s)*[0-9]+$")
                user_in = input("Please enter the numbers (separated by a space) you want to test for: ").strip()
                if re.fullmatch(pattern, user_in):
                    chart_type = 1
                    iters = user_in.split(" ")
                    break
                print("Invalid input, please try again!")
            for i in iters[:]:
                iters[iters.index(i)] = int(i)
            iters.sort()
            break

        # this loop is executed if the user chooses a line graph
        # the user will be prompted to enter a single number (N)
        # this number will be used to generate a list of 1 to N to be passed to testing methods
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

    # sample is the number of times we want to run each method for an input n
    sample = 0
    pattern = re.compile("^[1-9]([0-9]*)$")

    # this loop will validate input for the sample size
    while True:
        user_in = input("Please enter the number of times you would like to test each number: ").strip()
        if re.fullmatch(pattern, user_in):
            sample = int(user_in)
            break
        print("Invalid input please try again!")

    # output of run_time_tests with user input
    time_list = run_time_tests(iters, sample)

    # decides which graph method to execute based on user input
    if chart_type == 1:
        compare_bars(time_list, iters, sample)
    elif chart_type == 2:
        compare_lines(time_list, iters, sample)
    else:
        print("wat")
        exit(-1)


# will execute the main method if this file is not being imported
if __name__ == "__main__":
    main()