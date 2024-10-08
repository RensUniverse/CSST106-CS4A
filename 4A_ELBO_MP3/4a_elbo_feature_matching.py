# -*- coding: utf-8 -*-
"""4A_ELBO_feature_matching.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VUdOuZTs2PG5ISHs5Wu5Bnj0ZJvjWsH8

# **Feature Matching naman with Brute-Force and FLANN NI ELBO**
"""

!pip install opencv-contrib-python

# import muna to
import cv2

# Tapos Load mo na yung images
pic1 = cv2.imread('ryushade.jpg', cv2.IMREAD_GRAYSCALE)
pic2 = cv2.imread('ryuwhiteshade.jpg', cv2.IMREAD_GRAYSCALE)

"""**Step 2: Extract ng Keypoints and Descriptors gamit ang SIFT, SURF, and ORB**"""

# SIFT
sift = cv2.SIFT_create()
keypnts_sift_1, descript_sift_1 = sift.detectAndCompute(pic1, None)
keypnts_sift_2, descript_sift_2 = sift.detectAndCompute(pic2, None)

# AKAZE
akaze = cv2.AKAZE_create()
keypnts_akaze_1, descript_akaze_1 = akaze.detectAndCompute(pic1, None)
keypnts_akaze_2, descript_akaze_2 = akaze.detectAndCompute(pic2, None)

# ORB
orb = cv2.ORB_create()
keypnts_orb_1, descript_orb_1 = orb.detectAndCompute(pic1, None)
keypnts_orb_2, descript_orb_2 = orb.detectAndCompute(pic2, None)

"""**STEP 3.1: Brute-Force Matcher muna**

"""

bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches_sift_bf = bf.match(descript_sift_1, descript_sift_2)
matches_sift_bf = sorted(matches_sift_bf, key=lambda x: x.distance)

# Draw matches lang
img_sift_bf = cv2.drawMatches(pic1, keypnts_sift_1, pic2, keypnts_sift_2, matches_sift_bf[:50], None)
cv2.imwrite('sift_bf_match.jpg', img_sift_bf)

"""**STEP 3.2: FLANN Matcher**"""

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches_sift_flann = flann.knnMatch(descript_sift_1, descript_sift_2, k=2)

good_matches = []
for m, n in matches_sift_flann:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# Draw matches
img_sift_flann = cv2.drawMatches(pic1, keypnts_sift_1, pic2, keypnts_sift_2, good_matches[:50], None)
cv2.imwrite('sift_flann_match.jpg', img_sift_flann)