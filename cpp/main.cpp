#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <iostream>
#include "VideoFile.hpp"
#include "Session.hpp"

int main() {
    boost::property_tree::ptree pt;

    boost::property_tree::read_json("config.json", pt); // Assuming you're reading a JSON file

    Session* s = new Session(pt);

    s->process_video();
    s->summarize();

    return 0;
}