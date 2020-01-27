import operator

#Take input line by line
file=open("input.txt","r")
content = file.readlines()
content = [x.strip() for x in content]

#Parse input
beds = [int(content[0])]*7
lots = [int(content[1])]*7
SPLAdaysRequested = [0]*7
LAHSAdaysRequested = [0]*7
assignedLAHSAs = []
assignedLAHSA = int(content[2])
contentPtr = 3
for i in range(assignedLAHSA):
    assignedLAHSAs.append(content[contentPtr])
    contentPtr += 1
assignedSPLAs = []
assignedSPLA = int(content[contentPtr])
contentPtr += 1
for i in range(assignedSPLA):
    assignedSPLAs.append(content[contentPtr])
    contentPtr += 1
totalApplicants = int(content[contentPtr])
applInfo = []
for i in range(totalApplicants):
    contentPtr += 1
    applInfo.append(content[contentPtr])

#Count remaining parking lots and remove applicants who have already been assigned
for i in assignedSPLAs:
    for j in applInfo:
        if(i[0]==j[0] and i[1]==j[1] and i[2]==j[2] and i[3]==j[3] and i[4]==j[4]):
            lots[0] -= int(j[13])
            lots[1] -= int(j[14])
            lots[2] -= int(j[15])
            lots[3] -= int(j[16])
            lots[4] -= int(j[17])
            lots[5] -= int(j[18])
            lots[6] -= int(j[19])
            applInfo.remove(j)


#Count remaining beds and remove applicants who have already been assigned
for i in assignedLAHSAs:
    for j in applInfo:
        if(i[0]==j[0] and i[1]==j[1] and i[2]==j[2] and i[3]==j[3] and i[4]==j[4]):
            beds[0] -= int(j[13])
            beds[1] -= int(j[14])
            beds[2] -= int(j[15])
            beds[3] -= int(j[16])
            beds[4] -= int(j[17])
            beds[5] -= int(j[18])
            beds[6] -= int(j[19])
            applInfo.remove(j)

#Assigning applicants who can be taken by SPLA
remSPLA = []
for i in applInfo:
    if(i[10]=='N' and i[11]=='Y' and i[12]=='Y'):
        remSPLA.append(i)

#Assigning applicants who can be taken by LAHSA
remLAHSA = []
for i in applInfo:
    if(i[5]=='F' and ((100*int(i[6]))+(10*int(i[7]))+int(i[8]))>17 and i[9]=='N'):
        remLAHSA.append(i)

#Dictionary for SPLA, maintaining total value for SPLA applicants
SPLAdict = {}
SPLAtotal = 0
for i in remSPLA:
    SPLAdict[i] = int(i[13])+int(i[14])+int(i[15])+int(i[16])+int(i[17])+int(i[18])+int(i[19])
    SPLAtotal += SPLAdict[i]
    SPLAdaysRequested[0] += int(i[13])
    SPLAdaysRequested[1] += int(i[14])
    SPLAdaysRequested[2] += int(i[15])
    SPLAdaysRequested[3] += int(i[16])
    SPLAdaysRequested[4] += int(i[17])
    SPLAdaysRequested[5] += int(i[18])
    SPLAdaysRequested[6] += int(i[19])

#Dictionary for LAHSA, maintaining total value for LAHSA applicants
LAHSAdict = {}
LAHSAtotal = 0
for i in remLAHSA:
    LAHSAdict[i] = int(i[13])+int(i[14])+int(i[15])+int(i[16])+int(i[17])+int(i[18])+int(i[19])
    LAHSAtotal += LAHSAdict[i]
    LAHSAdaysRequested[0] += int(i[13])
    LAHSAdaysRequested[1] += int(i[14])
    LAHSAdaysRequested[2] += int(i[15])
    LAHSAdaysRequested[3] += int(i[16])
    LAHSAdaysRequested[4] += int(i[17])
    LAHSAdaysRequested[5] += int(i[18])
    LAHSAdaysRequested[6] += int(i[19])


#Create SPLA conflict dictionary
SPLAconflict = {}
for i in remSPLA:
    SPLAconflict[i] = 0

for i,j in zip(range(0,7),range(13,20)):
    if(SPLAdaysRequested[i]>lots[i]):
        for k in remSPLA:
            for l in remSPLA:
                if(l!=k and k[j]=='1' and l[j]=='1'):
                    SPLAconflict[k] += 1

#Create LAHSA conflict dictionary
LAHSAconflict = {}
for i in remLAHSA:
    LAHSAconflict[i] = 0

for i,j in zip(range(0,7),range(13,20)):
    if(LAHSAdaysRequested[i]>beds[i]):
        for k in remLAHSA:
            for l in remLAHSA:
                if(l!=k and k[j]=='1' and l[j]=='1'):
                    LAHSAconflict[k] += 1

#Remove SPLA applicants with conflicts
maxSPLAconflict = max(SPLAconflict.iteritems(), key=operator.itemgetter(1))[1]
while(maxSPLAconflict>0):
    #Get applicants with this max value
    maxSPLApeople = [k for k,v in SPLAconflict.iteritems() if v==maxSPLAconflict]
    #Check if their request value is greater than total value
    for i in maxSPLApeople:
        if(SPLAdict[i]>=(SPLAtotal-SPLAdict[i])):
            if(len(SPLAconflict)!=1):
                SPLAconflict.pop(i,None)
        elif(SPLAdict[i]<(SPLAtotal-SPLAdict[i])):
            #Update SPLAdaysRequested and SPLAtotal
            SPLAdaysRequested[0] -= int(i[13])
            SPLAdaysRequested[1] -= int(i[14])
            SPLAdaysRequested[2] -= int(i[15])
            SPLAdaysRequested[3] -= int(i[16])
            SPLAdaysRequested[4] -= int(i[17])
            SPLAdaysRequested[5] -= int(i[18])
            SPLAdaysRequested[6] -= int(i[19])
            SPLAtotal -= SPLAdict[i]
            #Remove from SPLAdict, remSPLA and SPLAconflict
            SPLAdict.pop(i,None)
            remSPLA.remove(i)
            SPLAconflict.pop(i,None)
            #Update conflict dictionary
            for i in remSPLA:
                SPLAconflict[i] = 0

            for i,j in zip(range(0,7),range(13,20)):
                if(SPLAdaysRequested[i]>lots[i]):
                    for k in remSPLA:
                        for l in remSPLA:
                            if(l!=k and k[j]=='1' and l[j]=='1'):
                                SPLAconflict[k] += 1

        maxSPLAconflict = max(SPLAconflict.iteritems(), key=operator.itemgetter(1))[1]

#Remove LAHSA applicants with conflicts
maxLAHSAconflict = max(LAHSAconflict.iteritems(), key=operator.itemgetter(1))[1]
while(maxLAHSAconflict>0):
    #Get applicants with this max value
    maxLAHSApeople = [k for k,v in LAHSAconflict.iteritems() if v==maxLAHSAconflict]
    #Check if their request value is greater than total value
    for i in maxLAHSApeople:
        if(LAHSAdict[i]>=(LAHSAtotal-LAHSAdict[i])):
            if(len(LAHSAconflict)!=1):
                LAHSAconflict.pop(i,None)
        elif(LAHSAdict[i]<(LAHSAtotal-LAHSAdict[i])):
            #Update LAHSAdaysRequested and LAHSAtotal
            LAHSAdaysRequested[0] -= int(i[13])
            LAHSAdaysRequested[1] -= int(i[14])
            LAHSAdaysRequested[2] -= int(i[15])
            LAHSAdaysRequested[3] -= int(i[16])
            LAHSAdaysRequested[4] -= int(i[17])
            LAHSAdaysRequested[5] -= int(i[18])
            LAHSAdaysRequested[6] -= int(i[19])
            LAHSAtotal -= LAHSAdict[i]
            #Remove from LAHSAdict, remLAHSA and LAHSAconflict
            LAHSAdict.pop(i,None)
            remLAHSA.remove(i)
            LAHSAconflict.pop(i,None)
            #Update conflict dictionary
            for i in remLAHSA:
                LAHSAconflict[i] = 0

            for i,j in zip(range(0,7),range(13,20)):
                if(LAHSAdaysRequested[i]>beds[i]):
                    for k in remLAHSA:
                        for l in remLAHSA:
                            if(l!=k and k[j]=='1' and l[j]=='1'):
                                LAHSAconflict[k] += 1

        maxLAHSAconflict = max(LAHSAconflict.iteritems(), key=operator.itemgetter(1))[1]


#Sort SPLA and LAHSA dictionaries
sorted_SPLAdict = sorted(SPLAdict.items(), key=operator.itemgetter(1), reverse=True)
sorted_LAHSAdict = sorted(LAHSAdict.items(), key=operator.itemgetter(1), reverse=True)

#Check if there are any LAHSA applicants that SPLA can take
chosen = "null"

for i in sorted_SPLAdict:
    flag = 0
    for j in sorted_LAHSAdict:
        if(i[0][0]==j[0][0] and i[0][1]==j[0][1] and i[0][2]==j[0][2] and i[0][3]==j[0][3] and i[0][4]==j[0][4]):
            chosen = i[0][0]+i[0][1]+i[0][2]+i[0][3]+i[0][4]
            flag = 1
            break
    if(flag==1):
        break

#If there are no LAHSA applicants
if(chosen=="null"):
    chosen = sorted_SPLAdict[0][0][0]+sorted_SPLAdict[0][0][1]+sorted_SPLAdict[0][0][2]+sorted_SPLAdict[0][0][3]+sorted_SPLAdict[0][0][4]

print(chosen)
f = open("output.txt", "w")
f.write(chosen)
