from django.core.management import BaseCommand
import argparse
import cv2
import os
import random
import detector.views as views


class Command(BaseCommand):
    help = 'Take video and classes to be detected as input and outputs classes from video, ' \
           'please enter Q to quit the program'

    def add_arguments(self, parser):
        '''
         path needs to be path to the file
         example --path=/Users/Desktop/input_video.mp4

        '''
        parser.add_argument('--path', type=argparse.FileType())

    def handle(self, *args, **kwargs):
        try:
            path = kwargs.get('path')
            # read the default classes for the yolo model
            pwd = os.path.dirname(__file__)
            with open(pwd + '/coco_names.txt', 'r') as f:
                classes = [w.strip() for w in f.readlines()]

            print("Default classes: \n")
            for n, cls in enumerate(classes):
                print("%d. %s" % (n + 1, cls))

            # select specific classes that you want to detect out of the 80 and assign a color to each detection
            print("enter the comma seperated classes from the default classes")
            user_class = input()
            colours = [(0, 255, 255), (0, 0, 0)]
            selected = {"person": (0, 255, 255),
                        "laptop": (0, 0, 0)}

            if user_class:
                selected_classes = user_class.split(',')
                selected = {key: random.choice(colours) for key in selected_classes}

            # initialize the detector with the paths to cfg, weights, and the list of classes
            detector = views.YoloDetector(os.path.dirname(__file__) + '/yolov3-tiny.cfg',
                                          os.path.dirname(__file__) + '/yolov3-tiny.weights', classes)
            # initialize video stream
            if path:
                cap = cv2.VideoCapture(path.name)
            else:
                cap = cv2.VideoCapture(os.path.dirname(__file__) + '/input_video.mp4')

            # read first frame
            ret, frame = cap.read()
            # loop to read frames and update window
            while ret:
                # this returns detections in the format {cls_1:[(top_left_x, top_left_y, top_right_x, top_right_y), ..],
                #                                        cls_4:[], ..}
                # Note: you can change the file as per your requirement if necessary
                detections = detector.detect(frame)
                # loop over the selected items and check if it exists in the detected items, if it exists loop over all the items of the specific class
                # and draw rectangles and put a label in the defined color
                for cls, color in selected.items():
                    if cls in detections:
                        for box in detections[cls]:
                            x1, y1, x2, y2 = box
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=1)
                            cv2.putText(frame, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
                # display the detections
                cv2.imshow("detections", frame)
                # wait for key press
                key_press = cv2.waitKey(1) & 0xff
                # exit loop if q or on reaching EOF
                if key_press == ord('q'):
                    break
                ret, frame = cap.read()
            # release resources
            cap.release()
            # destroy window
            cv2.destroyAllWindows()
        except Exception as e:
            print(e.args[0])
