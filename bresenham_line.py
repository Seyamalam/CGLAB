import matplotlib.pyplot as plt

def bresenham_line(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    p = 2 * dy - dx
    x, y = x1, y1
    while x <= x2:
        print("Pixel", x, y)
        plt.plot(x, y, 'gs')
        if p < 0:
            p = p + 2 * dy
        else:
            y = y + 1
            p = p + 2 * dy - 2 * dx
        x = x + 1
    plt.plot([x1, x2], [y1, y2], color="red")
    plt.title("Bresenham Line")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

bresenham_line(2, 2, 15, 8)
