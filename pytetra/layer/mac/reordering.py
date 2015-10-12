
class TchsReorderer(object):
    tab = [
        35, 36, 37, 38, 39, 40, 41, 42, 43, 47, 48, 56, 61, 62, 63,
        64, 65, 66, 67, 68, 69, 70, 74, 75, 83, 88, 89, 90, 91, 92,
        93, 94, 95, 96, 97, 101, 102, 110, 115, 116, 117, 118, 119,
        120, 121, 122, 123, 124, 128, 129, 137,
        58, 85, 112, 54, 81, 108, 135, 50, 77, 104, 131, 45, 72,
        99, 126, 55, 82, 109, 136, 5, 13, 34, 8, 16, 17, 22, 23, 24,
        25, 26, 6, 14, 7, 15, 60, 87, 114, 46, 73, 100, 127, 44, 71,
        98, 125, 33, 49, 76, 103, 130, 59, 86, 113, 57, 84, 111,
        18, 19, 20, 21, 31, 32, 53, 80, 107, 134, 1, 2, 3, 4, 9,
        10, 11, 12, 27, 28, 29, 30, 52, 79, 106, 133, 51, 78, 105, 132,
    ]

    def __call__(self, b1):
        frame = [0] * 137

        for i, n in enumerate(self.tab):
            frame[n - 1] = b1[i]

        return frame