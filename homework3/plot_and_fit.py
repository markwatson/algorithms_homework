import math

def plot_and_fit(points, func=None):
    import matplotlib.pyplot as plt

    # setup the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # plot the points
    x, y = zip(*points)
    ax.plot(x, y, 'ro')

    # plot the curve
    if func is not None:
        scales = [y/func(x) for x, y in points]
        print scales
        scale = sum(scales)/len(scales)
        print scale
        scale = 0.8
        start = min(x for x, y in points) - 1
        end = max(x for x, y in points) + 1
        curve = [(x, scale*func(x)) for x in xrange(start, end, len(points))]
        x, y = zip(*curve)
        ax.plot(x, y, 'g-')

    # set additional settings and show plot
    ax.grid()
    #ax.set_xlim(0,50)
    #ax.set_ylim(0,50)
    ax.set_title('Closest Pair')
    plt.show()

def main():
    # Plot the results from tesating the closest pair

    #pts = [(10, 0.035), (100, 0.048), (1000, 0.094), (10000, 0.751), ]
    #(100000, 8.938), (1000000, 107.35)]
    pts = [(2,2), (3,3), (4,4)]
    plot_and_fit(pts, lambda x: x*math.log(x))
    #plot_and_fit(pts, lambda x: x)

if __name__ == "__main__":
    main()
