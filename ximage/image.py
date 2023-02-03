import os.path

import cv2
import numpy as np

from PIL import Image
from PIL import ImageChops

from pathlib import Path
from typing import Type, Any, Callable, Union, List, Optional


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)


def draw_bbox_segmentation_on_image(path: Union[Path, str], category_name: str,
                                    bbox: list = None, segmentation: list = None,
                                    color: tuple = (225, 255, 255), thickness: int = 1, font_scale: int = 1):
    """
    :param path:
    :param category_name:
    :param bbox: top left point and bottom right point
    :param segmentation:
    :param color:
    :param thickness:
    :param font_scale:
    :return:
    """
    cv_img = cv2.imread(str(path))
    height, width, channel = cv_img.shape

    if bbox is not None:
        cv_img = cv2.rectangle(cv_img, (round(bbox[0]), round(bbox[1])), (round(bbox[2]), round(bbox[3])), color, thickness)
        cv_img = cv2.putText(cv_img, category_name, (round(bbox[0]), round(bbox[1])+12), cv2.FONT_HERSHEY_PLAIN, font_scale, color, thickness)
        cv2.imwrite(str(path), cv_img)

    if segmentation is not None:
        cv_img = cv2.polylines(cv_img, np.array([segmentation[0]]), True, color, thickness)
        cv_img = cv2.putText(cv_img, category_name, (round(bbox[0]), round(bbox[1])), cv2.FONT_HERSHEY_PLAIN, font_scale, color, thickness)
        cv2.imwrite(str(path), cv_img)

    return width, height, channel


def images_identical(image_path_1, image_path_2):
    image_1_size, image_2_size = os.path.getsize(image_path_1), os.path.getsize(image_path_2)
    if image_1_size != image_2_size:
        return False

    image_1 = Image.open(image_path_1)
    image_2 = Image.open(image_path_2)
    if image_1.size != image_2.size:
        return False

    d = ImageChops.difference(image_1, image_2)
    if d.getbbox() is None:
        return True
    else:
        return False


def get_image_shape(img_path):
    img = cv2.imread(str(img_path))
    height, width, channel = img.shape
    return width, height, channel


def get_cv_image(img_path):
    return cv2.imread(str(img_path))


def _generate_labels(annotation_list: list, w_multiple: float, h_multiple: float, top: int = 0, left: int = 0) -> list:
    labels = list()

    for annotation in annotation_list:
        cat_id = int(annotation[0])
        x_l = round(annotation[2][0] * w_multiple) + left
        y_t = round(annotation[2][1] * h_multiple) + top
        x_r = round(annotation[2][2] * w_multiple) + left
        y_b = round(annotation[2][3] * h_multiple) + top

        labels.append([cat_id, x_l, y_t, x_r, y_b])

    return labels


def _generate_image_info(orig_width, orig_height,
                         final_width, final_height,
                         rsz_width, rsz_height,
                         rsz_padding_top, rsz_padding_bottom,
                         rsz_padding_left, rsz_padding_right) -> dict:
    image_info = dict()
    image_info["orig_width"] = orig_width
    image_info["orig_height"] = orig_height
    image_info["final_width"] = final_width
    image_info["final_height"] = final_height
    image_info["rsz_width"] = rsz_width
    image_info["rsz_height"] = rsz_height
    image_info["rsz_padding_top"] = rsz_padding_top
    image_info["rsz_padding_bottom"] = rsz_padding_bottom
    image_info["rsz_padding_left"] = rsz_padding_left
    image_info["rsz_padding_right"] = rsz_padding_right

    return image_info


def simple_resize_image(img_path, output_image_size: tuple = (640, 640), annotation_list: list = None,
                        interpolation=cv2.INTER_AREA):
    img = get_cv_image(img_path)
    orig_height, orig_width, _ = img.shape
    w_multiple, h_multiple = float(output_image_size[0] / orig_width), float(output_image_size[1] / orig_height)

    rsz_img = cv2.resize(img, output_image_size, interpolation=interpolation)

    labels = _generate_labels(annotation_list, w_multiple, h_multiple)

    image_info = _generate_image_info(
        orig_width, orig_height,
        output_image_size[0], output_image_size[1],
        output_image_size[0], output_image_size[1],
        0, 0, 0, 0)

    return rsz_img, labels, image_info


def adaptive_resize_image(img_path, output_image_size: tuple = (640, 640),
                          padding_color: tuple = BLACK, annotation_list: list = None,
                          interpolation=cv2.INTER_AREA):
    img = get_cv_image(img_path)
    orig_height, orig_width, _ = img.shape

    w_multiple, h_multiple = float(output_image_size[0] / orig_width), float(output_image_size[1] / orig_height)
    if w_multiple < h_multiple:
        rsz_width, rsz_height = output_image_size[0], round(orig_height * w_multiple)
    elif w_multiple == h_multiple:
        rsz_width, rsz_height = output_image_size[0], output_image_size[1]
    else:
        rsz_width, rsz_height = round(w * h_multiple), output_image_size[1]

    rsz_img = cv2.resize(img, (rsz_width, rsz_height), interpolation=interpolation)

    delta_w = output_image_size[0] - rsz_width
    delta_h = output_image_size[1] - rsz_height
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    labels = _generate_labels(annotation_list, w_multiple, h_multiple, top, left)

    image_info = _generate_image_info(
        orig_width, orig_height,
        output_image_size[0], output_image_size[1],
        rsz_width, rsz_height,
        top, bottom, left, right
    )

    return cv2.copyMakeBorder(rsz_img, top, bottom, left, right, cv2.BORDER_CONSTANT,
                              value=padding_color), \
           labels, image_info





