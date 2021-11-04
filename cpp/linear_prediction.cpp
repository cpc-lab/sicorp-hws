#include <iostream>
#include <stdio.h>
#include <stdlib.h>

#include "tmp/HLS_svm_param_linear_accum_d.h"
#include "tmp/HLS_normalize_param_accum_d.h"

void preprocessing(
    int *sample,
    double *feature
)
{
    feature[0] = (sample[0] - ins_min.double_param[0]) / (ins_max.double_param[0] - ins_min.double_param[0]);
    feature[1] = (sample[1] - cycle_min.double_param[0]) / (cycle_max.double_param[0] - cycle_min.double_param[0]);
    feature[2] = (sample[2] - memory_min.double_param[0]) / (memory_max.double_param[0] - memory_min.double_param[0]);
    feature[3] = (sample[3] - branchm_min.double_param[0]) / (branchm_max.double_param[0] - branchm_min.double_param[0]);
}

void prediction(
    double *feature,
    int *pred
)
{
    double y = 0;
    int t;
    
    for (int i = 0; i < coef_shape[1]; i++){
        y += coef.double_param[i]*feature[i];
    }
    y += bias.double_param[0];
    *pred = (y >= 0) ? 1 : -1;
}