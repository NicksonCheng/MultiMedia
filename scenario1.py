import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
import os
import pandas as pd

mask_1 = pd.read_csv('soccer1_mask.csv')
mask_2 = pd.read_csv('soccer2_mask.csv')
answer1 = mask_1['GT (True/False)']
answer2 = mask_2['GT (True/False)']

soccer1 = cv2.imread('soccer1.jpg')
img2 = cv2.imread('soccer2.jpg')

soccer1_resize = soccer1.reshape(-1, 3)
img2_resize = img2.reshape((-1, 3))
fig = plt.figure(figsize=(40, 20))
fig.suptitle('Accuracy', fontsize=20)
gaussian = [2, 5, 8, 11, 14, 17, 20, 23]

for i in range(len(gaussian)):
    n = gaussian[i]
    gmm_model = GMM(n_components=n, covariance_type='tied').fit(img2_resize)
    gmm_labels1 = gmm_model.predict(soccer1_resize)

    # choose the gaussian that represent the green ground
    counts = np.bincount(gmm_labels1)
    frequency_num = np.argmax(counts)
    # change frequent number to n+1
    gmm_labels1 = np.where(gmm_labels1 == frequency_num, n+1, gmm_labels1)
    gmm_labels1 = gmm_labels1 - n
    gmm_labels1 = np.clip(gmm_labels1, 0, 1)
    accuracy1 = 0
    for k in range(answer1.size):
        if answer1[k] == gmm_labels1[k]:
            accuracy1 += 1

    s1_acc = str(n) + 'GMM Scenario1: ' + str(round(accuracy1/answer1.size, 4))

    segmented1 = gmm_labels1.reshape(soccer1.shape[0], soccer1.shape[1])

    temp1 = (segmented1)*255  # black 0 white 255 scene

    first_col = fig.add_subplot(5, 4, (i+1)*2-1)
    first_col.title.set_text(s1_acc)
    plt.imshow(temp1, cmap=plt.cm.gray)
    plt.axis('off')

    gmm_labels2 = gmm_model.predict(img2_resize)

    counts = np.bincount(gmm_labels2)
    frequency_num = np.argmax(counts)

    gmm_labels2 = np.where(gmm_labels2 == frequency_num, n+1, gmm_labels2)
    gmm_labels2 = gmm_labels2 - n

    gmm_labels2 = np.clip(gmm_labels2, 0, 1)

    accuracy2 = 0
    for k in range(answer2.size):
        if answer2[k] == gmm_labels2[k]:
            accuracy2 += 1

    s2_acc = str(n) + 'GMM Scenario2 : ' + \
        str(round(accuracy2/answer2.size, 4))

    segmented2 = gmm_labels2.reshape(img2.shape[0], img2.shape[1])

    temp2 = (segmented2)*255
    second_col = fig.add_subplot(5, 4, (i+1)*2)
    second_col.title.set_text(s2_acc)
    plt.imshow(temp2, cmap=plt.cm.gray)
    plt.axis('off')

plt.show()
