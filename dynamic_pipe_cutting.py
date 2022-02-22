"""
Recursive problem to solve the rod cutting problem.
Use memoization to improve runtime.

author: Reis Gadsden
version: 22/02/2022

class: CS-5531 @ Appalachian State University
instructor: Mohammad Mohebbi
"""


def main() -> None:
    price_arr = [1, 5, 8, 9, 10, 17, 17, 20]
    n = 24

    memo_arr = []
    for i in range(0, n + 1):
        memo_arr.append(-1)

    print(cut_rod(n, price_arr))
    print(cut_rod_memo(n, price_arr, memo_arr))
    return


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


if __name__ == "__main__":
    main()

