#include "consume-ges.h"

#include <iostream>

int main(int nargs, char** args)
{
    std::cout << "[BEGIN]  Gstreamer initialization" << std::endl;
    // Here we call something from the `gstreamer` package
    gst_init(&nargs, &args);
    std::cout << "[END]    Gstreamer initialization" << std::endl;

    std::cout << "[BEGIN]  GES initialization" << std::endl;
    // Here we call something from the `gst-editing-services` package
    ges_init();
    std::cout << "[END]    GES initialization" << std::endl;

    std::cout << "DONE";
};