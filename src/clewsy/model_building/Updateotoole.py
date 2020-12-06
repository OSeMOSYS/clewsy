def Updateotoole(SetNames, NewSetItems, IARList, OARList, otooleOutputDirectory):
    import os
    if not os.path.exists(otooleOutputDirectory):
        os.makedirs(otooleOutputDirectory)
    # Ouptut the sets for otoole:
    for SetName in SetNames:
        with open(os.path.join(otooleOutputDirectory, SetName + '.csv'),'w') as f:
            f.write('VALUE\n')
            for items in NewSetItems[SetNames.index(SetName)]:
                f.write(items['value']+'\n')
    
    # And output the IAR for otoole:
    with open(os.path.join(otooleOutputDirectory, 'InputActivityRatio.csv'),'w') as f:
        f.write('REGION,TECHNOLOGY,FUEL,MODE_OF_OPERATION,YEAR,VALUE\n')
        for item in IARList:
            f.write(str(item['c'][0])+','+str(item['c'][1])+','+str(item['c'][2])+','+str(item['c'][3])+','+str(item['c'][4])+','+str(item['v'])+'\n')

    # And output the OAR for otoole:
    with open(os.path.join(otooleOutputDirectory, 'OutputActivityRatio.csv'),'w') as f:
        f.write('REGION,TECHNOLOGY,FUEL,MODE_OF_OPERATION,YEAR,VALUE\n')
        for item in OARList:
            f.write(str(item['c'][0])+','+str(item['c'][1])+','+str(item['c'][2])+','+str(item['c'][3])+','+str(item['c'][4])+','+str(item['v'])+'\n')
