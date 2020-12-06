def Fill_Set(new_set_items, set_names, sets, value1, color1, name1 = '', t = "name"):
    new_set_items[set_names.index(sets)].append(\
    {"value": value1, t: name1, "color": color1})
