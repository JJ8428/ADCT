import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D  # Necessary in order to recognize 3D plots as 3D


def gen_hex():    # Generate a random hex value
    return '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def distance(arr1, arr2):    # Find the distance between 2 points
    if arr1.__len__() != arr2.__len__():
        print('Dimension Mismatch')
        exit(1)
    ret = 0
    for i in range(0, arr1.__len__()):
        ret += (arr1[i] - arr2[i]) ** 2
    ret **= .5
    return ret


class ADCT:

    # Basic Constructor
    def __init__(self):
        self.name = 'No name'
        self.rows, self.columns = 0, 0
        self.type = 'No training'
        self.axis = []
        self.data = []
        self.clusterCount = 0
        self.centroids = []
        self.clusters = []

    # Alternate Constructor
    def create(self, name, rows, columns, axis, data, cluster_count, centroids, clusters):
        self.name = name
        self.rows, self.columns = rows, columns
        self.type = 'User inputted'
        self.axis = axis
        self.data = data
        self.clusterCount = cluster_count
        self.centroids = centroids
        self.clusters = clusters

    # toString() method
    def __str__(self):
        ret = 'Name:\n\t' + self.name + '\n'
        ret += 'Dimension:\n\t' + self.rows.__str__() + ' x ' + self.columns.__str__() + '\n'
        ret += 'Type:\n\t' + self.type + '\n'
        ret += 'Axis:\n'
        for a in range(0, self.columns):
            ret += '\t[' + self.axis[a] + ']\n'
        ret += 'Data:\n'
        for a in range(0, self.rows):
            ret += '\t['
            for b in range(0, self.columns):
                ret += self.data[a][b].__str__()
                if b != self.columns - 1:
                    ret += ', '
            ret += ']\n'
        ret += 'ClusterCount:\n\t' + self.clusterCount.__str__() + '\n'
        ret += 'Centroids:\n'
        for a in range(0, self.clusterCount):
            ret += '\t['
            for b in range(0, self.columns):
                ret += self.centroids[a][b].__str__()
                if b != self.columns - 1:
                    ret += ', '
            ret += ']\n'
        if self.type != 'No training':
            ret += 'Clusters:\n\t['
            for a in range(0, self.rows):
                ret += self.clusters[a].__str__()
                if a != self.rows - 1:
                    ret += ', '
            ret += ']\n'
        return ret

    # Method to read data from file
    def get_data(self, file):
        rows = 0
        # GUI requires the path of the file
        try:
            r = open(file, 'r')
        except():
            print('File not found')
            return
        # Harvest the axis
        axis = r.readline().split(',')
        for a in range(0, axis.__len__()):
            axis[a] = axis[a].replace(' ', '').replace('\n', '')
        self.axis = axis
        self.columns = axis.__len__()
        # Harvest the data, dimensions, and check if file is correctly formatted
        for line in r.readlines():
            rows += 1
            if line.split(',').__len__() != self.columns:
                print('Data is not formatted consistently. Correct the file.')
                return
            self.data.append([float(numeric_string) for numeric_string in line.split(',')])
        self.rows = rows
        self.__normal__()
        if self.centroids.__len__() != 0:
            self.classify()

    # Removes duplicate data
    def __normal__(self):
        data = []
        for a in range(0, self.rows):
            if not data.__contains__(self.data[a]):
                data.append(self.data[a])
        self.data = data
        self.rows = data.__len__()

    # Allows for DAT to run kmc immediately after ms and vice versa
    def __wipe__(self):
        self.clusterCount = 0
        self.centroids = []
        self.clusters = []

    # K-Means-Clustering with infinite iterations
    def kmc(self, cluster_count):
        if self.data.__len__() == 0:
            print('Please load data first before calling the classify function.')
        self.__wipe__()
        self.type = 'KMC'
        self.clusterCount = cluster_count
        change_detected = True
        # First iteration of 'n' centroid pairs are first 'n' data points
        group_count = np.zeros(self.clusterCount, dtype=int)
        for a in range(0, self.clusterCount):
            self.centroids.append(self.data[a])
        clusters = np.zeros(self.rows, dtype=int)
        while change_detected:
            for a in range(0, self.clusterCount):
                group_count[a] = 0
            # Figure out which of the 'n' clusters each point belongs to
            for a in range(0, self.rows):
                shortest_dist = -1
                for b in range(0, self.clusterCount):
                    dist = 0
                    for c in range(0, self.columns):
                        dist += (self.data[a][c] - self.centroids[b][c]) ** 2
                    if shortest_dist == -1 or shortest_dist > dist:
                        shortest_dist = dist
                        clusters[a] = b
            # Calculate the new centroids
            group_count.astype(np.int64)
            for a in range(0, self.rows):
                group_count[clusters[a]] += 1
            new_centroids = np.zeros([self.clusterCount, self.columns], dtype=float)
            for a in range(0, self.rows):
                for b in range(0, self.columns):
                    new_centroids[clusters[a]][b] += (self.data[a][b] / group_count[clusters[a]])
            # Break while loop if kmc clusters calculated are equal to previous iteration
            if np.array_equal(self.centroids, new_centroids):
                change_detected = False
            self.centroids = new_centroids
        self.classify()

    # K-Means-Clustering within 'n' iterations, may cut iterations short if centroids are found
    def kmc_custom(self, cluster_count, iterations):
        if self.data.__len__() == 0:
            print('Please load data first before calling the classify function')
        self.__wipe__()
        self.type = "KMC-Custom"
        self.clusterCount = cluster_count
        change_detected = True
        # First iteration of 'n' centroid pairs are first 'n' data points
        group_count = np.zeros(self.clusterCount, dtype=int)
        for a in range(0, self.clusterCount):
            self.centroids.append(self.data[a])
        clusters = np.zeros(self.rows, dtype=int)
        while change_detected:
            for a in range(0, self.clusterCount):
                group_count[a] = 0
            # Figure out which of the 'n' clusters each point belongs to
            for a in range(0, self.rows):
                shortest_dist = -1
                for b in range(0, self.clusterCount):
                    dist = 0
                    for c in range(0, self.columns):
                        dist += (self.data[a][c] - self.centroids[b][c]) ** 2
                    if shortest_dist == -1 or shortest_dist > dist:
                        shortest_dist = dist
                        clusters[a] = b
            # Calculate the new centroids
            group_count.astype(np.int64)
            for a in range(0, self.rows):
                group_count[clusters[a]] += 1
            new_centroids = np.zeros([self.clusterCount, self.columns], dtype=float)
            for a in range(0, self.rows):
                for b in range(0, self.columns):
                    new_centroids[clusters[a]][b] += (self.data[a][b] / group_count[clusters[a]])
            # Break while loop if kmc clusters calculated are equal to previous iteration
            if np.array_equal(self.centroids, new_centroids):
                change_detected = False
            self.centroids = new_centroids
            if iterations <= 1:
                return
            iterations -= 1
        self.classify()

    # Mean-Shifting-Clustering method with self defined bandwidth
    def ms(self):
        if self.data.__len__() == 0:
            print('Please load data first before calling the classify function')
        self.__wipe__()
        self.type = 'MSC'
        self.clusters = np.zeros(self.rows, dtype=int)
        # Bandwidth the average distance away from the mean of all data points
        center = np.zeros(self.columns, dtype=float)
        rads = 0
        for a in range(0, self.rows):
            rads += distance(self.data[a], center)
        rads /= self.rows
        is_cluster = np.zeros(self.rows, dtype=bool)
        while True:
            # Take the first index of a data point not clustered yet
            index = 0
            repeat = False
            for a in range(0, self.rows):
                # If all data points fall in a cluster, than the centroids have been calculated
                if not is_cluster[a]:
                    index = a
                    repeat = True
                    break
            if not repeat:
                break
            centroid = self.data[index][:]
            near_and_nc = np.zeros(self.rows, dtype=bool)
            while True:
                # Filter out which point are not clustered yet and in in the bandwidth of centroid
                for a in range(0, self.rows):
                    near_and_nc[a] = 0
                viable = 0
                for a in range(0, self.rows):
                    if not is_cluster[a]:
                        if distance(self.data[a], centroid) < rads:
                            near_and_nc[a] = True
                            viable += 1
                # Find the average of all viable points
                new_centroid = np.zeros(self.columns, dtype=float)
                for a in range(0, self.rows):
                    if near_and_nc[a]:
                        for b in range(0, self.columns):
                            new_centroid[b] += self.data[a][b] / viable
                # Check if centroids are matching up
                if np.array_equal(new_centroid, centroid):
                    break
                centroid = new_centroid[:]
            self.clusterCount += 1
            self.centroids = np.append(self.centroids, new_centroid, axis=0)
            # All data points within the bandwidth of the centroid are marked is_clustered[...] as True
            for a in range(0, self.rows):
                if near_and_nc[a]:
                    is_cluster[a] = True
        # Fix the member variable centroids since it is not formatted correctly
        fix = []
        for a in range(0, self.centroids.__len__(), self.columns):
            point = self.centroids[a:a+self.columns]
            fix.append(point)
        self.centroids = np.array(fix)
        # Classify data points
        self.classify()

    # Mean-Shifting method with self defined bandwidth
    def ms_custom(self, radius):
        if self.data.__len__() == 0:
            print('Please load data first before calling the classify function')
        self.__wipe__()
        self.type = 'MSC-Custom'
        self.clusters = np.zeros(self.rows, dtype=int)
        # Bandwidth the average distance away from the mean of all data points
        rads = radius
        is_cluster = np.zeros(self.rows, dtype=bool)
        while True:
            # Take the first index of a data point not clustered yet
            index = 0
            repeat = False
            for a in range(0, self.rows):
                # If all data points fall in a cluster, than the centroids have been calculated
                if not is_cluster[a]:
                    index = a
                    repeat = True
                    break
            if not repeat:
                break
            centroid = self.data[index][:]
            near_and_nc = np.zeros(self.rows, dtype=bool)
            while True:
                # Filter out which point are not clustered yet and in in the bandwidth of centroid
                for a in range(0, self.rows):
                    near_and_nc[a] = 0
                viable = 0
                for a in range(0, self.rows):
                    if not is_cluster[a]:
                        if distance(self.data[a], centroid) < rads:
                            near_and_nc[a] = True
                            viable += 1
                # Find the average of all viable points
                new_centroid = np.zeros(self.columns, dtype=float)
                for a in range(0, self.rows):
                    if near_and_nc[a]:
                        for b in range(0, self.columns):
                            new_centroid[b] += self.data[a][b] / viable
                # Check if centroids are matching up
                if np.array_equal(new_centroid, centroid):
                    break
                centroid = new_centroid[:]
            self.clusterCount += 1
            self.centroids = np.append(self.centroids, new_centroid, axis=0)
            # All data points within the bandwidth of the centroid are marked is_clustered[...] as True
            for a in range(0, self.rows):
                if near_and_nc[a]:
                    is_cluster[a] = True
        # Fix the member variable centroids since it is not formatted correctly
        fix = []
        for a in range(0, self.centroids.__len__(), self.columns):
            point = self.centroids[a:a + self.columns]
            fix.append(point)
        self.centroids = np.array(fix)
        # Classify data points
        self.classify()

    # This method is automatically committed at te end of any cluster method called
    def classify(self):
        if self.data.__len__() == 0:
            print('Please load data first before calling the classify function')
        self.clusters = np.zeros(self.rows, dtype=int)
        for a in range(0, self.rows):
            short_dist = -1
            for b in range(0, self.clusterCount):
                dist = distance(self.data[a], self.centroids[b])
                if short_dist == -1 or short_dist > dist:
                    short_dist = dist
                    self.clusters[a] = b

    # Plot a 2D scatter plot with dimensions of given indices as x and y axis
    def plot_2d(self, var1, var2):
        if self.type == 'No training':
            print('Please train your data before calling the plot_2d function')
        for a in range(0, self.clusterCount):
            hex = gen_hex()
            for b in range(0, self.rows):
                if self.clusters[b] == a:
                    plt.scatter(self.data[b][var1], self.data[b][var2], c=hex)
        for a in range(0, self.clusterCount):
            plt.scatter(self.centroids[a][var1], self.centroids[a][var2],
                        c='#ffffff', edgecolors='#000000')
        plt.xlabel(self.axis[var1])
        plt.ylabel(self.axis[var2])
        plt.title('DAT: ' + self.axis[var1] + ' v. ' + self.axis[var2])
        plt.grid(True)
        # plt.show()
        return plt

    # Plot a 3D scatter plot with the dimensions of given indices as x, y, and z axis
    def plot_3d(self, var1, var2, var3):
        if self.type == 'No training':
            print('Please train your data before calling the plot_3d function')
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for a in range(0, self.clusterCount):
            hex = gen_hex()
            for b in range(0, self.rows):
                if self.clusters[b] == a:
                    ax.scatter(self.data[b][var1], self.data[b][var2], self.data[b][var3], c=hex)
        for a in range(0, self.clusterCount):
            ax.scatter(self.centroids[a][var1], self.centroids[a][var2], self.centroids[a][var3],
                       c='#ffffff', edgecolors='#000000')
        ax.set_xlabel(self.axis[var1])
        ax.set_ylabel(self.axis[var2])
        ax.set_zlabel(self.axis[var3])
        plt.grid(True)
        # plt.show()
        return plt
