# SeaHorse Project Python Drifter Utilities
import re

def sh_gpxcut2txt(FNIN,FNOUT,TIME1,TIME2):
    """
    reads track data from a garmin gpx file (A*.gpx) 
    and saves only a valid portion between TIME1 and TIME2
    (T*.gpx)
    and also converts to ascii format
    (T*.txt)
    
    example of the gpx file content:
    <trkpt lat="42.24367619" lon="-70.78660727"><ele>0.137</ele><time>2010-08-16T17:32:10Z</time></trkpt>
    
    usage examples:
    sh_gpxcut2txt('A140707_1.gpx','T140707_1.gpx','2014-07-07T17:40:00','2014-07-17T18:05:00')
    sh_gpxcut2txt('A140707_1.gpx','','2014-07-07T17:40:00','2014-07-17T18:05:00')
    """
    
    if FNOUT=='':
        FNOUT='T'+FNIN.lstrip('A')
    
    FNOUTTXT=FNOUT.rstrip('.gpx')+'.txt'

    print('sh_gpxcut2txt ' + FNIN + ' -> ' + FNOUT + ', '+FNOUTTXT)
    print('              ' + TIME1+ ' ' +TIME2)
    
    # read the whole input file
    f=open(FNIN,'r')
    S=f.read() 
    f.close()
    
    # open and write the output file header
    f2=open(FNOUT,'wt');
    S1='<gpx>\n';f2.write(S1)
    S1='<trk>\n';f2.write(S1)
    S1='<trkseg>\n';f2.write(S1)

    # open file to write ascii output
    f2txt=open(FNOUTTXT,'wt');
    
            
    Trkpts=re.findall(r'<trkpt.*?</trkpt>',S,re.S)
    for TRKPT in Trkpts:
        TIME=re.search('(<time.*?</time>)',TRKPT).group()
        TIME=TIME.split('</time>')[0].split('<time>')[1]
        TIME=TIME.rstrip('Z') # Z at the end does not affect comparison
        LAT=re.search('lat=".*?"',TRKPT).group().split('"')[1].strip()
        LON=re.search('lon=".*?"',TRKPT).group().split('"')[1].strip()
        if ((TIME >= TIME1) & (TIME < TIME2)):
            f2.write(TRKPT)
            f2txt.write(TIME+'   '+LAT+'  '+LON+'\n')
    
    # write the output file header and close the file
    S1='</trkseg>\n';f2.write(S1)
    S1='</trk>\n';f2.write(S1)
    S1='</gpx>\n';f2.write(S1)
    f2.close()
    
    f2txt.close()

