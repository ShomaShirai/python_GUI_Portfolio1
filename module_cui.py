import csv
import os

import cv2
import numpy as np

import config


def blur_area(src, x, y, width, height, blur_intensity):
    dst = src.copy()
    small = cv2.resize(
        src[y : y + height, x : x + width],
        None,
        fx=blur_intensity,
        fy=blur_intensity,
        interpolation=cv2.INTER_NEAREST,
    )
    dst[y : y + height, x : x + width] = cv2.resize(
        small, (width, height), interpolation=cv2.INTER_NEAREST
    )
    return dst


def load_face_detector(directory, model_file="face_detection_yunet_2023mar.onnx"):
    weights = os.path.join(directory, model_file)
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
    return face_detector


def create_csv(directory, filename="face_detection_output.csv"):
    file = open(os.path.join(directory, filename), "w", newline="")
    header = [
        "X座標",
        "Y座標",
        "幅",
        "高さ",
        "右目X座標",
        "右目Y座標",
        "左目X座標",
        "左目Y座標",
        "鼻X座標",
        "鼻Y座標",
        "右口角X座標",
        "右口角Y座標",
        "左口角X座標",
        "左口角Y座標",
        "信頼度",
    ]
    writer = csv.writer(file)
    writer.writerow(header)
    return writer, file


def draw_landmarks(image, face, color=(0, 0, 255), thickness=2):
    box = list(map(int, face[:4]))  # バウンディングボックス
    cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

    landmarks = list(map(int, face[4 : len(face) - 1]))  # ランドマーク
    landmarks = np.array_split(landmarks, len(landmarks) / 2)
    for landmark in landmarks:
        cv2.circle(image, landmark, 5, color, -1, cv2.LINE_AA)

    confidence = face[-1]  # 信頼度
    confidence_str = "{:.2f}".format(confidence)
    position = (box[0], box[1] - 10)
    cv2.putText(
        image,
        confidence_str,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        2,
        cv2.LINE_AA,
    )

    return box, landmarks, confidence_str


def write_to_csv(writer, box, landmarks_flattened, confidence_str):
    row = box + landmarks_flattened + [confidence_str]
    writer.writerow(row)


def sunburn_area(image, box, sunburn_intensity):
    face_roi = image.copy()
    cv2.imwrite("output.png", face_roi)
    x, y, w, h = box
    face_roi = image[y : y + h, x : x + w].copy()

    face_roi_hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
    face_roi_hsv[:, :, 1] = np.clip(
        face_roi_hsv[:, :, 1] * sunburn_intensity, 0, 255
    )  # 彩度の調整
    face_roi_tanned = cv2.cvtColor(face_roi_hsv, cv2.COLOR_HSV2BGR)  # BGRに戻す

    image[y : y + h, x : x + w] = face_roi_tanned

    return image


def apply_grabcut(image, box):
    grabcut_image = image.copy()

    mask = np.zeros(grabcut_image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    rect = config.NAGATOMO_RECT  # 顔の領域を矩形として指定
    cv2.grabCut(grabcut_image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # 0, 2 は背景領域、1, 3 は前景領域
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")

    # 前景領域だけを保持し、背景は除去
    grabcut_image = grabcut_image * mask2[:, :, np.newaxis]

    return grabcut_image


def process_image(
    face_detector,
    image,
    writer,
    is_blur_face,
    is_write_csv,
    is_sunburn,
    is_grabcut,
    blur_intensity=0,
    sunburn_intensity=0,
):
    height, width, _ = image.shape
    face_detector.setInputSize((width, height))
    _, faces = face_detector.detect(image)
    faces = faces if faces is not None else []
    blur_image = image.copy()
    sunburn_image = image.copy()
    grabcut_image = image.copy()

    for face in faces:
        try:
            box, landmarks, confidence_str = draw_landmarks(image, face)
            landmarks_flattened = [
                coord for landmark in landmarks for coord in landmark
            ]

            if is_write_csv:
                write_to_csv(writer, box, landmarks_flattened, confidence_str)
            if is_blur_face:
                blur_image = blur_area(
                    blur_image, box[0], box[1], box[2], box[3], blur_intensity
                )
            if is_sunburn:
                sunburn_image = sunburn_area(sunburn_image, box, sunburn_intensity)
            if is_grabcut:
                grabcut_image = apply_grabcut(grabcut_image, box)

        except Exception as e:
            print(f"Error processing face landmarks: {e}")

    if is_blur_face:
        return blur_image
    elif is_sunburn:
        return sunburn_image
    elif is_grabcut:
        return grabcut_image
    else:
        return image


def change_face(face_detector, img1, img2):
    """顔の入れ替え処理"""

    def extract_face(image):
        height, width = image.shape[:2]
        face_detector.setInputSize((width, height))
        _, faces = face_detector.detect(image)
        return (
            list(map(int, faces[0][:4]))
            if faces is not None and len(faces) > 0
            else None
        )

    def paste_face(target_image, face, box):
        x, y, w, h = box
        face_resized = cv2.resize(face, (w, h))
        target_image[y : y + h, x : x + w] = face_resized

    box1 = extract_face(img1)
    box2 = extract_face(img2)

    if box1 is None or box2 is None:
        raise ValueError("Failed to detect face in one or both images")

    face1 = img1[box1[1] : box1[1] + box1[3], box1[0] : box1[0] + box1[2]]
    face2 = img2[box2[1] : box2[1] + box2[3], box2[0] : box2[0] + box2[2]]

    swapped_img1 = img1.copy()
    swapped_img2 = img2.copy()

    paste_face(swapped_img1, face2, box1)
    paste_face(swapped_img2, face1, box2)

    return swapped_img1, swapped_img2
