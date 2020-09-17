#!/usr/bin/python

# Copyright 2007, 2020 Yannick Gingras <ygingras@ygingras.net>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
# MA 02110-1301 USA

from urllib.request import urlopen
from re import compile
from random import sample

# Some french text from
#   http://www.gutenberg.org/browse/languages/fr

BOOKS = [ 18092, 13704, 17808, 16901, 10774, 15943, 18627, 13598,
  21124, 5781, 11040, 13834, 18262, 18197, 18244, 18245, 9053, 16388,
  15212, 18771, 20823, 20824, 20825, 20865, 17543, 20077, 13938,
  18518, 11494, 20079, 19604, 18890, 15371, 11744, 19982, 20479,
  19440, 15462, 19075, 20664, 17335, 16743, 18583, 16874, 17106,
  16789, 17344, 15305, 8822, 8864, 18367, 18368, 20562, 15871, 16237,
  11590, 11766, 12949, 11049, 17915, 17501, 13808, 16812, 16813,
  16814, 12603, 19756, 18106, 6099, 20761, 13792, 20790, 17670, 16210,
  14536, 20577, 15463, 13247, 12332, 16234, 17565, 17791, 14399,
  20079, 14541, 14512, 17708, 4562, 4570, 4740, 4566, 4561, 4565,
  4563, 4569, 4564, 4741, 4567, 4568, 15543, 19497, 18014, 21544,
  11453, 18864, 8876, 12487, 5158, 20079, 12230, 12782, 12893, 13192,
  13475, 19700, 11769, 12072, 17879, 17880, 12646, 14159, 17363,
  13804, 12251, 20964, 16815, 11176, 17738, 17739, 19184, 19021,
  18962, 18899, 18983, 13219, 18085, 20564, 16235, 17240, 12949,
  14912, 12105, 12437, 10346, 8591, 8591, 20440, 19689, 14151, 18215,
  17372, 10604, 13038, 12451, 15626, 18715, 12356, 18090, 18455,
  20398, 16066, 16067, 14713, 14788, 16020, 17258, 10764, 15459,
  17261, 18864, 21001, 16796, 16795, 18623, 19431, 15375, 17899,
  17758, 18454, 18535, 17963, 18208, 18263, 18403, 18490, 18404,
  18029, 18585, 19045, 18672, 18944, 10824, 17631, 18064, 17419,
  17830, 20703, 6484, 13703, 18059, 15060, 20244, 12247, 17267, 14537,
  19956, 17298, 17248, 10384, 17242, 13861, 16236, 12949, 16709,
  16499, 17577, 15324, 15732, 17353, 17714, 17715, 17716, 17717,
  15885, 18111, 18296, 16883, 17230, 8074, 20949, 19588, 16260, 19954,
  13024, 17736, 6691, 13557, 19440, 16934, 18918, 16492, 18611, 15297,
  14158, 9824, 11650, 12949, 17550, 12950, 13256, 11770, 12726, 12727,
  16848, 15645, 13825, 10687, 5105, 13848, 13598, 13096, 11586, 12603,
  16236, 14703, 18825, 18112, 13059, 13149, 9892, 9893, 11893, 18108,
  18015, 17311, 16824, 17899, 14258, 14310, 13846, 19266, 20554,
  19854, 17940, 17984, 18121, 19455, 13981, 16758, 10289, 18059,
  13771, 14789, 17879, 17880, 16021, 16022, 17868, 17869, 17565,
  16020, 17675, 17676, 16023, 14059, 14030, 13862, 13863, 6501, 13284,
  13036, 13070, 19519, 19536, 19483, 16649, 18693, 18692, 19152,
  14343, 15557, 16824, 14918, 13735, 13734, 18718, 18717, 18716,
  13795, 17540, 17747, 18611, 18491, 10290, 2419, 18321, 6319, 8693,
  8692, 15574, 18006, 18028, 18199, 18200, 13819, 17989, 17990, 17991,
  17992, 9262, 9637, 9638, 9639, 18003, 18271, 2682, 5104, 18697,
  13947, 13948, 13949, 13950, 15208, 7770, 7771, 7772, 13856, 13857,
  21017, 17693, 18401, 18402, 18586, 18773, 18826, 21191, 8863, 13951,
  1910, 13952, 17004, 13230, 13122, 12751, 18074, 15844, 17010, 15558,
  21013, 15458, 18340, 8173, 12949, 9643, 17675, 17676, 18081, 16825,
  12749, 16887, 11037, 20640, 20479, 14828, 13914, 12365, 14720,
  19920, 18494, 15816, 14398, 14702, 19919, 10053, 12602, 14157,
  14156, 14155, 10982, 12065, 6691, 18806, 17555, 18942, 19008, 20703,
  12489, 8864, 8524, 17345, 5147, 19233, 7268, 19248, 10160, 11645,
  7173, 6377, 19344, 19249, 20143, 19345, 17573, 17809, 18106, 19955,
  18455, 15361, 14751, 16237, 15579, 18302, 11588, 15107, 18027,
  17105, 11301, 8650, 8719, 11622, 12665, 8520, 17184, 11646, 18407,
  10442, 12949, 14288, 17578, 17757, 18142, 6739, 11042, 15593, 11767,
  21343, 21804, 10604, 17509, 13794, 17285, 18724, 17420, 17238,
  17505, 14803, 14799, 17947, 17746, 18055, 17123, 17285, 14803,
  14799, 17123, 20262, 17541, 16988, 16886, 17605, 17590, 17542,
  17646, 12603, 17538, 15907, 17509, 12250, 13771, 14789, 13855,
  15739, 14905, 18873, 18873, 19454, 13190, 20864, 16816, 17140,
  15942, 14827, 15846, 15848, 18162, 18311, 15303, 19201, 16710,
  15032, 16128, 15847, 18312, 20720, 17930, 13868, 19219, 14791,
  15312, 15433, 15635, 18294, 18159, 18295, 18695, 20773, 18169,
  18179, 19228, 19227, 18143, 15071, 15849, 18313, 21277, 14309, 8739,
  18024, 6966, 13525, 12289, 14805, 13299, 14285, 14286, 11928, 9261,
  8541, 12137, 8186, 8453, 8454, 8490, 6838, 13628, 6994, 9976, 5423,
  12137, 9644, 17489, 17493, 17494, 17518, 17519, 19657, 9645, 17840,
  10689, 20966, 12271, 10685, 4933, 12566, 16849, 16884, 16816, 17140,
  13187, 20886, 12459, 20414, 21215, 20705, 16238, 9453, 12399, 12120,
  17980, 18797, 20262, 19124, 10697, 17941, 17942, 17688, 14609,
  17828, 14913, 15642, 18920, 11132, 12005, 16989, 18865, 18727,
  11036, 19820, 17258, 19738, 19662, 12472, 12472, 17641, 17319,
  18996, 19186, 17577, 14404, 14541, 20894, 17271, 14804, 17360,
  20490, 17692, 17752, 18067, 18415, 18416, 18034, 17281, 13772,
  19035, 13765, 15554, 13737, 15286, 20441, 21221, 20457, 21199,
  21257, 17794, 14071, 14259, 21669, 4935, 20894, 17868, 17869, 11035,
  16465, 7809, 18358, 7263, 18427, 4785, 14792, 10680, 13676, 17709,
  4708, 11178, 17458, 14082, 14082, 4688, 12284, 12174, 13027, 13336,
  13385, 13400, 13490, 13793, 13562, 13654, 14820, 14082, 14082,
  11300, 11678, 15686, 17670, 17459, 13622, 12504, 12504, 19187,
  20396, 19738, 17691, 9453, 10768, 10841, 11048, 11046, 9818, 10746,
  11199, 11714, 14790, 12949, 11450, 10775, 11175, 11495, 11596,
  11597, 12011, 18353, 11131, 17457, 14793, 19862, 19234, 18610,
  15598, 14115, 16239, 12949, 14115, 16240, 17632, 13189, 13478,
  20829, 20415, 18738, 17810, 16820, 14677, 7012, 7818, 16862, 6318,
  5130, 3645, 5178, 5318, 5644, 18152, 12620, 11905, 18446, 18537,
  12949, 13231, 13221, 20246, 14539, 20635, 11037, 16238, 10906,
  17335, 5258, 11380, 12401, 18089, 18083, 15915, 15915, 14251, 20950,
  18073, 12504, 12504, 14113, 17602, 14397, 17561, 17098, 17641,
  16022, 17233, 17232, 17231, 17234, 17236, 17235, 17233, 17232,
  17231, 17234, 17236, 17235, 17233, 17232, 17231, 17234, 17236,
  17235, 19984, 18061, 12812, 15823, 15739, 14082, 14082, 12562,
  20761, 20790, 15267, 15267, 15811, 15146, 16817, 16818, 16819,
  20498, 15152, 17983, 11747, 13743, 8946, 12999, 2650, 2998, 2999,
  3000, 15288, 15075, 13798, 12562, 15790, 15790, 17691, 21413, 10682,
  12829, 13807, 15113, 9824, 20199, 4559, 9891, 16850, 18133, 12488,
  17098, 4936, 16888, 2820, 2820, 14911, 15589, 7854, 1256, 19149,
  21023, 21792, 20895, 16421, 16649, 16885, 17707, 13594, 13965,
  14692, 19992, 17044, 18889, 17252, 12862, 13431, 14372, 14564,
  13668, 17225, 12666, 13258, 13374, 12338, 12837, 13629, 13837,
  13838, 13875, 13839, 13917, 14038, 17795, 13653, 15397, 13380,
  13671, 13744, 13818, 15584, 17589, 13303, 17911, 13016, 15388,
  20254, 16286, 18075, 13025, 12865, 12869, 13892, 15226, 13198,
  15235, 12448, 12367, 12534, 12447, 12889, 18205, 15239, 15287,
  14688, 13592, 17251, 13263, 20623, 19540, 20108, 20234, 15372,
  18718, 18717, 18716, 20325, 14069, 18112, 14703, 18825, 16828,
  12472, 12472, 9893, 9892, 12969, 12993, 13456, 13013, 12979, 18090,
  15058, 12783, 11621, 14247, 11434, 15059, 15057, 19972, 20507,
  18849, 15942, 15846, 15848, 18162, 18311, 15303, 19201, 16710,
  15032, 16128, 15847, 18312, 20720, 17930, 13868, 19219, 20773,
  18169, 18179, 19228, 19227, 18143, 15071, 15849, 18313, 21277,
  15310, 15310, 20013, 12331, 12080, 21413, 20262, 20013, 16235,
  15790, 15790, 19232, 7812, 14115, 14115, 797, 801, 796, 803, 798,
  802, 18123, 16851, 15295, 15296, 18921, 18922, 18923, 18924, 18925,
  16876, 16875, 19075, 20664, 17916, 17640, 19662, 17734, 17044,
  19075, 20664, 20564, 16336, 5892, 12752, 19112, 20864, 17656, 9945,
  13607, 9894, 10385, 10678, 10953, 11423, 11964, 12295, 12258, 6309,
  17668, 11038, 17696, 17552, 17949, 17950, 17951, 17264, 15882,
  15815, 12301, 11622, 18995, 17643, 2820, 17551, 2820, 14705, 14704,
  20640, 18084, 20394, 20394, 14538, 17662, 14609, 17834, 17834,
  10061, 20568, 15112, 5097, 5095, 5096, 17798, 14287, 17660, 4717,
  11927, 5082, 4968, 4548, 799, 14163, 16826, 5081, 14806, 8174, 8175,
  17796, 11484, 16827, 14810, 7442, 17914, 15646, 5126, 12533, 800,
  3456, 14162, 15203, 17832, 4791, 11589, 16066, 16067, 13794, 17261,
  18211, 9655, 15434, 17623, 17399, 12246, 18669, 20700, 18749, 18940,
  18919, 18920, 18543, 4771, 4772, 5138, 15804, 15805, 4647, 4648,
  4649, 4650, 4651, 4718, 3644, 20372, 11748, 11748, 10683, 15555,
  14693, 20234, 14192, 15372, 15150, 14683, 1339, 18152, 15556, 17673,
  17661, 13207, 13339, 13383, 13523, 13524, 13727, 17516, 6497, 16852,
  5154, 8712, 7462, 17553, 17831, 8560, 6558, 5711, 17533, 6470, 5250,
  13866, 8416, 17517, 8907, 17557, 8563, 7461, 8561]

  

BASE_URL = "http://www.gutenberg.org/"
MAIN_URL = BASE_URL + "etext/%d"
DL_PAT = compile(r'<td class="pgdbfilesdownload"><a href="(/(?:dirs|files)/.*?.txt)"')
MAX = 2**22

for book in sample(BOOKS, 50):
    try:
        data = urlopen(MAIN_URL % book).read(MAX)
        print(book, end=' ') 
        dl = DL_PAT.findall(data)[0]
        print(dl)
        stream = urlopen(BASE_URL + dl)
        open("%04d.txt" % book, "w").write(stream.read(MAX))
    except:
        print("Error")
    
