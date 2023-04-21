from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import mediapipe as mp
from kivy.uix.camera import Camera
import numpy as np

mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
mp_holistic = mp.solutions.holistic



class CamApp(App):

    def build(self):

        self.holistic = mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.img1 = Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)
        # opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        return layout

    def update(self, dt):
        cap = self.capture
        holistic = self.holistic
        ret, image = cap.read()
        # pass by reference.

        image.flags.writeable = False
        # Draw landmark annotation on the image.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        results = holistic.process(image)
        print(results)

        buf1 = cv2.flip(image, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1


if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows
