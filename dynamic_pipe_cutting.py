"""
Recursive problem to solve the rod cutting problem.
Use memoization to improve runtime
"""


def main() -> None:
    price_arr = [0, 1, 5, 8 , 9, 10, 17, 17, 20]
    n = 8
    print(cut_rod(n, price_arr))
    return


def cut_rod(n, price_arr) -> int:
    if n == 0:
        return 0
    q = 0
    for i in range(1, n + 1):
        q = max(q, price_arr[i] + cut_rod(n - i, price_arr))
    return q


def cut_rod_memo(n, price_arr) -> int:
    pass


if __name__ == "__main__":
    main()

