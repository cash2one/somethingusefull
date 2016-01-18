# capture image from video
from cv2 import VideoCapture, imwrite

def main():
    cap = VideoCapture('feng.mp4')
    ret, frame = cap.read()
    imwrite("feng1.jpg", frame)

if __name__ == '__main__':
    main()
        
