# Aggregates images from around world with corresponding location information
# including continent, country, and (state?) city
import imports


def get_data(type):
    # type is the level of geographical specificity: continent, country, or state/city
    images = []  # RGB pixel matrix
    labels = []  # Label strings to be converted to scalars
    return images, labels

