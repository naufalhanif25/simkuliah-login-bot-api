import numpy as np
import cv2
import requests

class Image:
    def __init__(self, image: any = None, url: str = None, code: int = cv2.COLOR_BGR2RGB) -> None:
        self.image = image

        if url is not None:
            self.from_url(url, code)

    def from_url(self, url: str, code: int = cv2.COLOR_BGR2RGB) -> None:
        resp = requests.get(url)
        image_array = np.frombuffer(resp.content, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        self.image = cv2.cvtColor(image, code)

    def apply(self, func: any, *args, **kwargs) -> None:
        self.image = func(self.image, *args, **kwargs)

    def replace(self, image: any) -> None:
        self.image = image

    def shape(self) -> any:
        return self.image.shape[:2]

    def __call__(self) -> any:
        return self.image