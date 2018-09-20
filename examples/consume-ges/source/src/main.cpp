#include "consume-ges.h"

#include <iostream>

int main(int nargs, char** args)
{
    // Here we call something from the `gstreamer` package
    gst_init(&nargs, &args);

    // Here we call something from the `gst-editing-services` package
    if (ges_init())
    {
        std::cout << "SUCCESS initializing GES." << std::endl;
    }
    else
    {
        std::cout << "FAILURE initializing GES." << std::endl;
    }

    // Here we load an element from gst-plugins-good (alpha)
    GstElement* alpha = gst_element_factory_make("alpha", "alpha0");
    if (nullptr == alpha)
    {
        std::cout << "FAILURE loading the 'alpha' plugin from gst-plugins-good" << std::endl;
    }
    else
    {
        std::cout << "SUCCESS loading the 'alpha' plugin from gst-plugins-good" << std::endl;
    }

    // Here we load an element from gst-plugins-bad (hlssink)
    GstElement* hlssink = gst_element_factory_make("hlssink", "hlssink0");
    if (nullptr == hlssink)
    {
        std::cout << "FAILURE loading the 'hlssink' plugin from gst-plugins-bad" << std::endl;
    }
    else
    {
        std::cout << "SUCCESS loading the 'hlssink' plugin from gst-plugins-bad" << std::endl;
    }

    // Here we load an element from gst-libav (avdec_aac)
    GstElement* avdec_aac = gst_element_factory_make("avdec_aac", "avdec_aac0");
    if (nullptr == avdec_aac)
    {
        std::cout << "FAILURE loading the 'avdec_aac' plugin from gst-libav" << std::endl;
    }
    else
    {
        std::cout << "SUCCESS loading the 'avdec_aac' plugin from gst-libav" << std::endl;
    }

    std::cout << "DONE" << std::endl;
};