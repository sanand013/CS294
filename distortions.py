import numpy as np

#image = np.ones((28, 28))
image = np.random.rand(28, 28)

def kSpaceTrajectoryFunction(timeLinePosition):
    #For non-cartesian trajectories this is non-trivial
    return timeLinePosition

def distortion(timeLinePosition, position, shape1):
    def scale1(time1, pos1, shape2):
        distortionFactor = 0.01
        dist1 = time1 * distortionFactor
        #dist1 = 0.1
        fromCenter = pos1 - (shape2 - 1.0)/2.0
        pos1 = pos1 + (dist1 * fromCenter)
        return pos1
    #newPosition = [scale1(timeLinePosition[1], position[0], shape1[0]), scale1(timeLinePosition[1], position[1], shape1[1])]
    if timeLinePosition[0] == 0:
        newPosition = position
    else:
        distortionFactor = 0.1
        newPosition = [position[0] + np.random.normal(0, distortionFactor) , position[1]]

    newPosition = [int(newPosition[0]), int(newPosition[1])]
    return newPosition

def makeIndexMatrix(shape1):
    indexMatrix = []
    a = 0
    while a < shape1[0]:
        indexMatrix.append([])
        b = 0
        while b < shape1[1]:
            indexMatrix[a].append([a,b])
            b += 1
        a += 1
    return indexMatrix

def thoughtKRealK(shape1):
    thoughtK = []
    realK = []
    a = 0
    while a < shape1[0]:
        b = 0
        while b < shape1[1]:
            timeLinePosition = [a, b]
            thoughtKPos = kSpaceTrajectoryFunction(timeLinePosition)
            thoughtK.append(thoughtKPos)
            newPosition = distortion(timeLinePosition, thoughtKPos, shape1)
            realK.append(newPosition)
            b += 1
        a += 1
    return (thoughtK, realK)

def makeThoughtKGrid(thoughtK, shape1):
    thoughtKGrid = np.zeros(shape1)
    for pos in thoughtK:
        thoughtKGrid[pos[0]][pos[1]] = 1
    return thoughtKGrid

def handleUnsampled(pos, shape1):
    if pos[0] >= shape1[0]:
        pos[0] = shape1[0] - 1
    if pos[1] >= shape1[1]:
        pos[1] = shape1[1] - 1
    if pos[0] < 0:
        pos[0] = 0
    if pos[1] < 0:
        pos[1] = 0
    return pos

def makeCollectedImage(image1, thoughtK, realK):
    shape1 = image1.shape
    valueGrid = np.zeros(shape1)
    a = 0
    while a < len(thoughtK):
        realKpos = realK[a]
        realKpos = handleUnsampled(realKpos, shape1)
        value = image1[realKpos[0]][realKpos[1]]
        thoughtKpos = thoughtK[a]
        valueGrid[thoughtKpos[0]][thoughtKpos[1]] = value
        a += 1
    return valueGrid

def fullSamplingDistortion(image1):
    shape1 = image1.shape
    (thoughtK, realK) = thoughtKRealK(shape1)
    thoughtKGrid = makeThoughtKGrid(thoughtK, shape1)
    valueGrid = makeCollectedImage(image1, thoughtK, realK)
    return (np.array(thoughtKGrid), np.array(valueGrid))

(thoughtKGrid, valueGrid) = fullSamplingDistortion(image)
#print (valueGrid[5])
#print (image[5])

import matplotlib.pyplot as plt
f, axarr = plt.subplots(1,2)
axarr[0].imshow(image)
axarr[1].imshow(valueGrid)
#axarr[1].imshow(thoughtKGrid)
plt.show()
