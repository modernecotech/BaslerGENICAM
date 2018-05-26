// Grab.cpp
/*
    
    This sample illustrates how to grab and process images using the CInstantCamera class.

    Images are first grabbed and displayed freerolling, and when a button is pressed on the keyboard 10 images are saved into PNG format and the program exits.

==hayder aziz, 19th feb 2016
*/

//for usleep command
#include <stdlib.h>
#include <unistd.h>
#include <iostream>
// Include files to use the PYLON API.
#include <pylon/PylonIncludes.h>
#include "../include/SampleImageCreator.h"

//include files for opencv3.1
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/core/core.hpp"


//opencv namespace
using namespace cv;

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;

int main(int argc, char* argv[])
{
    // The exit code of the sample application.
    int exitCode = 0;
    //image constants for the 5MP sensor. this is for preview image
      const uint32_t Width = 1944;
      const uint32_t Height = 2592;

    // Before using any pylon methods, the pylon runtime must be initialized. 
    PylonInitialize();
    // This smart pointer will receive the grab result data.
    CGrabResultPtr ptrGrabResult;

    try
    {
        // Create an instant camera object with the camera device found first.
        CInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice());

	// this opencv image is an 16 bit unsigned single channel
//for mono sensor use below
//	Mat cv_img(Width, Height, CV_8UC1);
//for colour sensor use below
	Mat cv_img(Width, Height, CV_8UC3);

        // The parameter MaxNumBuffer can be used to control the count of buffers
        // allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer = 9;

        // Start the grabbing of c_countOfImagesToGrab images.
        // The camera device is parameterized with a default configuration which
        // sets up free-running continuous acquisition.
        camera.StartGrabbing();
        CPylonImage image;

	//setup the pylon imageconverter
	CImageFormatConverter fc;
//for colour sensor use below
        fc.OutputPixelFormat = PixelType_RGB8packed;
//for mono sensor use below
//        fc.OutputPixelFormat = PixelType_Mono8;

        while ( camera.IsGrabbing())
        {
            // Wait for an image and then retrieve it. A timeout of x ms is used.
            camera.RetrieveResult( 1000, ptrGrabResult, TimeoutHandling_ThrowException);
            // Image grabbed successfully?
            if (ptrGrabResult->GrabSucceeded())
            {
	    // opencv convert the grabbed image and display it
	     fc.Convert(image, ptrGrabResult);  
//for mono camera use below
//	     cv_img = cv::Mat(Width, Height, CV_8UC1,(uint8_t*)image.GetBuffer());
//for colour camera use below
	     cv_img = cv::Mat(Width, Height, CV_8UC3,(uint8_t*)image.GetBuffer());
//	     cv_img = cv::Mat(Width, Height, CV_8UC3);
//	     memcpy(cv_img.ptr(),image.GetBuffer(),2592*1944);
	     resize(cv_img, cv_img, Size(cv_img.cols/3, cv_img.rows/3));
//             namedWindow("OICO Cam", WINDOW_OPENGL);
             imshow("OICO Cam",cv_img);
//	     waitKey(1);
		if (waitKey(27)>=32){
		//command for pexpect in linux to switch on white LED
	         cout << "XXXXXX"  << endl;
		//when image pressed save the image to PNG and exit
                CImagePersistence::Save( ImageFileFormat_Png, "1.png", ptrGrabResult);
		destroyAllWindows();
		while ( camera.IsGrabbing())
		{
		camera.RetrieveResult( 1000, ptrGrabResult, TimeoutHandling_ThrowException);
		 if (ptrGrabResult->GrabSucceeded())
		{
		CImagePersistence::Save( ImageFileFormat_Png, "2.png", ptrGrabResult);
		while ( camera.IsGrabbing())
		{
		camera.RetrieveResult( 1000, ptrGrabResult, TimeoutHandling_ThrowException);
		 if (ptrGrabResult->GrabSucceeded())
		{
		CImagePersistence::Save( ImageFileFormat_Png, "3.png", ptrGrabResult);
		while ( camera.IsGrabbing())
		{
		camera.RetrieveResult( 1000, ptrGrabResult, TimeoutHandling_ThrowException);
		 if (ptrGrabResult->GrabSucceeded())
		{
		CImagePersistence::Save( ImageFileFormat_Png, "4.png", ptrGrabResult);
                camera.StopGrabbing();
		}
		}
		}
		}
		}
		}
		}
           }

	}
	}
            catch (const GenericException &e)
            {

                cerr << "Could not grab an image: " << endl
                    << e.GetDescription() << endl;
            }


    // Releases all pylon resources. 
    PylonTerminate();  

    return exitCode;
}
