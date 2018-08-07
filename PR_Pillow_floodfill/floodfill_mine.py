import time
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


def _color_diff(rgb1, rgb2):
    """
    Uses 1-norm distance to calculate difference between two rgb values.
    """
    return abs(rgb1[0]-rgb2[0]) + abs(rgb1[1]-rgb2[1]) + abs(rgb1[2]-rgb2[2])


def flood_fill_0(image, xy, value, thresh=0):
    pixel = image.load()
    x, y = xy
    try:
        background = pixel[x, y]
        if _color_diff(value, background) <= thresh:
            return  # seed point already has fill color
        pixel[x, y] = value
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = {(x, y)}
    full_edge = set()
    i = 0
    while edge:
        new_edge = set()
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):

                if (s,t) in full_edge:
                    continue
                i = i + 1
                try:
                    p = pixel[s, t]
                except IndexError:
                    pass
                else:
                    if _color_diff(p, background) <= thresh:
                        pixel[s, t] = value
                        new_edge.add((s, t))
                        full_edge.add((s, t))
        edge = new_edge
    print(i)


def flood_fill_mine(image, xy, value, thresh=0):
    pixel = image.load()
    x, y = xy
    try:
        background = pixel[x, y]
        if _color_diff(value, background) <= thresh:
            return  # seed point already has fill color
        pixel[x, y] = value
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = {(x, y)}
    full_edge0 = set()
    full_edge1 = set()
    i = 0
    while edge:
        new_edge = set()
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if ((s,t) in full_edge0) or ((s,t) in full_edge1):
                    continue
                i = i + 1
                try:
                    p = pixel[s, t]
                except IndexError:
                    pass
                else:
                    if _color_diff(p, background) <= thresh:
                        pixel[s, t] = value
                        new_edge.add((s, t))
                        full_edge0.add((s, t))
        full_edge0 = full_edge1
        full_edge1 = edge
        edge = new_edge
    print(i)


def floodfill_o(image, xy, value, border=None, thresh=0):
    """
    (experimental) Fills a bounded region with a given color.
    :param image: Target image.
    :param xy: Seed position (a 2-item coordinate tuple). See
        :ref:`coordinate-system`.
    :param value: Fill color.
    :param border: Optional border value.  If given, the region consists of
        pixels with a color different from the border color.  If not given,
        the region consists of pixels having the same color as the seed
        pixel.
    :param thresh: Optional threshold value which specifies a maximum
        tolerable difference of a pixel value from the 'background' in
        order for it to be replaced. Useful for filling regions of non-
        homogeneous, but similar, colors.
    """
    # based on an implementation by Eric S. Raymond
    pixel = image.load()
    x, y = xy
    try:
        background = pixel[x, y]
        if _color_diff(value, background) <= thresh:
            return  # seed point already has fill color
        pixel[x, y] = value
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = [(x, y)]
    i = 0
    if border is None:
        while edge:
            newedge = []
            for (x, y) in edge:
                for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    i = i + 1
                    try:
                        p = pixel[s, t]
                    except IndexError:
                        pass
                    else:
                        if _color_diff(p, background) <= thresh:
                            pixel[s, t] = value
                            newedge.append((s, t))
            edge = newedge

    else:
        while edge:
            newedge = []
            for (x, y) in edge:
                for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    try:
                        p = pixel[s, t]
                    except IndexError:
                        pass
                    else:
                        if p != value and p != border:
                            pixel[s, t] = value
                            newedge.append((s, t))
            edge = newedge
    print(i)


if __name__ == '__main__':

    img_path = 'rect-test-1000.jpg'
    # first mine
    img0 = Image.open(img_path)
    t1 = time.time()
    flood_fill_mine(img0, (1, 1), (0, 255, 0), 0)
    print(time.time() - t1)
    plt.imshow(img0)
    plt.ginput(1)
    plt.close()

    # first mine
    img0 = Image.open(img_path)
    t1 = time.time()
    flood_fill_0(img0, (1, 1), (0, 255, 0), 0)
    print(time.time() - t1)
    plt.imshow(img0)
    plt.ginput(1)
    plt.close()

    # second original
    img1 = Image.open(img_path)
    t1 = time.time()
    floodfill_o(img1, (1,1), (0,255,0), None, 0)
    print(time.time() - t1)
    plt.imshow(img1)
    plt.ginput(1)
    plt.close()
