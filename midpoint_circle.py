import matplotlib.pyplot as plt

def midpoint_circle(xc, yc, r):
    x, y = 0, r
    p = 1 - r
    while x <= y:
        for px, py in [(xc+x, yc+y), (xc-x, yc+y), (xc+x, yc-y), (xc-x, yc-y),
                       (xc+y, yc+x), (xc-y, yc+x), (xc+y, yc-x), (xc-y, yc-x)]:
            print("Pixel", px, py)
            plt.plot(px, py, 'gs')
        if p < 0:
            p += 2 * x + 3
        else:
            p += 2 * (x - y) + 5
            y -= 1
        x += 1
    circle = plt.Circle((xc, yc), r, color="red", fill=False)
    plt.gca().add_patch(circle)
    plt.title("Midpoint Circle")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

midpoint_circle(0, 0, 10)
