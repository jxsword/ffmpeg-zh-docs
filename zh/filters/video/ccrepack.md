# ccrepack

Repack CEA-708 closed captioning side data

This filter fixes various issues seen with commercial encoders related to upstream malformed CEA-708 payloads, specifically incorrect number of tuples (wrong cc_count for the target FPS), and incorrect ordering of tuples (i.e. the CEA-608 tuples are not at the first entries in the payload).
