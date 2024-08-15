# Schema
# [
#     { 
#         "keysize": unit or string ID (string IDs must be handled via custom code; numerical units will be auto-calculated),
#         "stabilizer_dist": X distance of one of the stabilizer holes from the switch center (or leftside if stabilizer_dist_right is defined),
#         "stabilizer_dist_right": X distance of the right stabilizer holes from the switch center (for asymmetrical stabilizers),
#         "stabilizer_vert": Whether or not to rotate the stabilizers vertically
#     },
#     ...
# ]


# Simple MX
KEYSIZES_MX = [
    {
        "keysize": 1
    },
    {
        "keysize": 1.25
    },
    {
        "keysize": 1.5
    },
    {
        "keysize": 1.75
    },
    {
        "keysize": 2,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": 2.25,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": 2.75,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": 3,
        "stabilizer_dist": 19.05
    },
    {
        "keysize": 6,
        "stabilizer_dist": 47.625
    },
    {
        "keysize": 6.25,
        "stabilizer_dist": 50
    },
    {
        "keysize": 7,
        "stabilizer_dist": 57.15
    },
    {
        "keysize": 8,
        "stabilizer_dist": 66.675
    },
    {
        "keysize": 9,
        "stabilizer_dist": 66.675
    },
    {
        "keysize": 10,
        "stabilizer_dist": 66.675
    },
    {
        "keysize": "ISO",
        "stabilizer_vert": True,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": "ISO-Rotated",
        "stabilizer_dist": 11.938
    },
    {
        "keysize": "6U-Offcenter",
        "stabilizer_dist": 57.15,
        "stabilizer_dist_right": 38.1
    },
    {
        "keysize": "2U-Vertical",
        "stabilizer_vert": True,
        "stabilizer_dist": 11.938
    }
]


# Alps (with plate-mount stabilizers)
KEYSIZES_ALPS = [
    {"keysize": 1},
    {"keysize": 1.25},
    {"keysize": 1.5},
    {"keysize": 1.75},
    {"keysize": 2},
    {"keysize": 2.25},
    {"keysize": 2.75},
    {"keysize": 3},
    {"keysize": 6.25},
    {"keysize": 6.5},
    {"keysize": 7},
    {"keysize": "ISO"}
]


# MX/Alps Hybrid
KEYSIZES_MX_ALPS = KEYSIZES_MX[:] + [
    {"keysize": 6.5}
]


# Alps with MX stabilizers where supported (DCS and similar)
KEYSIZES_ALPS_MX_STABILIZERS = [
    {
        "keysize": 1
    },
    {
        "keysize": 1.25
    },
    {
        "keysize": 1.5
    },
    {
        "keysize": 1.75
    },
    {
        "keysize": 2,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": 2.25,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": 2.75,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": 6.25,
        "stabilizer_dist": 50
    },
    {
        "keysize": 6.5
    },
    {
        "keysize": 7,
        "stabilizer_dist": 57.15
    },
    {
        "keysize": "ISO",
        "stabilizer_vert": True,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": "ISO-Rotated",
        "stabilizer_dist": 11.938
    },
    {
        "keysize": "2U-Vertical",
        "stabilizer_vert": True,
        "stabilizer_dist": 11.938
    }
]


# Gateron KS-33 (Low Profile 2.0)
KEYSIZES_GATERON_KS33 = [
    {"keysize": 1},
    {"keysize": 1.25},
    {"keysize": 1.5},
    {"keysize": 1.75},
    {
        "keysize": 2,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": 2.25,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": 2.75,
        "stabilizer_dist": 11.938
    },
    {
        "keysize": 6.25,
        "stabilizer_dist": 50
    },
    {
        "keysize": 7,
        "stabilizer_dist": 57.15
    },
]


# Kailh PG1353 (Choc V2)
# For now, just use the Gateron KS33 sizes unless they start to differ in support
KEYSIZES_KAILH_PG1353 = KEYSIZES_GATERON_KS33