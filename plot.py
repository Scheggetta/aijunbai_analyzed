from matplotlib import pyplot as plt
import pandas as pd
from collections import defaultdict


def main(title, style="fivethirtyeight", end_line_extension=True):
    # plt.style.use(style)

    """
        Table:
        0: Iteration; 1: Move; 2: Q, 3: V; 4: N; 5: tU; 6: tR; 7: tT
    """
    """
    # 2
    table02 = pd.read_csv("stat/plain-uct_031021090658.csv")
    # 6
    table06 = pd.read_csv("stat/plain-uct_031021091025.csv")
    # 10
    table10 = pd.read_csv("stat/plain-uct_031021091333.csv")
    # 16
    table16 = pd.read_csv("stat/plain-uct_031021091736.csv")
    # 20
    table20 = pd.read_csv("stat/plain-uct_031021091955.csv")
    # 26
    table26 = pd.read_csv("stat/plain-uct_031021092240.csv")
    # 30
    table30 = pd.read_csv("stat/plain-uct_031021092406.csv")
    # 36
    table36 = pd.read_csv("stat/plain-uct_031021092546.csv")
    # 40
    table40 = pd.read_csv("stat/plain-uct_031021092636.csv")
    """# 46
    table46 = pd.read_csv("stat/plain-uct_031021092730.csv")
    # 50
    table50 = pd.read_csv("stat/plain-uct_031021092755.csv")
    # 56
    table56 = pd.read_csv("stat/plain-uct_031021092818.csv")
    # 58
    table58 = pd.read_csv("stat/plain-uct_031021092823.csv")

    """ Creating table """
    table = [[table46, table50], [table56, table58]]
    plt_title = [["Move n.46", "Move n.50"], ["Move n.56", "Move n.58"]]

    """ Creating matplotlib figure """
    plt_rows = 2
    plt_cols = 2
    fig, ax = plt.subplots(nrows=plt_rows, ncols=plt_cols, sharex=False)

    for plt_row in range(plt_rows):
        for plt_col in range(plt_cols):

            actual_table = table[plt_row][plt_col]
            actual_ax = ax[plt_row][plt_col]
            actual_title = plt_title[plt_row][plt_col]

            data_array = actual_table.get_values()
            moves = actual_table["Move"].unique()

            iteration = range(data_array.shape[0])
            data = defaultdict(list)
            # data[move]: [[iteration1, iteration2, ...], [value1, value2, ...], ...]

            for i in iteration:
                row = data_array[i]
                move = row[1]
                action_value = row[2]
                tU = row[5]
                tR = row[6]
                tT = row[7]

                if move not in data:
                    data[move] = [[0, i], [], [0, action_value], [], [], [0, tU], [0, tR], [0, tT]]
                else:
                    data[move][0].append(i)
                    data[move][2].append(action_value)
                    data[move][5].append(tU)
                    data[move][6].append(tR)
                    data[move][7].append(tT)

            max_i = max(iteration) + 1

            for m in moves:
                if end_line_extension:
                    max_iteration = len(data[m][0])
                    action_value = data[m][2][max_iteration - 1]

                    data[m][0].append(max_i)
                    data[m][2].append(action_value)

                actual_ax.plot(data[m][0], data[m][2], label=str(m))

                # The two following lines of code are here only for graphic clarity purposes
                # if m == str((7, 3)) or m == str((7, 4)) or m == str((3, 2)):
                #     continue

                # ax2.plot(data[m][0], data[m][5], label=str(m) + " tU")
                # ax2.plot(data[m][0], data[m][6], label=str(m) + " tR")
                # ax2.plot(data[m][0], data[m][7], label=str(m) + " tT")

            actual_ax.set_title(actual_title, fontsize=10.5)
            actual_ax.set_xlabel("Iterations")
            actual_ax.set_ylabel("Action value")

            # actual_ax.legend()

    plt.tight_layout()
    # fig.suptitle(title, fontsize=16)
    fig.set_size_inches(8, 6)
    plt.savefig("plt_fig.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    title = "Move action values over aijunbai_analyzed iterations in different states of an Othello game"
    main(title, end_line_extension=False)
