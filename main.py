import argparse
import cv2
import numpy as np
from utils import floatsec_to_minsecms, load_config

class VideoFile():
    def __init__(self, cfg):
        self.file_name = cfg['inputs'][0]['file_name']
        self.handle = cv2.VideoCapture(self.file_name)
        self.framerate = int(self.handle.get(cv2.CAP_PROP_FPS))
        self.width = int(self.handle.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.handle.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def display_frame(self, frame, frame_count):
        cv2.putText(frame, f"Frame: {frame_count}", (int(self.height/2)-200, self.height-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Elapsed Time (s): {frame_count/self.framerate}", (int(self.width/2+100), self.height-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Video', frame)

    def process(self):
        frame_count = 0
        delay = 0
        lap_events = []
        laps = []
        while self.handle.isOpened():
            ret, frame = self.handle.read()
            if not ret:
                break
            self.display_frame(frame, frame_count)
            frame_count += 1

            key = cv2.waitKey(int(1000/self.framerate) + delay) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('a'):
                frame_count -= 100
                frame_count = max(0, frame_count)
                self.handle.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
            elif key == ord('d'):
                frame_count += 100
                self.handle.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
            elif key == ord('w'):
                delay += 500
            elif key == ord('s'):
                delay = 0
            elif key == ord(' '):
                lap_events.append(float(frame_count)/float(self.framerate))
                if len(lap_events) >= 2:
                    laps.append(lap_events[-1]-lap_events[-2])
                    print(f'Lap {len(lap_events)-1}: {floatsec_to_minsecms(laps[-1])}')
            elif key == ord('f'):
                frame_count += int(np.average(laps)*self.framerate * 0.95)
                self.handle.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

        print(f'Fastest Lap: {floatsec_to_minsecms(np.min(laps))}')
        self.handle.release()
        cv2.destroyAllWindows()

def main():
    cfg = load_config(args.config)
    v = VideoFile(cfg)
    v.process()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=False, help="Configuration YAML file", dest="config", default='cfg.yml')
    args = parser.parse_args()
    main()