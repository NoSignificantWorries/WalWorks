import sys
from pathlib import Path

import streamlit as st
import cv2


def pth(path: str) -> Path:
    path_obj = Path(path).expanduser().absolute()

    if not path_obj.exists():
        raise FileNotFoundError(f"Not found file '{path_obj}'")
    return path_obj


def main():
    img_path = pth("~/.wallpaper")

    image_bgr = cv2.imread(str(img_path))
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    st.title("WalWorks")
    st.image(image_rgb, caption="Image", use_container_width=True)


if __name__ == "__main__":
    try:
        main()
    except BaseException as err:
        print(f"Error while running app: {err}")
        sys.exit(1)

