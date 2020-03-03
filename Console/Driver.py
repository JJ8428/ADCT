from Console.DataOBJ import DAT
from Console.DataHandler import HANDLER

curr = DAT()
obj = HANDLER()
path = 'Data/saved.txt'

print('Welcome to the ADCT Console!')
while True:
    print('Select the index of user\'s choice:')
    choice = int(input('\t1. Load previous ADCTs'
                       + '\n\t2. Save current ADCTs'
                       + '\n\t3. Create null DAT instance'
                       + '\n\t4. Modify data DAT instance'
                       + '\n\t5. Delete DAT instance'
                       + '\n\t6. Train DAT instance'
                       + '\n\t7. View Summary of DAT'
                       + '\n\t8. Generate plot'
                       + '\n\t9. Exit Program\n'))
    # If the user does not enter proper input
    if choice > 9 or choice < 1:
        print('Invalid Input')
        exit(1)
    if choice == 1:
        fP = path
        print('Which source file to load from?')
        choice0 = int(input('\t1. Provided Src file'
                            + '\n\t2. Custom Src file\n'))
        if choice0 == 2:
            fP = input('Enter file path of Custom Src file:\n')
        choice1 = input('Any unsaved work will be lost. Continue loading data? (Y/N)\n')
        if not choice1.lower().__eq__('y'):
            continue
        obj.load(fP)
        print('Successfully loaded ' + obj.datum.__len__().__str__() + ' DAT instance(s)')
    if choice == 2:
        fP = path
        print('Which source file to save into?')
        choice0 = int(input('\t1. Provided Src file'
                            + '\n\t2. Custom Src file\n'))
        if choice0 == 2:
            fP = input('Enter file path of Custom Src file:\n')
        choice1 = input('Previous data will be overwritten. Continue saving data? (Y/N)\n')
        if not choice1.lower().__eq__('y'):
            continue
        obj.save(fP)
        print('Successfully saved ' + obj.datum.__len__().__str__() + ' DAT instance(s)')
    if choice == 3:
        toAdd = DAT()
        obj.add(toAdd)
        print('Created new DAT instance at the last index.')
    if choice == 4:
        print('Indices:')
        for a in range(0, obj.datum.__len__()):
            print('\t' + a.__str__() + '. ' + obj.datum[a].name)
        choice0 = int(input('Enter the index of the instance to modify data:\n'))
        if choice0 < 0 or choice0 > obj.datum.__len__() - 1:
            print('Invalid index')
            continue
        fP = input('Enter the file path of data to insert into the DAT:\n')
        name = input('Enter the name of the updated DAT instance:\n')
        obj.datum[choice0].get_data(fP)
        obj.datum[choice0].name = name
    if choice == 5:
        print('Indices:')
        for a in range(0, obj.datum.__len__()):
            print('\t' + a.__str__() + '. ' + obj.datum[a].name)
        choice1 = int(input('Enter the index of the instance to delete:\n'))
        if choice1 < 0 or choice1 > obj.datum.__len__() - 1:
            print('Invalid index')
            continue
        obj.delete(choice1)
    if choice == 6:
        print('Indices:')
        for a in range(0, obj.datum.__len__()):
            print('\t' + a.__str__() + '. ' + obj.datum[a].name)
        choice0 = int(input('Select the index of instance to train:\n'))
        if choice0 < 0 or choice0 > obj.datum.__len__() - 1:
            print('Invalid index')
            continue
        print('Select index of type of clustering to perform:')
        choice1 = int(input('\t1. K-Means Clustering'
                            + '\n\t2. K-Means Clustering within \'n\' iterations'
                            + '\n\t3. Mean-Shift Clustering'
                            + '\n\t4. Mean-Shift Clustering within \'n\' bandwidth\n'))
        if choice1 > 4 or choice < 1:
            print('Invalid Input')
            continue
        if choice1 == 1:
            clusters = int(input('Enter the number of clusters to commit KMC under:\n'))
            obj.datum[choice0].kmc(clusters)
        elif choice1 == 2:
            clusters = int(input('Enter the number of clusters to commit KMC under:\n'))
            iterations = int(input('Enter the number of iterations to commit KMC under:\n'))
            obj.datum[choice0].kmc_custom(clusters, iterations)
        elif choice1 == 3:
            obj.datum[choice0].ms()
        else:
            bandwidth = int(input('Enter the bandwidth of clusters to commit MS under:\n'))
            obj.datum[choice0].ms_custom(bandwidth)
        print('Clustering attempted')
    if choice == 7:
        print('View summary of ...')
        choice0 = int(input('\t1. One instance of a DAT'
                            + '\n\t2. All DATs of inventory\n'))
        if choice0 == 1:
            for a in range(0, obj.datum.__len__()):
                print('\t' + a.__str__() + '. ' + obj.datum[a].name)
            choice1 = int(input('Enter the index of instance to view summary:\n'))
            if choice1 < 0 or choice1 > obj.datum.__len__() - 1:
                print('Invalid index')
                continue
            print(obj.datum[choice1].__str__())
        else:
            for a in range(0, obj.datum.__len__()):
                print('\n' + obj.datum[a].__str__() + '\n')
    if choice == 8:
        print('Indices:')
        for a in range(0, obj.datum.__len__()):
            toPrint = '\t' + a.__str__() + '. ' + obj.datum[a].name + ' || '
            for b in range(0, obj.datum[a].axis.__len__()):
                toPrint += '[' + obj.datum[a].axis[b] + ']'
            print(toPrint)
        choice0 = int(input('Enter the index of DAT to plot:\n'))
        print('Create a plot for ...')
        choice1 = int(input('\t1. 2D'
                            + '\n\t2. 3D\n'))
        if choice1 < 1 or choice1 > 2:
            print('Invalid Index')
            continue
        print('Axes:')
        for a in range(0, obj.datum[choice0].axis.__len__()):
            print(a.__str__() + ' [' + obj.datum[a].axis[a] + ']')
        if choice1 == 1:
            var1 = int(input('Enter the index of variable #1 to plot:\n'))
            var2 = int(input('Enter the index of variable #2 to plot:\n'))
            obj.datum[choice0].plot_2d(var1, var2).show()
            obj.datum[choice0].plot_2d(var1, var2).savefig('Data/2D/' + obj.datum[choice0].axis[var1] + '_v_'
                                                           + obj.datum[choice0].axis[var2] + '.png')
            print('Plot successfully generated and saved')
        else:
            var1 = int(input('Enter the index of variable #1 to plot:\n'))
            var2 = int(input('Enter the index of variable #2 to plot:\n'))
            var3 = int(input('Enter the index of variable #3 to plot:\n'))
            obj.datum[choice0].plot_3d(var1, var2, var3).show()
            print('Plot successfully generated')
    if choice == 9:
        choice0 = input('Exit without saving? (Y/N)\n')
        if not choice0.lower().__eq__('y'):
            continue
        exit(1)
