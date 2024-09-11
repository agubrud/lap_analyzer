#include <boost/property_tree/ptree.hpp>
#include <numeric>
#include "Session.hpp"

Session::Session(boost::property_tree::ptree pt){
    // Access data from the ptree
    this->desc = pt.get<std::string>("description");
    this->file_name = pt.get<std::string>("file_name");
    this->video = new VideoFile(this->file_name);
}
char Session::user_input(){
    int key = this->video->wait_key(this->inter_frame_delay);
    int event_list_len;
    int lap_list_len;

    switch ((char) key) {
        case 'a':
            std::cout << "scrub back 100 frames" << std::endl;
            this->video->scrub(-100);
            break;
        case 'd':
            std::cout << "scrub forward 100 frames" << std::endl;
            this->video->scrub(100);
            break;
        case 'w':
            std::cout << "slow down framerate" << std::endl;
            this->inter_frame_delay += 500;
            break;
        case 's':
            std::cout << "return framerate to normal" << std::endl;
            this->inter_frame_delay = 0;
            break;
        case ' ':
            std::cout << "log event" << std::endl;
            this->event_times.push_back(this->video->get_cur_frame());
            std::cout << "Event added: " << std::to_string(this->video->get_cur_frame()) << std::endl;
            event_list_len = this->event_times.size();
            
            if (event_list_len > 1) {
                int penult = this->event_times[event_list_len - 2];
                int ult = this->event_times[event_list_len - 1];
                this->lap_times.push_back(ult - penult);
                std::cout << "Lap added: " << std::to_string(ult - penult) << std::endl;
            }
            break;
        case 'f':
            std::cout << "approximate lap scrub" << std::endl;
            lap_list_len = this->lap_times.size();
            if (lap_list_len > 0){
                int sum = std::accumulate(this->lap_times.begin(), this->lap_times.end(), 0);

                // Calculate the average
                int average = (int) static_cast<double>(sum) / lap_list_len;
                
                average = (int) static_cast<double>(average) * 0.95;
                this->video->scrub(average);
            }
            break;
        default:
            // Handle other key presses (if needed)
            break;
    }

    if (key == 'q') {
        return 1;
    }
    return 0;
}
int Session::process_video(){
    if (!this->video->is_opened()) {
        std::cerr << "Error opening video file" << std::endl;
        return -1;
    }

    while (true) {
        cv::Mat frame;
        int ret;
        this->video->display_frame(&frame);

        ret = user_input();
        if (ret == 1){
            break;
        }
    }

    this->video->end_playback();
    return 0;
}
void Session::summarize(){
    int fastest_lap;
    if (this->lap_times.size() == 0){
        return;
    }
    auto it = std::min_element(this->lap_times.begin(), this->lap_times.end());
    fastest_lap = *it;
    float fastest_lap_sec = static_cast<float>(fastest_lap) / static_cast<float>(this->video->get_framerate());

    int minutes = (int) fastest_lap_sec / 60;
    int seconds = (int) fastest_lap_sec % 60;
    int whole_part = static_cast<int>(fastest_lap_sec);
    float milliseconds = (float) fastest_lap_sec - whole_part;

    std::cout << "Fastest lap: ";
    std::cout << std::setw(2) << std::setfill('0') << minutes << ":";
    std::cout << std::setw(2) << std::setfill('0') << seconds << ".";
    std::cout << std::setw(3) << std::setfill('0') << std::round(milliseconds*1000) << std::endl;
}