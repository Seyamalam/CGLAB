import matplotlib.pyplot as plt

def dda_line(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    steps = max(abs(dx), abs(dy))
    x_inc, y_inc = dx / steps, dy / steps
    x, y = x1, y1
    for _ in range(steps + 1):
        print("Pixel", round(x), round(y))
        plt.plot(round(x), round(y), 'gs')
        x += x_inc
        y += y_inc
    plt.plot([x1, x2], [y1, y2], color="red")
    plt.title("DDA Line")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

dda_line(2, 2, 15, 8)
