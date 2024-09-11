#include <iostream>
#include <numeric>
#include <math.h>
#include "VideoFile.hpp"

VideoFile::VideoFile(std::string file_name)
{
    this->handle = new cv::VideoCapture(file_name);
    this->cur_frame = 0;
    this->framerate = (int) this->handle->get(cv::CAP_PROP_FPS);
    this->width = (int) this->handle->get(cv::CAP_PROP_FRAME_WIDTH);
    this->height = (int) this->handle->get(cv::CAP_PROP_FRAME_HEIGHT);
    this->num_frames = (int) this->handle->get(cv::CAP_PROP_FRAME_COUNT);
}
void VideoFile::end_playback(){
    this->handle->release();
    cv::destroyAllWindows();
}
bool VideoFile::is_opened(){
    return this->handle->isOpened();
}
int VideoFile::display_frame(cv::Mat* frame){
    int ret = 0;
    bool can_grab = this->handle->grab();
    if (can_grab){
        this->handle->retrieve(*frame);
    }
    this->cur_frame += 1;

    if (frame->empty()) {
        ret = -1;
    }
    
    putText(*frame, std::to_string(this->cur_frame), cv::Point(100, 200), cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(0, 0, 0), 2);

    imshow("Video Player", *frame);
    return ret;
}
int VideoFile::wait_key(int inter_frame_delay){
    return cv::waitKey(int(1000/this->framerate) + inter_frame_delay);
}
int VideoFile::get_cur_frame(){
    return this->cur_frame;
}
int VideoFile::get_framerate(){
    return this->framerate;
}
void VideoFile::scrub(int val){
    if (this->cur_frame + val < 0 || this->cur_frame + val > this->num_frames){
        val = 0;
    }
    this->cur_frame += val;
    this->handle->set(cv::CAP_PROP_POS_FRAMES, this->cur_frame);
}