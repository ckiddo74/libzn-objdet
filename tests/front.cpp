#include <zn.hpp>
/*
#include <opencv2/opencv.hpp>
#include <iostream>
#include <stdio.h>
#include <chrono>
#include <thread>
#include <zmq.hpp>
#include <zmq_addon.hpp>
#include <vector>
#include <string>
#include <stdint.h>
#include <stdlib.h>
*/

using namespace std;
using namespace cv;

int main(int argc, char** argv)
{

    VideoCapture cap;
    //cap.open(0);
    cap.open("/workspace/assets/male.mp4");

    if (!cap.isOpened())
    {
        printf("--(!)Error opening video capture\n");
        return -3;
    }

    Mat image;
    namedWindow("Image", CV_WINDOW_AUTOSIZE);

    zmq::context_t context{1};

    int major, minor, patch;
    zmq_version(&major, &minor, &patch);
    printf("Installed ZeroMQ version: %d.%d.%d\n", major, minor, patch);

    zmq::socket_t socket{context, zmq::socket_type::req};
    socket.connect("tcp://localhost:5555");

    cv::Mat result;
    long long int sum = 0;
    long long int n = 0;
    while (1)
    {

        if (!cap.read(image)) {
            break;
        }

        auto start = std::chrono::steady_clock::now();

        zn::send_image(socket, image);
        zn::receive_image(socket, result);

        auto end = std::chrono::steady_clock::now();

        auto elapsed =  static_cast<long long int>(std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count());
        sum += elapsed;
        n += 1;

        printf("FPS=%.2f\n", ((double) n*1000/((double) sum)));


        //printf("FPS=%.2f\n", ((double) 1.0/(double) (((double) sum/(double) n)*1000.0)));



        imshow("Image", result);
        auto k=waitKey(1);
        if (k != -1) {
            return 0;
        }



    }







#if 0
    VideoCapture cap;
    //cap.open(0);
    cap.open("male.mp4");

    if (!cap.isOpened())
    {
        printf("--(!)Error opening video capture\n");
        return -3;
    }


    Mat image;
    namedWindow("Image", CV_WINDOW_AUTOSIZE);

    zmq::context_t context (1);
    zmq::socket_t socket (context, ZMQ_REQ);

    socket.connect ("tcp://127.0.0.1:5555");

    long long int sum = 0;
    long long int n = 0;
    while (1)
    {
        cap.read(image);

        auto start = std::chrono::steady_clock::now();

        send_image(socket, image);

        auto end = std::chrono::steady_clock::now();

        /*
        imshow("Image", image);
        auto k=waitKey(1);
        */

        auto elapsed =  static_cast<long long int>(std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count());
        sum += elapsed;
        n += 1;

        printf("FPS=%.2f\n", ((double) 1/(double) (sum/n)*1000));

        //if (k == 113 ) break; // 'q'

    }

#endif

    printf("sucessfully completed!\n");


    return 0;
}

