#ifndef SESSION_HPP
#define SESSION_HPP
#include "VideoFile.hpp"

class Session {
public:
    // Public members (accessible from outside the class)
    Session(boost::property_tree::ptree pt);
    char user_input();
    int process_video();
    void summarize();

private:
    // Private members (accessible only from within the class)
    //void privateMemberFunction();
    std::string desc;
    std::string file_name;
    int framerate = 25;
    int inter_frame_delay = 0;
    std::vector<int> lap_times;
    std::vector<int> event_times;
    VideoFile* video;
};

#endif