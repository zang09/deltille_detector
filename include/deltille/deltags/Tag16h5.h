/** DelTag family with 34 distinct codes.
    bits: 16,  minimum hamming: 5,  minimum complexity: 0.5
    seed: 7953

    Max bits corrected       False positive rate
                0                       0.0518799%%
                1                       0.881958%%
                2                       7.10754%%

    Generation time: 0.117997 s

    Hamming distance between pairs of codes (accounting for rotation):

    0000  0
    0001  0
    0002  0
    0003  0
    0004  0
    0005  120
    0006  196
    0007  133
    0008  73
    0009  32
    0010  7
    0011  0
    0012  0
    0013  0
    0014  0
    0015  0
    0016  0
**/

#pragma once

namespace Deltille {

const unsigned long long delTag16h5[] = {
    0x24d6LL, 0x2a9bLL, 0x3625LL, 0x3beaLL, 0x41afLL, 0x4d39LL, 0x58c3LL, 0x5e88LL, 0x644dLL,
    0x86ebLL, 0xa989LL, 0xbad8LL, 0xd7b1LL, 0xeec5LL, 0x1cedLL, 0x8a8cLL, 0xca03LL, 0xf266LL,
    0x74f5LL, 0x1c46LL, 0x2d95LL, 0x4a6eLL, 0x25acLL, 0x7b90LL, 0x796cLL, 0x6628LL, 0x974aLL,
    0x6433LL, 0x8f76LL, 0xf46bLL, 0xe6bdLL, 0xb491LL, 0x8c5dLL, 0x1d8bLL};

static const TagCodes delTagCodes16h5 =
    TagCodes("delTag16h5", 16, 5, delTag16h5, sizeof(delTag16h5) / sizeof(delTag16h5[0]));

} // namespace Deltille
