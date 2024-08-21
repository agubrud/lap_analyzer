import argparse
import yaml
import cv2
import numpy as np

def load_config(cfg):
    with open(cfg, 'r') as f:
        return yaml.safe_load(f)
    
def floatsec_to_minsecms(num):
    minutes = num // 60
    seconds = num % 60
    milliseconds = int((seconds % 1) * 1000)
    return f'{str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}.{milliseconds}'
    
def display_video(video_name):
    cap = cv2.VideoCapture(video_name)
    src_framerate = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = 0
    delay = 0
    lap_events = []
    laps = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.putText(frame, f"Frame: {frame_count}", (int(width/2)-200, height-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.putText(frame, f"Elapsed Time (s): {frame_count/src_framerate}", (int(width/2+100), height-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Video', frame)
        # Display frame number and time on the frame
        frame_count += 1

        key = cv2.waitKey(int(1000/src_framerate) + delay) & 0xFF
        if key == ord('q'):
            print(f'Fastest Lap: {floatsec_to_minsecms(np.min(laps))}')
            break
        elif key == ord('a'):
            frame_count -= 100
            frame_count = max(0, frame_count)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        elif key == ord('d'):
            frame_count += 100
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        elif key == ord('w'):
            delay += 500
        elif key == ord('s'):
            delay = 0
        elif key == ord(' '):
            lap_events.append(float(frame_count)/float(src_framerate))
            if len(lap_events) >= 2:
                laps.append(lap_events[-1]-lap_events[-2])
                print(f'Lap {len(lap_events)-1}: {floatsec_to_minsecms(laps[-1])}')
        elif key == ord('f'):
            frame_count += int(np.average(laps)*src_framerate * 0.95)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)


    cap.release()
    cv2.destroyAllWindows()


def main():
    cfg = load_config(args.config)
    display_video(cfg['inputs'][0]['file_name'])
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=False, help="Configuration YAML file", dest="config", default='cfg.yml')
    args = parser.parse_args()
    main()