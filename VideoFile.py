import cv2
from utils import floatsec_to_minsecms

class VideoFile():
    def __init__(self, file_name):
        self.handle = cv2.VideoCapture(file_name)
        self.framerate = int(self.handle.get(cv2.CAP_PROP_FPS))
        self.width = int(self.handle.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.handle.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.num_frames = int(self.handle.get(cv2.CAP_PROP_FRAME_COUNT))
        self.cur_frame = 0

    def display_frame(self):
        ret, frame = self.handle.read()
        cv2.putText(frame, f"Frame: {self.cur_frame}", (int(self.height/2)-200, self.height-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Elapsed Time (s): {floatsec_to_minsecms(self.cur_frame/self.framerate)}", (int(self.width/2+100), self.height-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Video', frame)
        self.cur_frame += 1
        return ret
    
    def scrub(self, val):
        if self.cur_frame + val < 0 or self.cur_frame > self.num_frames:
            print(f'Tried to skip to frame {self.cur_frame} range is [0, {self.num_frames}]!')
        self.cur_frame += val
        self.handle.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame)

    def wait_key(self, inter_frame_delay):
        return cv2.waitKey(int(1000/self.framerate) + inter_frame_delay) & 0xFF

    def end_playback(self):
        self.handle.release()
        cv2.destroyAllWindows()