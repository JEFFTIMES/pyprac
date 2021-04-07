import simplyGUI.verySimpleCalculator as simpleCalc
import simplyGUI.demos as demos

"""
    This is the test place to run all the functions in the simpleGUI package 

"""

# call the verySimpleCalc function
simpleCalc.verySimpleCalc()


# call the other functions

import simplyGUI.restrictInput as rsI

rsI.numberInputOnly()

rsI.multilineDemo()

demos.simpleTextInput()

demos.manyCalendars()

demos.fileSelect()

demos.fileCompare()
