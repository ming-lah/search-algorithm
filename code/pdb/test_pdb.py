import time
from astar_pdb import load_or_generate_pdb, astar_puzzle
from idastar_pdb import load_or_generate_pdb, ida_star_puzzle

if __name__ == "__main__":

    goal_state = (
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    )

    tiles1 = [1, 2, 3, 4, 5]
    tiles2 = [6, 7, 8, 9, 10]
    tiles3 = [11, 12, 13, 14, 15]

    pdb_start_time = time.time()
    print("正在构建或加载 PDB1 ...")
    pdb1 = load_or_generate_pdb(goal_state, tiles1, "pdb_1.pkl")
    print("PDB1 状态数：", len(pdb1))
    print("正在构建或加载 PDB2 ...")
    pdb2 = load_or_generate_pdb(goal_state, tiles2, "pdb_2.pkl")
    print("PDB2 状态数：", len(pdb2))
    print("正在构建或加载 PDB3 ...")
    pdb3 = load_or_generate_pdb(goal_state, tiles3, "pdb_3.pkl")
    print("PDB3 状态数：", len(pdb3))
    pdb_end_time = time.time()
    print("PDB生成/加载时间：{:.4f}秒".format(pdb_end_time - pdb_start_time))
    print()

    # 6 个测试样例
    samples = [
        (
            # (1,  2,  4,  8),
            # (5,  7, 11, 10),
            # (13, 15, 0,  3),
            # (14, 6,  9, 12)
            # test 
            (5,  1,  2,  4),
            (9,  6,  3,  8),
            (13, 15, 10, 11),
            (14, 0,  7,  12)
        ),
        (
            (14, 10, 6,  0),
            (4,   9,  1,  8),
            (2,   3,  5, 11),
            (12, 13,  7, 15)
        ),
        (
            (5,  1,  3,  4),
            (2,  7,  8, 12),
            (9,  6, 11, 15),
            (13, 10, 14, 0)
        ),
        (
            (6,  10,  3, 15),
            (14,  8,  7, 11),
            (5,   1,  0,  2),
            (13, 12,  9,  4)
        ),
        (
            (11,  3,  1,  7),
            (4,   6,  8,  2),
            (15,  9, 10, 13),
            (14, 12,  5,  0)
        ),
        (
            (0,   5, 15, 14),
            (7,   9,  6, 13),
            (1,   2, 12, 10),
            (8,  11,  4,  3)
        ),
    ]

    print("=====astar_test=====")
    for i, puzzle in enumerate(samples, start=1):
        print(f"=== 测试样例 {i} ===")
        search_start_time = time.time()
        result = astar_puzzle(puzzle, goal_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3)
        search_end_time = time.time()
        if result is None:
            print("无解")
        else:
            print("解法步骤：", result)
        print("搜索时间：{:.4f}秒".format(search_end_time - search_start_time))
        print()

    print("=====idastar_test======")
    for i, puzzle in enumerate(samples, start=1):
        print(f"=== 测试样例 {i} ===")
        search_start_time = time.time()
        result = ida_star_puzzle(puzzle, goal_state, pdb1, pdb2, pdb3, tiles1, tiles2, tiles3)
        search_end_time = time.time()
        if result is None:
            print("无解")
        else:
            print("解法步骤：", result)
        print("搜索时间：{:.4f}秒".format(search_end_time - search_start_time))
        print()

