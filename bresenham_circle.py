import matplotlib.pyplot as plt

def bresenham_circle(xc, yc, r):
    x, y = 0, r
    d = 3 - 2 * r
    while x <= y:
        for px, py in [(xc+x, yc+y), (xc-x, yc+y), (xc+x, yc-y), (xc-x, yc-y),
                       (xc+y, yc+x), (xc-y, yc+x), (xc+y, yc-x), (xc-y, yc-x)]:
            print("Pixel", px, py)
            plt.plot(px, py, 'gs')
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    circle = plt.Circle((xc, yc), r, color="red", fill=False)
    plt.gca().add_patch(circle)
    plt.title("Bresenham Circle")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

bresenham_circle(0, 0, 10)
