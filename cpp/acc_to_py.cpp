#include <iostream>
#include <iomanip>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define FEATURE_SHAPE 4
#define OUTPUT_BUFFER_SIZE 500

void preprocessing(
    int *sample,
    double *feature
);

void prediction(
    double *feature,
    int *pred
);

//--------------------------------------------------------------------
// Main Function
//--------------------------------------------------------------------
int main(int argc, char *argv[])
{
    std::string krnl = argv[1]; //linear //rbf
    std::string type = argv[2]; //accum //interval //delta
    std::string mode = argv[3]; //d //s
    std::string size = argv[4]; //10 //20 //30 //40 //50 //60 //70 //80
    std::string benchmark = argv[5]; //a2time //aifftr //aiifft //bitmnp //canrdr //idctrn //pntrch //ttsprk
    std::string num = argv[6]; //81 ~ 100
    std::string testinput = "../data/svm_input/0001/" + benchmark + "01_lite/svm_input_" + type + "_" + num + ".txt";
    const char *testinput_arg = testinput.c_str();

    int i, j;
    FILE *fp;

    int sample[FEATURE_SHAPE];
    double feature[FEATURE_SHAPE];
    int pred[1];
    int all_pred[OUTPUT_BUFFER_SIZE];

	if ((fp = fopen(testinput_arg, "r")) == NULL){
		fprintf(stderr, "CAN'T OPEN input FILE\n");
		exit(-1);
	}

    int buf[4], count;
    count = 0;
    
    while(fscanf(fp, "%d %d %d %d", &buf[0], &buf[1], &buf[2], &buf[3]) != EOF){
        for (j = 0; j < 4; j++){
            sample[j] = (int)buf[j];
        }
        preprocessing(sample, feature);
        prediction(feature, pred);
        count++;

        std::cout << *pred << ",";
    }
    std::cout << std::endl;

	fclose(fp);
}