# create_set in BuildCLEWsModel.py
def create_set(set_names, new_SetItems, new_setGroups, sets):
    set_names.append(sets)
    new_SetItems.append([])
    new_setGroups.append([])    
        
# func1 in BuildCLEWsModel.py
def AddActivityListItems(year1, region, input1, input2, List, value = None, g = "1", v = "1"):    
    for year in year1:
        Sets = [region, input1, input2, g, year]
        Value = value
        Item = {"c": Sets, "v": v}
        List.append(Item)
