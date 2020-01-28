import ADCT


class HANDLER:

    def __init__(self):
        self.datum = []

    def delete(self, index):
        self.datum.remove(index)

    def add(self, add):
        self.datum.append(add)

    # Save the datum data in 'saved.txt' file location
    def save(self, path):
        if self.datum.__len__() == 0:
            print('No cluster models to save. Unable to perform save function')
            return
        w = open(path, 'w')
        for a in range(0, self.datum.__len__()):
            w.write('=== DAT obj ===\n')
            w.write(self.datum[a].__str__())
            w.write('=== DAT end ===\n')
        w.write('\n')
        w.close()

    def load(self, path):    # Path is a string constant
        r = open(path, 'r')
        prev, state = -1, -1
        name, type = '', ''
        rows, columns, cluster_count = 0, 0, 0
        axis, data, centroids, clusters = [], [], [], []
        for line in r.readlines():
            if line.__eq__('Name:\n'):
                state = 0
            if line.__eq__('Dimension:\n'):
                state = 1
            if line.__eq__('Type:\n'):
                state = 2
            if line.__eq__('Axis:\n'):
                state = 3
            if line.__eq__('Data:\n'):
                state = 4
            if line.__eq__('ClusterCount:\n'):
                state = 5
            if line.__eq__('Centroids:\n'):
                state = 6
            if line.__eq__('Clusters:\n'):
                state = 7
            if line.__eq__('=== DAT end ===\n'):
                state = 8
            if state != prev:
                prev = state
                continue
            if state == 0:
                name = line.replace('\n', '').replace('\t', '').replace('  ', '')
                state = -1
                print(name)
            if state == 1:
                temp = line.replace('\n', '').replace('\t', '').replace('  ', '').split(' x ')
                rows = int(temp[0])
                columns = int(temp[1])
                state = -1
            if state == 2:
                type = line.replace('\n', '').replace('\t', '').replace('  ', '')
                state = -1
            if state == 3:
                temp = line.replace('\n', '').replace('\t', '').replace('  ', '').replace('[', '').replace(']', '')
                axis.append(temp)
            if state == 4:
                temp = line.replace('\n', '').replace('\t', '').replace('[', '').replace(']', '').split(', ')
                temp = [float(numeric_string) for numeric_string in temp]
                data.append(temp)
            if state == 5:
                cluster_count = int(line.replace('\n', '').replace('\t', '').replace('  ', ''))
                state = -1
            if state == 6:
                temp = line.replace('\n', '').replace('\t', '').replace('[', '').replace(']', '').split(', ')
                temp = [float(numeric_string) for numeric_string in temp]
                centroids.append(temp)
            if state == 7:
                temp = line.replace('\n', '').replace('\t', '').replace('[', '').replace(']', '').split(', ')
                clusters = [int(numeric_string) for numeric_string in temp]
                state = -1
            if state == 8:
                toAdd = DAT()
                toAdd.create(name, rows, columns, axis, data, cluster_count, centroids, clusters)
                self.datum.append(toAdd)
                name, type = '', ''
                rows, columns, cluster_count = 0, 0, 0
                axis, data, centroids, clusters = [], [], [], []
                state = -1
'''
test = DAT()
test.get_data('../testData.txt')
test.kmc(2)
test2 = HANDLER()
test2.datum.append(test)
test2.datum.append(test)
print(test2.datum[0])
test2.save()
'''
'''
test2 = HANDLER()
test2.load()
temp = test2.datum[0]
temp.kmc(2)
temp.classify()
temp.plot_2d(0, 1).show()
print('end')
# print(test2.datum)
'''
