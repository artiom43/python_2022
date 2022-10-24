import numpy as np


class LifeGame(object):
    """
    Class for Game life
    """
    def __init__(self, list1: list[list[int]]) -> None:
        self.list = list1
        rows: int = len(list1)
        columns: int = len(list1[0])
        self.list_normal = list(np.zeros((rows + 2, columns + 2), dtype=int))
        for i in range(rows + 2):
            self.list_normal[i] = list(self.list_normal[i])
        for i in range(rows):
            for j in range(columns):
                self.list_normal[i + 1][j + 1] = list1[i][j]

    def get_next_generation(self) -> list[list[int]]:
        rows: int = len(self.list)
        columns: int = len(self.list[0])
        list_new: list[list[int]] = list(np.zeros((rows + 2, columns + 2), dtype=int))
        for i in range(rows):
            for j in range(columns):
                list_new[i + 1][j + 1] = self.list_normal[i + 1][j + 1]
        # print(self._count_neibors_fish(2, 1), 2, 1)
        # print(self._count_neibors_fish(2, 1), 2, 1)
        # print(self.list_normal)
        for i in range(rows):
            for j in range(columns):
                ii = int(i) + 1
                jj = int(j) + 1
                if self.list_normal[ii][jj] == 1:
                    continue
                if self.list_normal[ii][jj] == 2:
                    if self._count_neibors_fish(ii, jj) == 2 or self._count_neibors_fish(ii, jj) == 3:
                        pass
                    else:
                        list_new[ii][jj] = 0
                    continue
                if self.list_normal[ii][jj] == 3:
                    if self._count_neibors_shrimp(ii, jj) == 2 or self._count_neibors_shrimp(ii, jj) == 3:
                        pass
                    else:
                        list_new[ii][jj] = 0
                    continue
                if self.list_normal[ii][jj] == 0:
                    # print(self._count_neibors_fish(ii, jj), ii, jj)
                    # print(self.list_normal)
                    if self._count_neibors_fish(ii, jj) == 3:
                        list_new[ii][jj] = 2
                        continue
                    if self._count_neibors_shrimp(ii, jj) == 3:
                        list_new[ii][jj] = 3
                        continue
        for i in range(rows):
            for j in range(columns):
                self.list_normal[i + 1][j + 1] = list_new[i + 1][j + 1]
        for i in range(rows):
            for j in range(columns):
                self.list[i][j] = self.list_normal[i + 1][j + 1]
        # print(self.list)
        return self.list

    def _count_neibors_fish(self, i: int, j: int) -> int:
        list_i = [1, 1, 1, 0, 0, -1, -1, -1]
        list_j = [1, 0, -1, 1, -1, 1, 0, -1]
        answer: int = 0
        for index in range(8):
            ii = i + list_i[index]
            jj = j + list_j[index]
            if self.list_normal[ii][jj] == 2:
                answer = answer + 1
        return answer

    def _count_neibors_shrimp(self, i: int, j: int) -> int:
        list_i = [1, 1, 1, 0, 0, -1, -1, -1]
        list_j = [1, 0, -1, 1, -1, 1, 0, -1]
        answer: int = 0
        for index in range(8):
            ii = i + list_i[index]
            jj = j + list_j[index]
            if self.list_normal[ii][jj] == 3:
                answer = answer + 1
        return answer
