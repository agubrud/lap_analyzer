import numpy as np
from VideoFile import VideoFile
from utils import floatsec_to_minsecms

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

        self.video.end_playback()

    def summarize(self):
        print(f"Fastest Lap: {floatsec_to_minsecms(np.min(self.timing['laps']))}")