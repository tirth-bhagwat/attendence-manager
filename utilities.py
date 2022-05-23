import styles

#######################################################
############### currently useless #####################
#######################################################

def getInput(condition,console=None):
    while condition:
        if console is not None:
            console.print("Invalid class name... Please Retry !!",style=styles.ERROR, justify="CENTER")
        inp = input()
    return inp