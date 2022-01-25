from sklearn.cluster import KMeans
import cv2
from collections import Counter
from loguru import logger
from PIL import Image


def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def colors(file):
    image = get_image(file)
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)

    number_of_colors = 5
    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)

    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i] for i in counts.keys()]
    rgb_colors = [[int(c) for c in ordered_colors[i]] for i in counts.keys()]

    return rgb_colors


if __name__ == '__main__':
    dominant_colors = colors('psbank.ru.png')
    logger.info(dominant_colors)
    for color in dominant_colors:
        color = tuple([int(i) for i in color])
        color_block = Image.new(mode="RGB", size=(100, 100), color=color)
        color_block.show()