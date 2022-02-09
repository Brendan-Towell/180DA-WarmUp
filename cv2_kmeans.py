"""
based off the script found at https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
the main differences were converting it to use a video feed instead of a static image, displaying
the dominant colors in real time (albeit with significant latency), and limiting the dominant color
detection to the central square
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

cap = cv2.VideoCapture(0)
xmin, xmax = 200, 280
ymin, ymax = 240, 400

while(1):
    _, originalImg = cap.read()
    img = cv2.cvtColor(originalImg, cv2.COLOR_BGR2RGB)[xmin:xmax, ymin:ymax]


    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(img)

    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)

    cv2.rectangle(originalImg, (ymin,xmin), (ymax,xmax), (255,255,255), 2)
    cv2.imshow('img',originalImg)
    cv2.imshow('colors', cv2.cvtColor(bar, cv2.COLOR_RGB2BGR))
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()