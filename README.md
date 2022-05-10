# Deltille detector
This is a spin-off version of Deltille detector (https://github.com/facebookincubator/deltille), which was published once and almost archieved with no update by now. In this repo, we've fixed several issues that had been blocking the use of the Deltille detector, such as missing script for target generation, mismatch in the grid indices between board definition and detection, compile issues, etc. 

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

## Compile
```
$ mkdir build
$ cd build
$ cmake .. -DCMAKE_BIULD_TYPE=Release -G Ninja
$ ninja
```

## How to run
Target generation (e.g. ico_deltille example pattern)
```
$ python3 ./scripts/generate_pattern.py --design ico_deltille ico_deltille.pdf
```

Target detector
```
$ ./deltille_detector -t /path/to/dsc/pattern.dsc -f /path/to/image/*.png -o /path/to/output -s
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
