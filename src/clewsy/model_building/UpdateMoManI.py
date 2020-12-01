def UpdateMoManI(Model, SetNames, NewSetItems, NewSetGroups, IARList, OARList):

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
