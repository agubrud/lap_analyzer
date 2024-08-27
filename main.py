import argparse
import cv2
import numpy as np
from utils import floatsec_to_minsecms, load_config

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

class Session():
    def __init__(self, cfg):
        self.video = VideoFile(cfg['inputs'][0]['file_name'])
        self.inter_frame_delay = 0
        self.timing = {'laps': [], 'events': []}

    def user_input(self):
        key = self.video.wait_key(self.inter_frame_delay)
        if key == ord('q'):
            return False
        elif key == ord('a'):
            self.video.scrub(-100)
        elif key == ord('d'):
            self.video.scrub(100)
        elif key == ord('w'):
            self.inter_frame_delay += 500
        elif key == ord('s'):
            self.inter_frame_delay = 0
        elif key == ord(' '):
            self.timing['events'].append(float(self.video.cur_frame)/float(self.video.framerate))
            if len(self.timing['events']) >= 2:
                self.timing['laps'].append(self.timing['events'][-1]-self.timing['events'][-2])
                print(f"Lap {len(self.timing['events'])-1}: {floatsec_to_minsecms(self.timing['laps'][-1])}")
        elif key == ord('f'):
            if len(self.timing['laps']) > 0:
                self.video.scrub(int(np.average(self.timing['laps'])*self.video.framerate * 0.97))
            else:
                print(f'Not enough laps logged to project the skip length!')

        return True

    def process_video(self):
        while self.video.handle.isOpened():
            ret = self.video.display_frame()
            if not ret:
                break

            ret = self.user_input()
            if not ret:
                break

        print(f"Fastest Lap: {floatsec_to_minsecms(np.min(self.timing['laps']))}")
        self.video.end_playback()

def main():
    cfg = load_config(args.config)
    s = Session(cfg)
    s.process_video()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=False, help="Configuration YAML file", dest="config", default='cfg.yml')
    args = parser.parse_args()
    main()