# LikelihoodRatio_ML

## Introduction

## Results

## Future work

### Centered bounding boxes
In order to improve the model, we need to have more bounding boxes in locations other than the center of the image. To do this, we could obtain the RA/Dec coordinates of the bounding box and create subimages containing the bounding box, but have it moved off center in the subimages. This would likely help to remove the bias in the model to place boxes primarily in the center of the image, leading to better results.

### Box selection
Use IR components to produce training data

### Other box definition
$(X center,Y center, width, height)$
