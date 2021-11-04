#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>

#include "tmp/HLS_svm_param_rbf_accum_d.h"
#include "tmp/HLS_normalize_param_accum_d.h"

void preprocessing(
    int *sample,
    float *feature
)
{
    feature[0] = (sample[0] - ins_min.float_param[0]) / (ins_max.float_param[0] - ins_min.float_param[0]);
    feature[1] = (sample[1] - cycle_min.float_param[0]) / (cycle_max.float_param[0] - cycle_min.float_param[0]);
    feature[2] = (sample[2] - memory_min.float_param[0]) / (memory_max.float_param[0] - memory_min.float_param[0]);
    feature[3] = (sample[3] - branchm_min.float_param[0]) / (branchm_max.float_param[0] - branchm_min.float_param[0]);
}

//--------------------------------------------------------------------
// prediction by using gaussian rbf kernel
//--------------------------------------------------------------------
void prediction(
    float *feature,
    int *pred
)
{
    int i, j;
    float y = 0;
    float diff = 0;

    for (i = 0; i < support_vectors_shape[0]; i++){
        float sum = 0;
        for (j = 0; j < support_vectors_shape[1]; j++){ // rbf kernel
            diff = support_vectors.float_param[support_vectors_shape[1]*i+j] - feature[j];
            sum += diff*diff;
        }
        y += dual_coef.float_param[i]*std::exp(-rbf_gamma.float_param[0]*sum);
    }
    y += bias.float_param[0];
    *pred = (y >= 0) ? 1 : -1;
}