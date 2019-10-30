from py import functions, htmlbase, PIEdataVARS, PieHandler, report
import numpy as np

def main(driver, startdate, enddate, statuslabel):
    locationstruct = PIEdataVARS.locations
    locationstruct.set_enddate(enddate)
    locationstruct.set_startdate(startdate)
    locationstruct.set_maxreturns(100000)
    locationurl = locationstruct.make_url()
    locationframe = PieHandler.goandget(driver, locationurl, locationstruct)
    locationframe['staffed_minutes'] = np.vectorize(functions.getMinutes)(locationframe['assumedDuration-difference'])
    locationframe['abb'] = locationframe['location-shortName'].apply(lambda x: functions.getAbb(x))
    locationframe = locationframe.groupby('abb')['staffed_minutes'].median().reset_index()

    tablelist = [locationframe.to_html()]
    picturelist = []

    outputfile = htmlbase.htmlbase('Stepout Medians', 'Stepout Medians', tablelist, picturelist)
    outputfile.makeHTML('StepoutMedians')

#This is a bad report...make better lol
description = "Just give median stepout times for each lab. Honestly kinda useless. Need to make not trash"
active = True
author = 'Brian Funk'

stepoutreport = report.report('Stepout Report', author,active)
stepoutreport.description = description
stepoutreport.main_run = main