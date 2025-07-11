from astar_manhattan import astar_puzzle as astar_manhattan
from astar_linear_conflict import astar_puzzle as astar_linear_conflict
import time

if __name__ == '__main__':
    goal_state = (
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    )

    samples = [
        # test1
        (
            (1,  2,  4,  8),
            (5,  7, 11, 10),
            (13, 15, 0,  3),
            (14, 6,  9, 12)
        ),
        # test2
        (
            (14, 10, 6,  0),
            (4,   9,  1,  8),
            (2,   3,  5, 11),
            (12, 13,  7, 15)
        ),
        # test3
        (
            (5,  1,  3,  4),
            (2,  7,  8, 12),
            (9,  6, 11, 15),
            (13, 10, 14, 0)
        ),
        # test4
        (
            (6,  10,  3, 15),
            (14,  8,  7, 11),
            (5,   1,  0,  2),
            (13, 12,  9,  4)
        ),
        # test5
        (
            (11,  3,  1,  7),
            (4,   6,  8,  2),
            (15,  9, 10, 13),
            (14, 12,  5,  0)
        ),
        # test6
        (
            (0,   5, 15, 14),
            (7,   9,  6, 13),
            (1,   2, 12, 10),
            (8,  11,  4,  3)
        ),
    ]

    print("manhattan:")
    for i, puzzle in enumerate(samples, start=1):
        print(f"=== 测试样例 {i} ===")
        start_time = time.perf_counter()
        result = astar_manhattan(puzzle, goal_state)
        end_time = time.perf_counter()
        if result is None:
            print("无解")
        else:
            print("解法步骤：", result)
        print("搜索用时：{:.4f} 秒".format(end_time - start_time))
        print()
    
    print("linear_conflict:")
    for i, puzzle in enumerate(samples, start=1):
        print(f"=== 测试样例 {i} ===")
        start_time = time.perf_counter()
        result = astar_linear_conflict(puzzle, goal_state)
        end_time = time.perf_counter()
        if result is None:
            print("无解")
        else:
            print("解法步骤：", result)
        print("搜索用时：{:.4f} 秒".format(end_time - start_time))
        print()