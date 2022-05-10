/** DelTag family with 47 distinct codes.
    bits: 25,  minimum hamming: 9,  minimum complexity: 0.5
    seed: 204067

    Max bits corrected       False positive rate
                0                       0.000140071%%
                1                       0.00364184%%
                2                       0.0456631%%
                3                       0.367826%%
                4                       2.13972%%

    Generation time: 21.3489 s

    Hamming distance between pairs of codes (accounting for rotation):

    0000  0
    0001  0
    0002  0
    0003  0
    0004  0
    0005  0
    0006  0
    0007  0
    0008  0
    0009  241
    0010  324
    0011  214
    0012  171
    0013  84
    0014  34
    0015  11
    0016  2
    0017  0
    0018  0
    0019  0
    0020  0
    0021  0
    0022  0
    0023  0
    0024  0
    0025  0
**/

#pragma once

namespace Deltille {

const unsigned long long delTag25h9[] = {
    0x09222e8LL, 0x12128adLL, 0x1ec4586LL, 0x07b4b4bLL, 0x19956d5LL, 0x0285c9aLL, 0x1d56de9LL,
    0x06473aeLL, 0x1be964cLL, 0x036c474LL, 0x17a0f75LL, 0x0452c4eLL, 0x1719fb2LL, 0x1b3aeddLL,
    0x1585069LL, 0x0d2c326LL, 0x052253bLL, 0x06c7d43LL, 0x0e82bd6LL, 0x1859975LL, 0x1665215LL,
    0x157840dLL, 0x0ce765fLL, 0x01b39e2LL, 0x144cf6cLL, 0x0c95d3cLL, 0x0b00df3LL, 0x0efa572LL,
    0x1f7b853LL, 0x1135a2eLL, 0x0c22965LL, 0x08f08d7LL, 0x1b4f42bLL, 0x07d9958LL, 0x08176bbLL,
    0x007ab40LL, 0x0bc696eLL, 0x17ddc24LL, 0x072b21eLL, 0x0c493cdLL, 0x1e7576bLL, 0x0b9ae42LL,
    0x0581746LL, 0x159e81aLL, 0x1f259a1LL, 0x0634de6LL, 0x01d8f29LL};

static const TagCodes delTagCodes25h9 =
    TagCodes("delTag25h9", 25, 9, delTag25h9, sizeof(delTag25h9) / sizeof(delTag25h9[0]));

} // namespace Deltille
