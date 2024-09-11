#ifndef VIDEOFILE_HPP
#define VIDEOFILE_HPP

#include <opencv2/opencv.hpp>

class VideoFile {
public:
    VideoFile(std::string file_name);
    void end_playback();
    bool is_opened();
    int display_frame(cv::Mat* frame);
    int wait_key(int inter_frame_delay);
    int get_cur_frame();
    int get_framerate();
    void scrub(int val);
private:
    cv::VideoCapture* handle;
    int framerate;
    int width;
    int height;
    int num_frames;
    int cur_frame;
};

#endif