
def Find_Quadrant(demo_arr,T_Peak):

    x = demo_arr[0, :]
    y = demo_arr[1, :]
    z = demo_arr[2, :]

    Tx = x[T_Peak]
    Ty = y[T_Peak]
    Tz = z[T_Peak]

    # initialize the quadrant situation to judge position of the point

    XYquadrant = 0
    ZYquadrant = 0
    XZquadrant = 0

    # in X-Y pic
    if(Tx > 0 and Ty > 0):
        XYquadrant = 1
    elif(Tx < 0 and Ty > 0):
        XYquadrant = 2
    elif(Tx < 0 and Ty < 0):
        XYquadrant = 3
    elif (Tx > 0 and Ty < 0):
        XYquadrant = 4
    else:
        XYquadrant = 5

    # in Z-Y pic
    if (Tz > 0 and Ty > 0):
        ZYquadrant = 1
    elif (Tz < 0 and Ty > 0):
        ZYquadrant = 2
    elif (Tz < 0 and Ty < 0):
        ZYquadrant = 3
    elif (Tz > 0 and Ty < 0):
        ZYquadrant = 4
    else:
        ZYquadrant = 5

    # in Y-Z pic
    if (Tx > 0 and Tz > 0):
        XZquadrant = 1
    elif (Tx < 0 and Tz > 0):
        XZquadrant = 2
    elif (Tx < 0 and Tz < 0):
        XZquadrant = 3
    elif (Tx > 0 and Tz < 0):
        XZquadrant = 4
    else:
        XZquadrant = 5

    SAVEPOS = [XYquadrant,ZYquadrant,XZquadrant]

    # situation judgement
    return_judge = ['Unknown', 'Unknown']
    return_judge1 = ['Lateral', 'Inferior']
    return_judge2 = ['Lateral', 'Anterior']
    return_judge3 = ['Anterior', 'Septal']
    return_judge4 = ['Septal', 'Inferior']

    if SAVEPOS[0] ==1 :
        if SAVEPOS[1] == 1:
            return_judge = return_judge1
        elif SAVEPOS[1] == 2:
            return_judge = return_judge2
        elif SAVEPOS[1] == 3:
            return return_judge
        elif SAVEPOS[1] == 4:
            return return_judge
        else:
            return return_judge
    elif SAVEPOS[0] == 2:
        if SAVEPOS[1] == 1:
            return return_judge
        elif SAVEPOS[1] == 2:
            return_judge = return_judge3
        elif SAVEPOS[1] == 3:
            return return_judge
        elif SAVEPOS[1] == 4:
            return return_judge
        else:
            return return_judge
    elif SAVEPOS[0] == 3 :
        if SAVEPOS[1] == 1:
            return return_judge
        elif SAVEPOS[1] == 2:
            return return_judge
        elif SAVEPOS[1] == 3:
            return_judge = return_judge4
        elif SAVEPOS[1] == 4:
            return return_judge
        else:
            return return_judge
    # elif SAVEPOS[0] == 4 :
    #     if SAVEPOS[1] == 1:
    #         return_judge =
    #     elif SAVEPOS[1] == 2:
    #         return_judge =
    #     elif SAVEPOS[1] == 3:
    #         return_judge =
    #     elif SAVEPOS[1] == 4:
    #         return_judge =
    #     else:
    #         return_judge =
    else:
        return return_judge

    return return_judge