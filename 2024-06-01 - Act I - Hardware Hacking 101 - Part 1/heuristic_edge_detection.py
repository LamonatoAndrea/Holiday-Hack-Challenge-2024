import os
import numpy as np
from PIL import Image

def load_images(folder):
    images = []
    filenames = sorted(os.listdir(folder))
    for filename in filenames:
        if filename.endswith('.png') or filename.endswith('.jpg'):
            img = Image.open(os.path.join(folder, filename)).convert('RGB')
            images.append(np.array(img))
    return images

def calculate_difference(slice1, slice2):
    # Calculate the sum of squared differences between the right edge of slice1 and the left edge of slice2
    return np.sum((slice1[:, -1] - slice2[:, 0]) ** 2)

def find_best_match(slices):
    n = len(slices)
    matched_slices = [slices[0]]
    slices.pop(0)

    while slices:
        last_slice = matched_slices[-1]
        differences = [calculate_difference(last_slice, s) for s in slices]
        best_match_index = np.argmin(differences)
        matched_slices.append(slices.pop(best_match_index))

    return matched_slices

def save_image(images, output_path):
    heights, widths, _ = zip(*(i.shape for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_image = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        pil_img = Image.fromarray(img)
        new_image.paste(pil_img, (x_offset, 0))
        x_offset += pil_img.width

    new_image.save(output_path)

def main():
    input_folder = './slices'
    output_path = './assembled_image.png'

    slices = load_images(input_folder)
    matched_slices = find_best_match(slices)
    save_image(matched_slices, output_path)

if __name__ == '__main__':
    main()