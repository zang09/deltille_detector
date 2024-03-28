# Deltille detector
This is a spin-off version of Deltille detector (https://github.com/facebookincubator/deltille), which was published once and almost archieved with no update. In this repo, we've fixed several issues that had been blocking the wide use of the Deltille detector, such as missing script for target generation, mismatched feature indices between definition and detection, opencv compile issue, etc. 

## Target generation
We hope the python scripts added in `scripts` folder are useful for the generation of a pattern PDF and a target description (DSC) file. An example command to generate some patterns for an icosahedron calibration object is:
```
$ python3 ./scripts/generate_pattern.py --design ico_deltille ico_deltille.pdf
```
The idea is to have a dedicated "design" script in `scripts/designs` folder for each new target design.
Please refer to the examples in the folder and make your own patterns for your purpose.

## Dependencies
```
Boost 1.63+
OpenCV 4.0+ 
```

## How to compile
```
$ mkdir build
$ cd build
$ cmake .. -DCMAKE_BUILD_TYPE=Release
$ make
```

## How to run
```
$ ./deltille_detector -t /path/to/<pattern>.dsc -f /path/to/your/image/*.png -o /output/path -s
```

## License
Deltille detector code is licensed under the LGPL v2.1 license. For more
information, please see COPYING file.

## Citation
If you find this work useful, please cite the related paper:
```
@InProceedings{Ha_2017_ICCV,
author = {Ha, Hyowon and Perdoch, Michal and Alismail, Hatem and So Kweon, In and Sheikh, Yaser},
title = {Deltille Grids for Geometric Camera Calibration},
booktitle = {The IEEE International Conference on Computer Vision (ICCV)},
month = {Oct},
pages = {5344--5352},
year = {2017}}
```
