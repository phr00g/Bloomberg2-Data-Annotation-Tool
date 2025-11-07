'''
Tools to take stringname of illusion images and break them down to locate their corresponding info in the excel file.

'''

def iden_from_filename(filename:str):
    if filename.endswith(".png"):
        try:
            iden = int(filename[20:-11])
        except:
            print("Broken")
            print(filename)
            return None
    else:
        print("non-png given! returning None!")
        return None
    

    return iden
def view_from_filename(filename:str):
    #gets the view, in dataset its equivalent to view_1 or view_2 so add 1 to it, because originally this is 0 and 1
    iden = int(filename[-5]) + 1
    return iden