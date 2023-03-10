""" Generlized clewsy: python script::

    Country Code 3 letters  == <ccd>
    Region Code 3 letters   == <rgn>
    Filter Code 3 letters   == <flt, rgn, ccd>

    Workflow:
        1- Input Data set preparation:
            [geofilter|canada + remove other technologies] >> 'osemosys_global' >>
                [./data-inp/osemosys-<ccd>/\*.csv]
            GAEZ[Land & Water Database] >> Clustering scripts >> [./data-inp/gaezclstr-<ccd>/\*.csv]

        2- clewsy:
            [./data-inp/gaezclstr-<ccd>/\*.csv + <clewsy parametrization file == CLEWS-CCD.yaml> +
            ./data-inp/osemosys-<ccd>/\*.csv] >>
            python src/build/build.py >>
                ./data-out/gaezclstr-<ccd>/\*.csv
        Supported OutputFormat == MoManI; otoole::Update; otoole::Append

This script (C) Taco Niet 2019-2020
"""

################################################################################
# Function to Create Set data::Called in BuildCLEWsModel()
################################################################
def create_set(set_names, new_SetItems, new_setGroups, sets):
    set_names.append(sets)
    new_SetItems.append([])
    new_setGroups.append([])

################################################################################
# Function to Add Activity List Items::Called in BuildCLEWsModel()
################################################################
def AddActivityListItems(year1, region, input1, input2, List, value = None, g = "1", v = "1"):
    for year in year1:
        Sets = [region, input1, input2, g, year]
        Value = value
        Item = {"c": Sets, "v": v}
        List.append(Item)

################################################################################
# Function to Fill Set data elements
################################################################
def Fill_Set(new_set_items, set_names, sets, value1, color1, name1 = '', t = "name"):
    new_set_items[set_names.index(sets)].append(\
    {"value": value1, t: name1, "color": color1})

################################################################################
# Function to OUTPUT TO OTOOLE FORMAT
################################################################
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

################################################################################
# Function to APPEND OTOOLE OUTPUT DATA
################################################################
def Appendotoole(SetNames, NewSetItems, IARList, OARList, otooleOutputDirectory, OsemosysGlobalPath):
    import os
    import shutil
    import decimal
    if not os.path.exists(otooleOutputDirectory):
        os.makedirs(otooleOutputDirectory)

    # Ouptut the sets for otoole:
    for SetName in SetNames:
        with open(os.path.join(otooleOutputDirectory, SetName + '.csv'),'w') as f:
            with open(os.path.join(OsemosysGlobalPath, SetName + '.csv'), 'r') as fin:
                if SetName == 'MODE_OF_OPERATION':
                    for items in NewSetItems[SetNames.index(SetName)]:
                        f.write(items['value']+'\n')
                else:
                    f.write(fin.read())
                    for items in NewSetItems[SetNames.index(SetName)]:
                        f.write(items['value']+'\n')

    # And output the IAR for otoole:
    #appnd IARList items to otoole output file
    with open(os.path.join(otooleOutputDirectory, 'InputActivityRatio.csv'),'w') as f:
        with open(os.path.join(OsemosysGlobalPath, 'InputActivityRatio.csv'), 'r') as fin:
            f.write(fin.read())
            for item in IARList:
                f.write(str(item['c'][0])+','+str(item['c'][1])+','+str(item['c'][2])+','+str(item['c'][3])+','+str(item['c'][4])+','+str(item['v'])+'\n')

    # ASR-Note: Use And output the OAR for otoole as Code section template for::
    #   ASR-TODO: Appendotoole we now need to also append the ResidCapList and append it to the ResidualCapacity.csv
    # And output the OAR for otoole:
    with open(os.path.join(otooleOutputDirectory, 'OutputActivityRatio.csv'),'w') as f:
        with open(os.path.join(OsemosysGlobalPath, 'OutputActivityRatio.csv'), 'r') as fin:
            f.write(fin.read())
            for item in OARList:
                f.write(str(item['c'][0])+','+str(item['c'][1])+','+str(item['c'][2])+','+str(item['c'][3])+','+str(item['c'][4])+','+str(item['v'])+'\n')

    for file in os.listdir(OsemosysGlobalPath):
        if not os.path.exists(os.path.join(otooleOutputDirectory, file)):
            shutil.copyfile(os.path.join(OsemosysGlobalPath, file), os.path.join(otooleOutputDirectory, file))


#    os.remove(otooleOutputDirectory + 'MODE_OF_OPERATION.csv')
#    shutil.copyfile(OsemosysGlobalPath + 'MODE_OF_OPERATION.csv', otooleOutputDirectory + 'MODE_OF_OPERATION.csv')
    for file in os.listdir(otooleOutputDirectory):
            if not os.path.exists(os.path.join(otooleOutputDirectory, file)):
                with open(file):
                    reader = csv.reader()
                    for row in reader:
                        ctx.create_decimal(row[-1])
    if 'COMMODITY.csv' in os.listdir(otooleOutputDirectory):
        os.rename(os.path.join(otooleOutputDirectory, 'COMMODITY.csv'), os.path.join(otooleOutputDirectory, 'FUEL.csv'))
    else:
        pass
    with open(os.path.join(otooleOutputDirectory, 'CapacityToActivityUnit.csv'),'w') as f1:
        with open(os.path.join(otooleOutputDirectory, 'TECHNOLOGY.csv'),'r') as f2:
            f1.write('REGION,TECHNOLOGY,VALUE\n')
            for technology in f2:
                if technology.startswith('PWR'):
                    f1.write('GLOBAL,'+technology[:-1]+',31.536\n')

################################################################################
# Function to UPDATE MOMANI WITH NEW DATA
################################################################
def UpdateMoManI(Model, SetNames, NewSetItems, NewSetGroups, IARList, OARList):
    import sys
    import pymongo
    from bson.objectid import ObjectId
    from bson.binary import Binary
    import uuid

    # Connect to the Mongodb daemon
    client = pymongo.MongoClient()

    # Connect to the momani database
    db = client.momani
    # OR can use:  db = client['pymongo_test']

    # Original search for string:
    ModelData = db.ComposedModel.find_one({"name": Model})
    try:
        Model_id = Binary(uuid.UUID(str(ModelData['_id'])).bytes, 4)
    except TypeError:
        sys.exit(
            "\x1b[0;30;41m Model \x1b[0m\x1b[6;30;42m" + Model + "\x1b[0m\x1b[0;30;41m not found in MoManI.  Please create the model in MoManI before running this script. \x1b[0m")

    Scenarios = db.Scenario.find({"modelId": Model_id})
    NumberofScenarios = db.Scenario.count_documents({"modelId": Model_id})

    # NumberofScenarios = Scenarios.count()
    if NumberofScenarios > 1:
        print("These are multiple scenarios in the MoManI database for", Model + ":")
        print("  Number Name                 Description                    Revision")
        for index, Scenario in enumerate(Scenarios):
            print("     ", str(index).ljust(2), Scenario['name'].ljust(20), Scenario['description'].ljust(30),
                  Scenario['revision'])
        print(
            "\x1b[0;30;41m Note: Updating one scenario with new set definitions will change the sets for all scenarios! \x1b[0m")
        while True:
            try:
                Choice = int(input("Please enter the number of the scenario you want to update:"))
            except ValueError:
                print("Sorry, I didn't understand that.")
                # better try again... Return to the start of the loop
                continue
            else:
                if 0 <= Choice <= NumberofScenarios - 1:
                    # We have a valid scencario choice - continue
                    break
                else:
                    print("Scenario number incorrectly entered.  Please try again.")

        Scenarios.rewind()  # Unwind the iteration through the query so we can get the correct scenario.
        Scenario = Scenarios[Choice]
    else:
        Scenario = db.Scenario.find_one({"modelId": Model_id})

    # Confirm users choice before updating scenario:
    while True:
        print("You have chosen to update scenario:")
        print("      Name                 Description                    Revision")
        print("     ", Scenario['name'].ljust(20), Scenario['description'].ljust(30), Scenario['revision'])
        print(
            "\x1b[0;30;41m Note: Updating one scenario with new set definitions will change the sets for all scenarios! \x1b[0m")
        Continue = input("Please confirm if you want to continue (y/n):")
        if Continue == 'y' or Continue == 'Y':
            # We have a valid scencario choice - continue
            break
        else:
            sys.exit("\x1b[0;30;41m You chose not to continue.  Exiting script. \x1b[0m")

    # Now we know that we have the correct scenario, so we can continue with processing things from that scenario.
    # Scenario = db.Scenario.find_one({"modelId":Model_id})
    Scenario_id = Binary(uuid.UUID(str(Scenario['_id'])).bytes, 4)

    # Create energy structure from model structure file
    sets = ModelData['sets']

    # Now upload the new sets to the database:
    for SetName in SetNames:
        SetforID = db.Sets.find_one({'name': SetName})
        if SetforID == None:
            print("Set\x1b[0;30;41m", SetName, "\x1b[0mnot found for", Model, "- continuing...")
            continue
        # print(SetforID)
        setId = Binary(uuid.UUID(str(SetforID['_id'])).bytes, 4)

        # Get the Object ID for the set we want to replace in the database
        set = db.SetData.find_one({"setId": setId, "modelId": Model_id})
        if set == None:
            # Should be impossible to get here, since we found the set above with the right name, but just in case...
            print("Set Data Not Found for set: ", SetName, "setId: ", setId, "modelId: ", Model_id)
            print("Creating new set data...")
            id = ObjectId()
            # Create new set with new data:
            newset = {"_id": id, 'setId': setId, 'modelId': Model_id, 'items': NewSetItems[SetNames.index(SetName)],
                      'groups': NewSetGroups[SetNames.index(SetName)]}
            db.SetData.insert_one(newset)
        else:
            id = ObjectId(set['_id'])
            # Create new set with new data:
            newset = {"_id": id, 'setId': setId, 'modelId': Model_id, 'items': NewSetItems[SetNames.index(SetName)],
                      'groups': NewSetGroups[SetNames.index(SetName)]}
            db.SetData.bulk_write([pymongo.UpdateOne({'_id': id}, {"$set": newset})])
        print("Set\x1b[6;30;42m", SetName, "\x1b[0mupdated for", Model, "model with",
              len(NewSetItems[SetNames.index(SetName)]), "items.")

    # And upload the IAR data into MoManI...

    # Find the parameter we're trying to update:
    InActRat = db.Parameters.find_one({"name": "InputActivityRatio"})
    InActRat_id = Binary(uuid.UUID(str(InActRat['_id'])).bytes, 4)

    Parameter = db.ParameterData.find_one({"scenarioId": Scenario_id, "parameterId": InActRat_id})
    # If parameters haven't been defined yet, then we need to create them...  Easiest to do this in MoManI...
    try:
        ParameterData_id = Binary(uuid.UUID(str(Parameter['_id'])).bytes, 4)
    except TypeError:
        sys.exit(
            "\x1b[0;30;41m Parameter \x1b[0m\x1b[6;30;42m" + "InputActivityRatio" + "\x1b[0m\x1b[0;30;41m not found in MoManI.  Please create the InputActivityRatio and OutputActivityRatio in MoManI before running this script. \x1b[0m")

    # We need to drop all existing input activity ratio parameters from the data bundle first, to clear things for the new data...
    # NOTE:  THIS IS THE EASY WAY TO DO THIS.  IF WE EDIT THE PARAMETERS IN MoManI WE'LL NEED TO DO IT SOME OTHER WAY...
    db.ParameterDataItemBundle.delete_many({"parameterDataId": ParameterData_id})

    # Now we should have a clean place to put the new input activity ratio parameters...

    # And upload into MoManI
    NumtoGroup = 10000  # From MoManI Code:  private const int ItemStorageBundleSize = 10000;
    q, r = divmod(len(IARList), NumtoGroup)
    for count in range(0, q + 1):
        itemBundle = IARList[count * NumtoGroup:count * NumtoGroup + NumtoGroup]
        id = ObjectId()
        set = {"_id": id, "parameterDataId": ParameterData_id, "itemBundle": itemBundle}
        db.ParameterDataItemBundle.insert_one(set)
        print("InputActivityRatio group", count, "uploaded for", Model, "model with", len(itemBundle), "items.")

    # And upload the OAR data into MoManI...

    # Find the parameter we're trying to update:
    OutActRat = db.Parameters.find_one({"name": "OutputActivityRatio"})
    OutActRat_id = Binary(uuid.UUID(str(OutActRat['_id'])).bytes, 4)

    Parameter = db.ParameterData.find_one({"scenarioId": Scenario_id, "parameterId": OutActRat_id})
    # If parameters haven't been defined yet, then we need to create them...  Easiest to do this in MoManI...
    try:
        ParameterData_id = Binary(uuid.UUID(str(Parameter['_id'])).bytes, 4)
    except TypeError:
        sys.exit(
            "\x1b[0;30;41m Parameter \x1b[0m\x1b[6;30;42m" + "OutputActivityRatio" + "\x1b[0m\x1b[0;30;41m not found in MoManI.  Please create the InputActivityRatio and OutputActivityRatio in MoManI before running this script. \x1b[0m")

    # We need to drop all existing output activity ratio parameters from the data bundle first, to clear things for the new data...
    # NOTE:  THIS IS THE EASY WAY TO DO THIS.  IF WE EDIT THE PARAMETERS IN MoManI WE'LL NEED TO DO IT SOME OTHER WAY...
    db.ParameterDataItemBundle.delete_many({"parameterDataId": ParameterData_id})

    # Now we should have a clean place to put the new output activity ratio parameters...

    # And upload the OAR data into MoManI...
    q, r = divmod(len(OARList), NumtoGroup)
    for count in range(0, q + 1):
        itemBundle = OARList[count * NumtoGroup:count * NumtoGroup + NumtoGroup]
        id = ObjectId()
        set = {"_id": id, "parameterDataId": ParameterData_id, "itemBundle": itemBundle}
        db.ParameterDataItemBundle.insert_one(set)
        print("OutputActivityRatio group", count, "uploaded for", Model, "model with", len(itemBundle), "items.")

################################################################################
# Function to Build CLEWs Model
################################################################
def BuildCLEWsModel(data, yaml_file):
    import sys
    import os

    import colorama
    import decimal
    import collections
    colorama.init()

    # create a decimal context
    ctx = decimal.Context()
    # Set to 4 Sig Figs for MoManI speed
    ctx.prec = 2
    # Unpacking yaml parameters
    # Model external dependencies: Directories & Files
    Model = data['Model']
    OutputFormat = data['OutputFormat']
    OperationModesOut = data['OperationModesOut']
    otooleOutputDirectory = data['otooleOutputDirectory']
    DataDirectoryName = data['DataDirectoryName']
    OsemosysGlobalPath = data['OsemosysGlobalPath']
    ClusterBaseFileName = data['ClusterBaseFileName']
    PrecipitationClusterBaseFileName = data['PrecipitationClusterBaseFileName']
    EvapotranspirationClusterBaseFileName = data['EvapotranspirationClusterBaseFileName']
    IrrigationWaterDeficitClusterBaseFileName = data['IrrigationWaterDeficitClusterBaseFileName']

    # Model Time Space parameters: Years, Land, Regions,... TimeSlices
    YearsN = data['Years']
    Years = [str(i) for i in data['Years']]
    LandRegions = data['LandRegions']
    LandToGridMap = data['LandToGridMap']
    LandUseCodes = data['LandUseCodes']
    # Sort land use codes to make visualization script effective
    # ASR- TODO: Converge w/ Taco need for collections.OrderedDict...)
    LandUseCodes = collections.OrderedDict(sorted(LandUseCodes.items()))
    Regions = data['Regions']
    Timeslices = data['Timeslices']

    # Model Land, Water parameters: Irrigation type, Rainfed,...
    IntensityList = data['IntensityList']
    IrrigationTypeList = data['IrrigationTypeList']
    EvapotranspirationPercentPRCOtherLandUse = data['EvapotranspirationPercentPRCOtherLandUse']
    GroundwaterPercentofExcessOtherLandUse = data['GroundwaterPercentofExcessOtherLandUse']
    GroundwaterPercentofExcess = data['GroundwaterPercentofExcess']

    # Model Energy parameters: Fuels, Transformation Tech,...
    EndUseFuels = data['EndUseFuels']
    ImportFuels = data['ImportFuels']
    ExportFuels = data['ExportFuels']
    DomesticMining = data['DomesticMining']
    DomesticRenewables = data['DomesticRenewables']
    TransformationTechnologies = data['TransformationTechnologies']
    PowerPlants = data['PowerPlants']
    Emissions = data['Emissions']

    # Model Agriculture & Crop yield  parameters:
    AgriculturalResidualCapacityRetirementYears = data['AgriculturalResidualCapacityRetirementYears']
    CropYieldFactors = data['CropYieldFactors']
    AgriculturalResidualCapacity = data['AgriculturalResidualCapacity']
    # ASR-TODO: Use sorted(data['AgriculturalResidualCapacity']) after studying collections.OrderedDict(sorted(...))
    SAgriculturalResidualCapacity = sorted(data['AgriculturalResidualCapacity'])

    print("BuildCLEWsModel w/: yaml file= {0}::"
        "\n\tModel= {1}; OutputFormat= {2};"
        "\n\tOperationModesOut= {3}; otooleOutputDirectory= {4}"
        "\n\tDataDirectoryName= {5}; OsemosysGlobalPath= {6}"
        "\n\tClusterBaseFileName= {7}; PrecipitationClusterBaseFileName= {8}"
        "\n\tEvapotranspirationClusterBaseFileName= {9}; IrrigationWaterDeficitClusterBaseFileName= {10}"
            .format(yaml_file, Model, OutputFormat, OperationModesOut, otooleOutputDirectory,
            DataDirectoryName, OsemosysGlobalPath, ClusterBaseFileName, PrecipitationClusterBaseFileName,
            EvapotranspirationClusterBaseFileName, IrrigationWaterDeficitClusterBaseFileName))
    print("--------------------------------\n")
    user_inp = raw_input("BuildCLEWsModel parameters OK? (Y/N)")
    print("ASR-Probe::user_inp= {0}" .format(user_inp))
    if user_inp != "Y":
        sys.exit("Please correct BuildCLEWsModel parameters & re-run... Exiting!!!")

    ################################################
    # CREATE ENERGY SET INFORMATION
    ################################################
    # Create empty list for new sets
    SetNames = []
    NewSetItems = []
    NewSetGroups = []
    IARList = []
    OARList = []
    ResidCapList = []

    if OutputFormat != 'append_otoole':
        # Create set YEARS
        # First create the new set name for year and add space for groups and items for this set
        create_set(SetNames, NewSetItems, NewSetGroups, 'YEAR')
        for year in Years:
            # Note: Cannot use the same function as other sets
            #   YEAR does not have a 'name' field. MoManI crashes!!!
            NewSetItems[SetNames.index('YEAR')].append({'value': year, 'color': '#000000'})

    # Create set EMISSIONS
    # First create the new set name for year and add space for groups and items for this set
    create_set(SetNames, NewSetItems, NewSetGroups, 'EMISSION')
    print("ASR-Probe::#SetNames= {0}; #NewSetItems= {1}; #NewSetGroups= {2}".
            format(range(len(SetNames)), range(len(NewSetItems)), range(len(NewSetGroups))))
    for n in range(len(SetNames)):
        print("SetNames[{0:1d}]= {1}" .format(n, SetNames[n]))

    for n in range(len(NewSetItems)):
        print("NewSetItems[{0:1d}]= {1}" .format(n, NewSetItems[n]))

    for n in range(len(NewSetGroups)):
        print("NewSetGroups[{0:1d}]= {1}" .format(n, NewSetGroups[n]))

    for emission in Emissions:
        Fill_Set(NewSetItems, SetNames, "EMISSION", emission, Emissions[emission][1], Emissions[emission][0])
    for n in range(len(SetNames)):
        print("ASR-Probe::Filled Set {0}..." .format(SetNames[n]))
        for m in range(len(NewSetItems)):
            print("SetNames[{0:1d}]= {x}::NewSetItems[{1:1d}]= {y}"
                    .format(n, m, x=SetNames[n], y=NewSetItems[m]))
            print("\tidx_val= {0}; Emissions[]= {1} {2}"
                    .format(emission, Emissions[emission][1], Emissions[emission][0]))
        print("--------------------------------\n")

    if OutputFormat != 'append_otoole':
        # Create set TIMESLICE
        # First create the new set name for year and add space for groups and items for this set
        create_set(SetNames, NewSetItems, NewSetGroups, 'TIMESLICE')
        for timeslice in Timeslices:
            Fill_Set(NewSetItems, SetNames, "TIMESLICE",
                    timeslice, Timeslices[timeslice][1], Timeslices[timeslice][0])

    # Create set REGION
    # First create the new set name for year and add space for groups and items for this set
    create_set(SetNames, NewSetItems, NewSetGroups, 'REGION')
    for Region in Regions:
        print("ASR-Probe::Region {0}..." .format(Region))
        if OutputFormat != 'append_otoole':
            Fill_Set(NewSetItems, SetNames, "REGION", Region, Regions[Region][1], Regions[Region][0])

    # Create empty set TECHNOLOGY
    create_set(SetNames, NewSetItems, NewSetGroups, 'TECHNOLOGY')

    # Create empty set COMMODITY
    create_set(SetNames, NewSetItems, NewSetGroups, 'COMMODITY')

    # Create sectoral demand technologies
    for sector in EndUseFuels:
        for fuel in EndUseFuels[sector]:
            # Create the demand fuel:
            Fill_Set(NewSetItems, SetNames, "COMMODITY", sector + fuel, "#000000", "")
            # Create the demand technology
            Fill_Set(NewSetItems, SetNames, "TECHNOLOGY",
                    "DEM" + sector + fuel, "#000000", "Demand technology for ")
            # Create the input fuel (if it doesn't exist)
            if not fuel in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
                if OutputFormat == 'append_otoole':
                    if not fuel[0:3] == "ELC":
                        Fill_Set(NewSetItems, SetNames, "COMMODITY", fuel, "#000000", "")
                else:
                    Fill_Set(NewSetItems, SetNames, "COMMODITY", fuel, "#000000", "")

            # Create the input and output activity for that combination:
            AddActivityListItems(Years, Region, "DEM" + sector + fuel, sector + fuel, OARList, value = "1")
            AddActivityListItems(Years, Region, "DEM" + sector + fuel, fuel, IARList, value = "1")

    for powerplant in PowerPlants:
        if not powerplant[3:6] in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
            Fill_Set(NewSetItems, SetNames, "COMMODITY", powerplant[3:6], "#000000", "")
        if not "PWR" + powerplant[3:6] in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
            Fill_Set(NewSetItems, SetNames, "COMMODITY", "PWR" + powerplant[3:6], "#000000", "")

            AddActivityListItems(Years, Region, "DEMPWR" + powerplant[3:6], powerplant[3:6], IARList, value = "1")
            AddActivityListItems(Years, Region, "DEMPWR" + powerplant[3:6], "PWR" + powerplant[3:6], OARList, value = "1")
        if not "DEMPWR" + powerplant[3:6] in [li['value'] for li in NewSetItems[SetNames.index("TECHNOLOGY")]]:
            Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "DEMPWR" + powerplant[3:6], "#000000", "")

        # Create ELC001 commodity if not already created.  But do this per land region (using the first character of the last three digits of the power plant as the key):
        if not "ELC" + powerplant[6:7] + "01" in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
            Fill_Set(NewSetItems, SetNames, "COMMODITY", "ELC" + powerplant[6:7] + "01", "#000000", "")
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", powerplant, "#000000", PowerPlants[powerplant][0])

        AddActivityListItems(Years, Region, powerplant, "PWR" + powerplant[3:6], IARList, value = str(PowerPlants[powerplant][1]),
                v = str(PowerPlants[powerplant][1]))
        AddActivityListItems(Years, Region, powerplant, "ELC" + powerplant[6:7] + "01", OARList, value = "1")

        # Create input surface water.
        LandRegion = [k for k, v in LandToGridMap.items() if v == powerplant[6:7]][0]
        if not "DEMPWRSUR" + LandRegion in [li['value'] for li in NewSetItems[SetNames.index("TECHNOLOGY")]]:
            Fill_Set(NewSetItems, SetNames, "TECHNOLOGY","DEMPWRSUR" + LandRegion,
            "#000000",  "", "Surface water demand for power in " + LandRegion)
        if not "PWRWAT" + LandRegion in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
            Fill_Set(NewSetItems, SetNames, "COMMODITY","PWRWAT" + LandRegion,
            "#000000",  "", "Surface water demand for power in " + LandRegion)

            AddActivityListItems(Years, Region, "DEMPWRSUR" + LandRegion, "WTRSUR" + LandRegion, IARList, value = "1")
            AddActivityListItems(Years, Region, "DEMPWRSUR" + LandRegion, "PWRWAT" + LandRegion, OARList, value = "1")

        AddActivityListItems(Years, Region, powerplant, "PWRWAT" + LandRegion, IARList, value = str(PowerPlants[powerplant][2]),
                v = str(PowerPlants[powerplant][2]))
        AddActivityListItems(Years, Region, powerplant, "WTRSUR" + LandRegion, OARList, value = str(PowerPlants[powerplant][3]),
                v = str(PowerPlants[powerplant][3]))

    # Create import fuels
    for fuel in ImportFuels:
        if not fuel in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
            print("")
            print("\x1b[0;30;41mWarning:  Import fuel " + fuel + " created for fuel that is not used in any sector.\x1b[0m")
            print("")
            Fill_Set(NewSetItems, SetNames, "COMMODITY", fuel, "#000000",  "")
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "IMP" + fuel, "#000000",  "")
        AddActivityListItems(Years, Region, "IMP" + fuel, fuel, OARList, value = "1")

    # Create domestic supply of fuels
    for fuel in DomesticMining:
        if not fuel in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
            print("")
            print(
                "\x1b[0;30;41mWarning:  Mining of fuel " + fuel + " created for fuel that is not used in any sector.\x1b[0m")
            print("")
            Fill_Set(NewSetItems, SetNames, "COMMODITY", fuel, "#000000",  "")
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "MIN" + fuel, "#000000",  "")
        AddActivityListItems(Years, Region, "MIN" + fuel, fuel, OARList, value = "1")

    # Create domestic supply of renewables
    for fuel in DomesticRenewables:
        if not fuel in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
            print("")
            print(
                "\x1b[0;30;41mWarning:  Renewable fuel " + fuel + " created for fuel that is not used in any sector.\x1b[0m")
            print("")
            Fill_Set(NewSetItems, SetNames, "COMMODITY", fuel, "#000000",  "")
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "RNW" + fuel, "#000000",  "")
        AddActivityListItems(Years, Region, "RNW" + fuel, fuel, OARList, value = "1")

    # Create export fuels
    for fuel in ExportFuels:
        if not fuel in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
            print("")
            print(
                "\x1b[0;30;41mWarning:  Export fuel " + fuel + " created for fuel that is not used/produced in any sector.\x1b[0m")
            print("")
            Fill_Set(NewSetItems, SetNames, "COMMODITY", fuel, "#000000",  "")
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "EXP" + fuel, "#000000",  "")
        AddActivityListItems(Years, Region, "EXP" + fuel, fuel, IARList, value = "1")

    ################################################
    # AGRICULTURAL TECHNOLOGIES, FUELS AND Input Activity Ratio (IAR)/Output Activity Ratio (OAR)
    ################################################
    # Create groups for sets to track commodities, technologies
    # Don't need groups for these for agriculture - can add later if needed...
    # Make all set colour black for the time being - can change later if needed...
    CropList = {}
    CropNumber = 1
    CropComboList = {}
    ModeList = []
    ModeNumber = 1

    Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "MINLND" + "TOT", "#000000", "Land suuply technology.")
    Fill_Set(NewSetItems, SetNames, "COMMODITY", "L" + "TOT", "#000000", "Land resource.")
    AddActivityListItems(Years, Region, "MINLND" + "TOT", "L" + "TOT", OARList, value = "1")

    for LandRegion in LandRegions:
        ###############################
        # Inputs for agricultural groundwater and electricity for pumping:
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "DEMAGRGWT" + LandRegion, "#000000", "Agricultural groundwater supply.")
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "DEMAGRSUR" + LandRegion, "#000000", "Agricultural groundwater supply.")
        Fill_Set(NewSetItems, SetNames, "COMMODITY", "AGRWAT" + LandRegion, "#000000", "Agricultural water for irrigation.")
        Fill_Set(NewSetItems, SetNames, "COMMODITY", "WTREVT" + LandRegion, "#000000", "Water lost to evapotranspiration.")
        Fill_Set(NewSetItems, SetNames, "COMMODITY", "WTRGRC" + LandRegion, "#000000", "Water lost to evapotranspiration.")
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "DEMPUBGWT" + LandRegion, "#000000", "Agricultural water for irrigation.")
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "DEMPUBSUR" + LandRegion, "#000000", "Agricultural water for irrigation.")
        Fill_Set(NewSetItems, SetNames, "COMMODITY", "PUBWAT" + LandRegion, "#000000", "Water lost to evapotranspiration.")

        # Creation of agricultural water supply from grownwater
        # 1.73 number taken from Bolivia - Should be 0.0173
        # NEED TO ADJUST THE IAR TO MATCH THE CORRECT VALUE FOR THE DEMAGRGWT...
        AddActivityListItems(Years, Region, "DEMAGRGWT" + LandRegion, "AGRELC" + LandToGridMap[LandRegion] + "02", IARList, value = "0.0173",
                v = "0.0173")

        # for year in Years:
        # Sets = [Region, "DEMAGRGWT"+LandRegion, "WTRGWT"+LandRegion, "1", year]
        # Value = "1"
        # Item = {"c":Sets, "v":Value}
        # IARList.append(Item)
        AddActivityListItems(Years, Region, "DEMAGRGWT" + LandRegion, "AGRWAT" + LandRegion, OARList, value = "1")

        # Creation of agricultural water supply from surface water
        # for year in Years:
        # Sets = [Region, "DEMAGRSUR"+LandRegion, "AGRELC"+LandToGridMap[LandRegion], "1", year]
        # Value = "0.0173"
        # # 1.73 number taken from Bolivia
        # # NEED TO ADJUST THE IAR TO MATCH THE CORRECT VALUE FOR THE DEMAGRGWT...
        # Item = {"c":Sets, "v":Value}
        # IARList.append(Item)
        AddActivityListItems(Years, Region, "DEMAGRSUR" + LandRegion, "WTRSUR" + LandRegion, IARList, value = "1")
        AddActivityListItems(Years, Region, "DEMAGRSUR" + LandRegion, "AGRWAT" + LandRegion, OARList, value = "1")

        # Creation of public water supply from surface water
        # for year in Years:
        # Sets = [Region, "DEMPUBSUR"+LandRegion, "COMELC"+LandToGridMap[LandRegion], "1", year]
        # Value = "0.0173"
        # # 1.73 number taken from Bolivia
        # # NEED TO ADJUST THE IAR TO MATCH THE CORRECT VALUE FOR THE DEMAGRGWT...
        # Item = {"c":Sets, "v":Value}
        # IARList.append(Item)
        AddActivityListItems(Years, Region, "DEMPUBSUR" + LandRegion, "WTRSUR" + LandRegion, IARList, value = "1")
        AddActivityListItems(Years, Region, "DEMPUBSUR" + LandRegion, "PUBWAT" + LandRegion, OARList, value = "1")

        # Creation of public water supply from groundwater water
        # 1.73 number taken from Bolivia
        # NEED TO ADJUST THE IAR TO MATCH THE CORRECT VALUE FOR THE DEMAGRGWT...
        AddActivityListItems(Years, Region, "DEMPUBGWT" + LandRegion, "COMELC" + LandToGridMap[LandRegion] + "02", IARList, value = "0.0173",
                v = "0.0173")

        # for year in Years:
        # Sets = [Region, "DEMPUBGWT"+LandRegion, "WTRGWT"+LandRegion, "1", year]
        # Value = "1"
        # Item = {"c":Sets, "v":Value}
        # IARList.append(Item)
        AddActivityListItems(Years, Region, "DEMPUBGWT" + LandRegion, "PUBWAT" + LandRegion, OARList, value = "1")

        ############################################
        # Precipitation sources
        Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "MINPRC" + LandRegion, "#000000", "Agricultural groundwater supply.")
        Fill_Set(NewSetItems, SetNames, "COMMODITY", "WTRPRC" + LandRegion, "#000000", "Agricultural water for irrigation.")
        AddActivityListItems(Years, Region, "MINPRC" + LandRegion, "WTRPRC" + LandRegion, OARList, value = "1")

        ###############################
        # Groundwater sources
        # NewSetItems[SetNames.index("TECHNOLOGY")].append({"value":"MINGWT"+LandRegion, "name":"Agricultural groundwater supply.", "color":"#000000"})
        # NewSetItems[SetNames.index("COMMODITY")].append({"value":"WTRGWT"+LandRegion, "name":"Agricultural water for irrigation.", "color":"#000000"})
        # for year in Years:
        # Sets = [Region, "MINGWT"+LandRegion, "WTRGWT"+LandRegion, "1", year]
        # Value = "1"
        # Item = {"c":Sets, "v":Value}
        # OARList.append(Item)    ###############################
        # Surfce water sources
        #    NewSetItems[SetNames.index("TECHNOLOGY")].append({"value":"MINSUR"+LandRegion, "name":"Agricultural groundwater supply.", "color":"#000000"})
        Fill_Set(NewSetItems, SetNames, "COMMODITY", "WTRSUR" + LandRegion, "#000000", "Agricultural water for irrigation.")
        #    for year in Years:
        #        Sets = [Region, "MINSUR"+LandRegion, "WTRSUR"+LandRegion, "1", year]
        #        Value = "1"
        #        Item = {"c":Sets, "v":Value}
        #        OARList.append(Item)    ###############################
        # Land resource
        # Moved to outside for loop:
        # Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "MINLND" + "TOT", "#000000", "Land suuply technology.")
        # Fill_Set(NewSetItems, SetNames, "COMMODITY", "L" + "TOT", "#000000", "Land resource.")
        # AddActivityListItems(Years, Region, "MINLND" + "TOT", "L" + "TOT", OARList, value = "1")

        ###############################
        # Cluster specific technologies for different crops, etc...
        Clusters = open(os.path.join(DataDirectoryName, ClusterBaseFileName + LandRegion + '.csv'), 'r').readlines()
        PrecipitationClusters = open(os.path.join(DataDirectoryName, PrecipitationClusterBaseFileName + LandRegion + '.csv'),
                                     'r').readlines()
        EvapotranspirationClusters = open(os.path.join(DataDirectoryName, EvapotranspirationClusterBaseFileName + LandRegion + '.csv'),
                                          'r').readlines()
        IrrigationWaterDeficitClusters = open(
            os.path.join(DataDirectoryName, IrrigationWaterDeficitClusterBaseFileName + LandRegion + '.csv'), 'r').readlines()

        # Create list of crops (or add crops to list), intensities, technology
        for Combo in Clusters[0].split(",")[10:]:
            Crop = ' '.join(Combo.split(' ')[:-2])
            IrrigationType = Combo.split(' ')[-2][0]
            Intensity = Combo.split(' ')[-1][0]
            # We have a crop combination.  We need to check if we have the crop already, and if not add a new crop.
            if Crop in CropList:  # We have already dealt with this crop in another situation...
                CropCode = CropList[Crop]
            else:
                CropCode = Crop
                CropNumber = CropNumber + 1
                CropList[Crop] = CropCode
                # And create the crop commodity for final output:
                Fill_Set(NewSetItems, SetNames, "COMMODITY", "CRP" + CropCode, "#000000", Crop)
            # And then we need to check if we have the combination already, and if not add it to the list.
            if CropCode + Intensity + IrrigationType in CropComboList:
                CropCombo = CropComboList[CropCode + Intensity + IrrigationType]
            else:
                # We don't have this one yet:
                CropCombo = CropCode + Intensity + IrrigationType
                CropComboList[CropCode + Intensity + IrrigationType] = CropCombo
                ModeList.append(CropCombo)
                ModeNumber = ModeNumber + 1
                # And add the links in for this technology to the land
                Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "LND" + CropCombo + "TOT", "#000000",
                "Land resource technology for crop combo " + Combo)
                Fill_Set(NewSetItems, SetNames, "COMMODITY", "L" + CropCombo + "TOT", "#000000",
                "Land resource commodity for crop combo " + Combo)
                AddActivityListItems(Years, Region, "LND" + CropCombo + "TOT", "L" + "TOT", IARList, value = "1")
                AddActivityListItems(Years, Region, "LND" + CropCombo + "TOT", "L" + CropCombo + "TOT", OARList, value = "1")

        # Crops and land tracking commodities have been created.  Now create land technologies to connect them together.
        for clustercount in range(1, len(Clusters)):
            # Add the agricultural land use technologies
            Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "LNDAGR" + LandRegion + "C" + Clusters[clustercount].split(',')[0].zfill(2),
            "#000000","Land resource in " + LandRegion + ".")
            # And add a mode for each crop combination and create the IAR and OAR
            for mode, modeCombo in enumerate(ModeList):
                # Add the IAR for the combo into the correct mode.
                AddActivityListItems(Years, Region, "LNDAGR" + LandRegion + "C" + Clusters[clustercount].split(',')[0].zfill(2),
                "L" + modeCombo + "TOT", IARList, value = "1",  g = str(mode + 1))

                # And add the OAR for the output crop:
                # Lookup the OAR from the cluster data:
                for CropCode2, cropcombo2 in CropList.items():
                    if modeCombo[:-2] == cropcombo2:
                        # IAR for Precipitation - Should only be entered if the combination exists
                        PrecipitationValue = float(PrecipitationClusters[clustercount].split(',')[
                                                       1])  # Precipitation values are constant across all technologies/crops in a region.
                        PrecipitationValue = format(ctx.create_decimal(repr(PrecipitationValue)), 'f')

                        AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + PrecipitationClusters[clustercount].split(',')[0].zfill(2),
                        "WTRPRC" + LandRegion, IARList, g = str(mode + 1), v = str(PrecipitationValue))

                        # Find the right OAR for this technology and put it into the OAR list:

                        CropComboLabel = CropCode2 + " " + IrrigationTypeList[modeCombo[-1]] + " " + IntensityList[
                            modeCombo[-2]]
                        Location = Clusters[0].strip().split(',').index(CropComboLabel)
                        Value = float(Clusters[clustercount].split(',')[Location]) * CropYieldFactors[CropComboLabel[0:3]]
                        Value = format(ctx.create_decimal(repr(Value)), 'f')

                        AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + Clusters[clustercount].split(',')[0].zfill(2),
                        "CRP" + modeCombo[:-2], OARList, g = str(mode + 1), v = str(Value))

                        # IAR for Irrigation
                        Location = IrrigationWaterDeficitClusters[0].strip().split(',').index(CropComboLabel)
                        IrrigationValue = float(IrrigationWaterDeficitClusters[clustercount].split(',')[Location])
                        if IrrigationTypeList[modeCombo[-1]] == 'Rain-fed':
                            IrrigationValue = 0.
                        IrrigationValue = format(ctx.create_decimal(repr(IrrigationValue)), 'f')
                        if float(
                                IrrigationValue) < 0.0001:  # fix to prevent scientific e-8 numbers from breaking the system.
                            IrrigationValue = '0'

                        AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + IrrigationWaterDeficitClusters[clustercount].split(',')[0].zfill(2),
                        "AGRWAT" + LandRegion, IARList, g = str(mode + 1), v = str(IrrigationValue))

                        # OAR for Evapotranspiration
                        Location = EvapotranspirationClusters[0].strip().split(',').index(CropComboLabel)
                        EvapotranspirationValue = float(EvapotranspirationClusters[clustercount].split(',')[Location])
                        EvapotranspirationValue = format(ctx.create_decimal(repr(EvapotranspirationValue)), 'f')
                        # print(CropComboLabel+" "+line.split(',')[0] + " " + Value)
                        # print(str(mode)+" "+modeCombo+ " "+CropCode2+ " "+cropcombo2)

                        AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + EvapotranspirationClusters[clustercount].split(',')[0].zfill(2),
                        "WTREVT" + LandRegion, OARList, g = str(mode + 1), v = str(EvapotranspirationValue))

                        # OAR for Groundwater
                        GroundwaterValue = (float(PrecipitationValue) + float(IrrigationValue) - float(
                            EvapotranspirationValue)) * GroundwaterPercentofExcess
                        GroundwaterValue = format(ctx.create_decimal(repr(GroundwaterValue)), 'f')
                        RunoffValue = (float(PrecipitationValue) + float(IrrigationValue) - float(
                            EvapotranspirationValue)) * (1 - GroundwaterPercentofExcess)
                        RunoffValue = format(ctx.create_decimal(repr(RunoffValue)), 'f')

                        AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + EvapotranspirationClusters[clustercount].split(',')[0].zfill(2),
                        "WTRGRC" + LandRegion, OARList, g = str(mode + 1), v = str(GroundwaterValue))

                        # OAR for Runoff
                        AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + EvapotranspirationClusters[clustercount].split(',')[0].zfill(2),
                        "WTRSUR" + LandRegion, OARList, g = str(mode + 1), v = str(RunoffValue))

    # Need a new for loop so we don't add the IAR values for the last few modes to the IAR and OAR above...
    for LandRegion in LandRegions:
        # ADD LAST FEW MODES, AND IAR FOR THEM IN LNDAGR technologies
        for LandUseCode, LandUse in LandUseCodes.items():
            if LandUse in ModeList:
                ModeNum = ModeList.index(LandUse)
                # Mode exists, use this one...
                # print(str(ModeNum)+LandUse+ModeList[ModeNum])
            else:
                # Mode doesn't exist, create new mode.
                ModeList.append(LandUse)
                ModeNum = ModeNumber - 1
                ModeNumber = ModeNumber + 1
                # print(str(ModeNum)+LandUse+ModeList[ModeNum])
                # print(str(ModeNum)+LandUse+ModeList[ModeNum])
                # Now add the land use sets, IAR and OAR to connect to the LNDAGR technologies...
                Fill_Set(NewSetItems, SetNames, "TECHNOLOGY", "LND" + LandUseCode + "TOT", "#000000", LandUse + " technology in " + "TOT" + ".")
                Fill_Set(NewSetItems, SetNames, "COMMODITY", "L" + LandUseCode + "TOT", "#000000", LandUse + " commodity in " + "TOT" + ".")

                AddActivityListItems(Years, Region, "LND" + LandUseCode + "TOT", "L" + "TOT", IARList, value = "1")

                AddActivityListItems(Years, Region, "LND" + LandUseCode + "TOT", "L" + LandUseCode + "TOT", OARList, value = "1")

            for line in Clusters[1:]:  # Have to have the output for all lines...
                # LSOU becomes LNDFORSOU, etc. in specified mode
                AddActivityListItems(Years, Region, "LNDAGR" + LandRegion + "C" + line.split(',')[0].zfill(2),
                "L" + LandUseCode + "TOT", IARList, value = "1", g = str(ModeNum + 1)) # print(Sets)

                # Now add precipitation and water balance inputs and outputs
                PrecipitationValue = float(PrecipitationClusters[int(line.split(',')[0])].split(',')[
                                               1])  # Precipitation values are constant across all technologies/crops in a region.
                PrecipitationValue = format(ctx.create_decimal(repr(PrecipitationValue)), 'f')

                AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + line.split(',')[0].zfill(2),
                        "WTRPRC" + LandRegion, IARList, g = str(ModeNum + 1), v = str(PrecipitationValue))

                # IAR for Irrigation doesn't exist - there is no irrigation for these technologies as they are not agricultural.
                # OAR for Evapotranspiration
                EvapotranspirationValue = float(PrecipitationValue) * EvapotranspirationPercentPRCOtherLandUse[LandUseCode]
                EvapotranspirationValue = format(ctx.create_decimal(repr(EvapotranspirationValue)), 'f')
                # print(CropComboLabel+" "+line.split(',')[0] + " " + Value)
                # print(str(mode)+" "+modeCombo+ " "+CropCode2+ " "+cropcombo2)

                AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + line.split(',')[0].zfill(2),
                        "WTREVT" + LandRegion, OARList, g = str(ModeNum + 1), v = str(EvapotranspirationValue))

                # OAR for Groundwater
                GroundwaterValue = (float(PrecipitationValue) - float(EvapotranspirationValue)) * \
                                   GroundwaterPercentofExcessOtherLandUse[LandUseCode]
                GroundwaterValue = format(ctx.create_decimal(repr(GroundwaterValue)), 'f')
                RunoffValue = (float(PrecipitationValue) - float(EvapotranspirationValue)) * (
                            1 - GroundwaterPercentofExcessOtherLandUse[LandUseCode])
                RunoffValue = format(ctx.create_decimal(repr(RunoffValue)), 'f')

                AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + line.split(',')[0].zfill(2),
                        "WTRGRC" + LandRegion, OARList, g = str(ModeNum + 1), v = str(GroundwaterValue))

                # OAR for Runoff
                AddActivityListItems(Years, Region,
                        "LNDAGR" + LandRegion + "C" + line.split(',')[0].zfill(2),
                        "WTRSUR" + LandRegion, OARList, g = str(ModeNum + 1), v = str(RunoffValue))

    # Add in the transformation technologies
    for transformationtech in TransformationTechnologies:
        # Create the technology if it does not exist:
        if not transformationtech[0] in [li['value'] for li in NewSetItems[SetNames.index("TECHNOLOGY")]]:
            NewSetItems[SetNames.index("TECHNOLOGY")].append(
                {"value": transformationtech[0], "name": transformationtech[5], "color": "#000000"})

        # Create the fuel and the IAR (if there is one specified)
        if transformationtech[1] != '':
            # Create the fuel if it doesn't already exist
            if not transformationtech[1] in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
                NewSetItems[SetNames.index("COMMODITY")].append(
                    {"value": transformationtech[1], "name":'', "color": "#000000"})
                print("")
                print(
                    "\x1b[0;30;41mWarning:  Fuel " + transformationtech[1] + " created for transformation tech "+transformationtech[0]+".\x1b[0m")
                print("")
            # Add the IAR
            AddActivityListItems(Years, Region, transformationtech[0], transformationtech[1], IARList, value = str(transformationtech[2]),
                g = transformationtech[6], v = str(transformationtech[2]))
        # Create the fuel and the OAR (if there is one specified)
        if transformationtech[3] != '':
            # Create the commodity if it doesn't already exist
            if not transformationtech[3] in [li['value'] for li in NewSetItems[SetNames.index("COMMODITY")]]:
                NewSetItems[SetNames.index("COMMODITY")].append(
                    {"value": transformationtech[3], "name": '', "color": "#000000"})
                print("")
                print(
                    "\x1b[0;30;41mWarning:  Fuel " + transformationtech[3] + " created for transformation tech "+transformationtech[0]+".\x1b[0m")
                print("")
            # Add the OAR
            AddActivityListItems(Years, Region, transformationtech[0], transformationtech[3], OARList, value = str(transformationtech[4]),
                g = transformationtech[6], v = str(transformationtech[4]))

    ################################################
    # CREATE MODES OF OPERATION
    SetNames.append("MODE_OF_OPERATION")
    NewSetItems.append([])
    NewSetGroups.append([])
    print("ASR-Probe::Generating MODE_OF_OPERATION @{0}" .format(OperationModesOut))
    for index, Mode in enumerate(ModeList):
        Fill_Set(NewSetItems, SetNames, "MODE_OF_OPERATION", str(index + 1), "#000000", Mode)
    if not os.path.exists(OperationModesOut):
        dataout_dir=os.path.dirname(OperationModesOut)
        print("Creating dataout_dir= {0}" .format(dataout_dir))
        os.makedirs(dataout_dir)
    with open(OperationModesOut, 'w') as ModeFile:
        ModeFile.write(str(ModeList))

    ################################################
    # Residual Capacity dataframe- PWR techs & reduce dataframe linearly vs. cutoff at 2025
    def print_resdlcap():
        for n in range(len(ResidCapList)):
            print("ResidCapList[{0:1d}]= {1};\t" .format(n, ResidCapList[n]))
        print('\n')

    # ASR-TODO: Delete 'print_sagri_rsdl_capacity()' after studying collections.OrderedDict(sorted(...))
    def print_sagri_rsdl_capacity():
#        for item in SAgriculturalResidualCapacity:
#            print(item)
        print("ASR-Probe::sorted(AgriculturalResidualCapacity)= {0}; AgriculturalResidualCapacity['MZEHRBC']= {1}"
                .format(sorted(AgriculturalResidualCapacity), AgriculturalResidualCapacity['MZEHRBC']))
        for n in range(len(SAgriculturalResidualCapacity)):
            print("ASR-Probe::n= {0}; SAgriculturalResidualCapacity[n]= {1}; AgriculturalResidualCapacity[SAgriculturalResidualCapacity[n]]= {2}"
                    .format(n, SAgriculturalResidualCapacity[n], AgriculturalResidualCapacity[SAgriculturalResidualCapacity[n]]))
        print('\n')

    # ASR-TODO: Delete ASR-Probe after studying collections.OrderedDict(sorted(...))
    SAgriculturalResidualCap = collections.OrderedDict(sorted(AgriculturalResidualCapacity.items()))
    print("ASR-Probe::AgriculturalResidualCapacityRetirementYears= {0}"
            "\n\tAgriculturalResidualCapacity= {1};"
            "\n\tAgriculturalResidualCapacity.items()= {2}"
            "\n\tsorted(AgriculturalResidualCapacity)= {3}"
            "\n\tSAgriculturalResidualCapacity= {4};"
            "\n\tSAgriculturalResidualCap= {5};"
            "\n\tYearsN= {6}"
            .format(AgriculturalResidualCapacityRetirementYears, AgriculturalResidualCapacity,
                AgriculturalResidualCapacity.items(), sorted(AgriculturalResidualCapacity),
                SAgriculturalResidualCapacity, SAgriculturalResidualCap, YearsN))
#    print_sagri_rsdl_capacity()

    for n in range(len(SAgriculturalResidualCapacity)):
        cropagri_key = SAgriculturalResidualCapacity[n]
        cropagri_val = AgriculturalResidualCapacity[SAgriculturalResidualCapacity[n]]
        print("ASR-Probe::n= {0}; cropagri_key == SAgriculturalResidualCapacity[n]= {1};"
            "\n\tcropagri_val == AgriculturalResidualCapacity[SAgriculturalResidualCapacity[n]]= {2}"
                .format(n, cropagri_key, cropagri_val))
        for year in YearsN:
            RemainingYears = AgriculturalResidualCapacityRetirementYears - (year - min(YearsN))
            if RemainingYears > 0:
                ResCap = cropagri_val * float(RemainingYears)/(float(AgriculturalResidualCapacityRetirementYears))
                ResidCapList.append([Region, "LND" + cropagri_key, str(year), ResCap])
    print_resdlcap()
    sys.exit("ASR-Probe::Exit Residual Capacity dataframe...")

    ############################################
    # Remove any 0's from IAR and OAR #
    for i, dic in enumerate(IARList):
        if float(dic['v']) == float('0'):
            IARList.pop(i)

    for i, dic in enumerate(OARList):
        if float(dic['v']) == float('0'):
            OARList.pop(i)

    ################################################
    # Create Model Output Files
    # UPDATE MOMANI WITH NEW DATA #
    if OutputFormat == 'MoManI':
        print("Updating MoManI with new data...")
        UpdateMoManI(Model, SetNames, NewSetItems, NewSetGroups, IARList, OARList)

    # OUTPUT TO OTOOLE FORMAT #
    if OutputFormat == 'otoole':
        print("Outputting data in otoole compatible format...")
        Updateotoole(SetNames, NewSetItems, IARList, OARList, otooleOutputDirectory)

    if OutputFormat == 'append_otoole':
        Appendotoole(SetNames, NewSetItems, IARList, OARList, otooleOutputDirectory, OsemosysGlobalPath)

################################################################################
# Main function::Calls Build CLEWs Model
################################################################
def main():
    import argparse, yaml
    ##########
    # For handling unintentional boolean operators from yaml file
    from yaml.constructor import Constructor
    def add_bool(self, node):
        return self.construct_scalar(node)
    yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:bool', add_bool)
    ##########
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Location of YAML file that describes the CLEWs model structure.")
    args = parser.parse_args()
    if args.file:
        with open(args.file, "r") as file_descriptor:
            data = yaml.safe_load(file_descriptor)
        BuildCLEWsModel(data, args.file)

################################################################################
# Function to build CLI arguments
################################################################
def build(args):
    import yaml, os
    if args.yamlfile:
        with open(os.path.join(os.getcwd(), args.yamlfile), "r") as file_descriptor:
            data = yaml.safe_load(file_descriptor)
        BuildCLEWsModel(data, args.file)

################################################################################
# clewsy runtime interface
################################################################
if __name__ == "__main__":
    import logging
    import sys
    logging.basicConfig(level=logging.DEBUG)
    print("ASR-Probe::IDX1B- Got here...")
    param = sys.argv[1]
    print("ASR-Probe::param= {0}..." .format(param))
    if param != "build":
        print("ASR-Probe::model_building local/debug run...")
        main()
    else:
        print("ASR-Probe::model_building distro run...")
        datafile = param
        build(datafile)
