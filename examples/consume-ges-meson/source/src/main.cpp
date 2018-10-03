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
        std::cout << "FAILURE loading the 'alpha' element from gst-plugins-good" << std::endl;
    }
    else
    {
        std::cout << "SUCCESS loading the 'alpha' element from gst-plugins-good" << std::endl;
    }

    // Here we load an element from gst-plugins-bad (hlssink)
    GstElement* hlssink = gst_element_factory_make("hlssink", "hlssink0");
    if (nullptr == hlssink)
    {
        std::cout << "FAILURE loading the 'hlssink' element from gst-plugins-bad" << std::endl;
    }
    else
    {
        std::cout << "SUCCESS loading the 'hlssink' element from gst-plugins-bad" << std::endl;
    }

    // Here we load an element from gst-plugins-ugly (hlssink)
    GstElement* asfdemux = gst_element_factory_make("asfdemux", "asfdemux0");
    if (nullptr == asfdemux)
    {
        std::cout << "FAILURE loading the 'asfdemux' element from gst-plugins-ugly" << std::endl;
    }
    else
    {
        std::cout << "SUCCESS loading the 'asfdemux' element from gst-plugins-ugly" << std::endl;
    }

    // Here we load an element from gst-libav (avdec_aac)
    GstElement* avdec_aac = gst_element_factory_make("avdec_aac", "avdec_aac0");
    if (nullptr == avdec_aac)
    {
        std::cout << "FAILURE loading the 'avdec_aac' element from gst-libav" << std::endl;
    }
    else
    {
        std::cout << "SUCCESS loading the 'avdec_aac' element from gst-libav" << std::endl;
    }

    std::cout << "DONE" << std::endl;
};