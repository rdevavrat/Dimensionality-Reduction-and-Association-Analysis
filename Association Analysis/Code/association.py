import pandas as pd
import itertools
import sys

filePath = sys.argv[1]

# Load DataSet
inputData = pd.read_csv(filePath, sep='\t', lineterminator='\n', header=None)


# Data Pre-processing
for i in range(len(inputData.columns)-1):
    inputData[i] = 'G' + str(i+1) + "_" + inputData[i].astype(str)
	

# Support and Confidence Values
support = int(sys.argv[2]) / 100 * len(inputData)
confidence = int(sys.argv[3])/100

# InputData is converted to a list of lists
inputDataList = []
for i in range(len(inputData)) :
    inputDataList.append(set(inputData.iloc[i]))
	
##############################################################################
# This function is used to generate candidate itemsets of desired length
##############################################################################
def candidateItemsetGenerator(inputItemset,desiredLength):
    candidateItemset = itertools.combinations(inputItemset,desiredLength)
    
    temporary = []
    for itr in list(candidateItemset):
        temporary.append(set(itr))
        
    return temporary
	
##############################################################################
# This function is used to Prune the Candidate Itemset
##############################################################################
def pruneCandidateItemset(inputItemset,totalFrequentItemset):
    pruned_Itemset = []
    for item in inputItemset:
        currentSupportCount = 0
        for row in inputDataList:
            if(item.issubset(row)):
                currentSupportCount += 1
        if(currentSupportCount >= support):
            pruned_Itemset.append(item)
            if(item != None):
                temp = list(item)
                temp.sort()
                #totalFrequentItemset[str(set(temp))] = currentSupportCount
                totalFrequentItemset.loc[len(totalFrequentItemset)] = pd.Series({'Itemset':set(temp), 'Support':currentSupportCount })
                
    return pruned_Itemset
	
##############################################################################
# This function is used to compute all the frequent itemset
##############################################################################
def aprioriAlgorithm(candidateItemset,maximumItemsetLength,totalFrequentItemset):
    for itr in range(len(inputData.columns)-1):
        # Call candidateItemsetGenerator() to generate candidate itemsets
        currentCandidateItemset = candidateItemsetGenerator(candidateItemset, itr + 1)
        
        # Call pruneCandidateItemset() to refine the candidate itemset and 
        # keep only those elements which satisfy the minimum support requirement
        prunedItemset = pruneCandidateItemset(currentCandidateItemset,totalFrequentItemset)
        
        # If after pruning the size of the list is zero 
        # break the loop as no more candidates can be generated
        if(len(prunedItemset) == 0):
            break
        else:
            # Otherwise print the total number of candidates generated
            ss = "number of length-" + str(itr+1) + " frequent itemsets"
            lengthOfItemsets.loc[len(lengthOfItemsets)] = pd.Series({'Type':ss,'Count':str(len(prunedItemset))})
        # Perform union operation on the prunedItemset with itself 
        # to compute combinations for next candidate itemset
        candidateItemset = set.union(*prunedItemset)
    
    # Print the number of total itemset generated
    
    lengthOfItemsets.loc[len(lengthOfItemsets)] = pd.Series({'Type':"Total frequent itemsets",'Count':str(len(totalFrequentItemset))})
    # Return the length largest itemset formed
    return itr

##############################################################################
# This section computes the initial length-1 frequent candidate itemset
##############################################################################
# Set to store the initial length-1 frequent itemset
candidateItemset = set()
# Store the dimensions of the input data
rows,columns = inputData.shape
# Iterate over each column of the input data
for col in range(columns):
    keys = []
    # Save all the unique elements of each columns in a list called keys
    keys = inputData[col].unique()
    # Store the frequency of each element of 'keys' 
    colSummary = inputData.groupby(inputData[col]).size()
    colFreq = colSummary.to_dict()
    #Iterate over all the elements and check their frequency
    # If the frequency of a item satisfies the 
    # minimum required frequency (support), store it.
    for i in range(len(keys)):
        if(colFreq[keys[i]] >= support):
            candidateItemset.add(keys[i])
	
lengthOfItemsets = pd.DataFrame(columns=['Type','Count'])
	
# totalFrequentItemset to store a list of all the generated frequent itemsets of all lengths
maximumItemsetLength = 0
totalFrequentItemset=pd.DataFrame(columns=['Itemset','Support'])
#totalFrequentItemset = aprioriAlgorithm(candidateItemset,maximumItemsetLength,FIS)
maximumItemsetLength = aprioriAlgorithm(candidateItemset,maximumItemsetLength,totalFrequentItemset)

# Creates an empty dataframe to store generated rules
AssociationRules = pd.DataFrame(columns=['HEAD','BODY','CONFIDENCE'])

##############################################################################
# This function is used to mine all possible assocication
# rules from the set of frequent itemsets
##############################################################################
def generateAssociationRules(totalFrequentItemset):
    #Iterate over each item of the frequent itemset
    for item in totalFrequentItemset['Itemset']:
        # Iterate over each of the element in the itemset
        for currLengthOfKey in range(len(item)):
            if(len(item) > currLengthOfKey + 1):
                # Generate all possible combinations of the elements present in the itemset
                rulesCombined = candidateItemsetGenerator(item,currLengthOfKey + 1)
                # Iterate over all the generate combinations of the itemset
                # Treat each itemset as head and body of the rule
                for rule in rulesCombined:
                    # 'a' contains the current itemset
                    a = list(item)
                    a.sort()
                    # 'b' contains the difference between current itemset and 
                    # the current combination of the elements between the itemset
                    b = list(item.difference(rule))
                    b.sort()
                    # Calculate the confidence for the current combination of the itemset
                    currentConfidence = totalFrequentItemset['Support'][totalFrequentItemset.loc[totalFrequentItemset['Itemset'] == set(a)].index.values[0]] / totalFrequentItemset['Support'][totalFrequentItemset.loc[totalFrequentItemset['Itemset'] == set(b)].index.values[0]]
                    # If the current combination of the itemset satisfies the 
                    # minimum required confidence, then store it.
                    if(currentConfidence > confidence):
                        AssociationRules.loc[len(AssociationRules)] = pd.Series({'HEAD':item.difference(rule),'BODY':rule,'CONFIDENCE':currentConfidence})
						
# Call generateAssociationRules to mine the Association rules
generateAssociationRules(totalFrequentItemset)

print("\n\n",lengthOfItemsets,"\n\n")

print("\n\n ********* Total Frequent Itemsets *********\n", totalFrequentItemset,"\n\n")

print("\n\n********* Association Rules *********\n", AssociationRules,"\n\n")


minedRules = pd.DataFrame(columns=['HEAD','BODY','CONFIDENCE'])

	
##############################################################################
# Template 1 Miner
##############################################################################

def template1(whereToFind, typeToFind, whatToFind,minedRules):
    count = 0
    
    # RULE
    if(whereToFind.lower() == "rule"):
        # ANY
        if(type(typeToFind) == str and typeToFind.lower() == "any"):
            for item in whatToFind:
                for row in range(len(AssociationRules)):
                    flag = False
                    for itemset in list(AssociationRules['HEAD'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    for itemset in list(AssociationRules['BODY'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    if(flag == True):
                        count += 1
                        minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # None
        elif(type(typeToFind) == str and typeToFind.lower() == "none"):
            for item in whatToFind:
                for row in range(len(AssociationRules)):
                    headFlag = False
                    bodyFlag = False
                    for itemset in list(AssociationRules['HEAD'][row]):
                        if(itemset.lower() == item.lower()):
                            headFlag = True
                    for itemset in list(AssociationRules['BODY'][row]):
                        if(itemset.lower() == item.lower()):
                            bodyFlag = True
                    if(headFlag == False and bodyFlag == False):
                        count += 1
                        minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # 1
        elif(typeToFind == 1):
            for row in range(len(AssociationRules)):
                flagList = []
                for item in whatToFind:
                    flag = False
                    for itemset in list(AssociationRules['HEAD'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    for itemset in list(AssociationRules['BODY'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    flagList.append(flag)
                if(flagList.count(True) == 1 and flagList.count(False) == len(flagList)-1):
                    count += 1
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})

    elif(whereToFind.lower() == "head"):
        # ANY
        if(type(typeToFind) == str and typeToFind.lower() == "any"):
            for item in whatToFind:
                for row in range(len(AssociationRules)):
                    flag = False
                    for itemset in list(AssociationRules['HEAD'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    if(flag == True):
                        count += 1
                        minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # None
        elif(type(typeToFind) == str and typeToFind.lower() == "none"):
            for item in whatToFind:
                for row in range(len(AssociationRules)):
                    flag = False
                    for itemset in list(AssociationRules['HEAD'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    if(flag == False):
                        count += 1
                        minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # 1
        elif(typeToFind == 1):
            for row in range(len(AssociationRules)):
                flagList = []
                for item in whatToFind:
                    flag = False
                    for itemset in list(AssociationRules['HEAD'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    flagList.append(flag)
                if(flagList.count(True) == 1 and flagList.count(False) == len(flagList)-1):
                    count += 1
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
                    
    elif(whereToFind.lower() == "body"):
        # ANY
        if(type(typeToFind) == str and typeToFind.lower() == "any"):
            for item in whatToFind:
                for row in range(len(AssociationRules)):
                    flag = False
                    for itemset in list(AssociationRules['BODY'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    if(flag == True):
                        count += 1
                        minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # None
        elif(type(typeToFind) == str and typeToFind.lower() == "none"):
            for item in whatToFind:
                for row in range(len(AssociationRules)):
                    flag = False
                    for itemset in list(AssociationRules['BODY'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    if(flag == False):
                        count += 1
                        minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # 1
        elif(typeToFind == 1):
            for row in range(len(AssociationRules)):
                flagList = []
                for item in whatToFind:
                    flag = False
                    for itemset in list(AssociationRules['BODY'][row]):
                        if(itemset.lower() == item.lower()):
                            flag = True
                    flagList.append(flag)
                if(flagList.count(True) == 1 and flagList.count(False) == len(flagList)-1):
                    count += 1
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
    
    for i in range(len(minedRules)):
        minedRules['HEAD'][i] = str( minedRules['HEAD'][i] )
        minedRules['BODY'][i] = str( minedRules['BODY'][i] )
        minedRules['CONFIDENCE'][i] = str( minedRules['CONFIDENCE'][i] )
    
    minedRules = minedRules.drop_duplicates()
    
    # print(whatToFind, " : ", count)
    #print(minedRules)
    
    
    return len(minedRules)
	

##############################################################################
# Template 1 Parser
##############################################################################

def parseTemplate1(query,minedRules):
    
    query = query[19:]
    
    # list of rules to find
    whatToFind = eval(query[query.find('['):query.find(']')+1])
    
    queryParts = query.split(",")
    
    # RULE / HEAD / BODY
    whereToFind = (queryParts[0].split("\""))[1]
    
    # 1 , ANY , NONE
    if(isinstance( eval(queryParts[1]), int ) ):
        typeToFind = eval(queryParts[1])
    else:
        typeToFind = (queryParts[1].split("\""))[1]


    print("\n*****************************\n Count = " , template1(whereToFind, typeToFind, whatToFind, minedRules),"\n*****************************\n") 
    #print("Rule = " , whereToFind, "\nType = " , typeToFind, "\nQuery = " , type(typeToFind) )
    
    #ctr = template1(whereToFind, typeToFind, whatToFind,minedRules)
		
	
##############################################################################
# Template 2
##############################################################################

def template2(whereToFind, size, minedRules):

    count = 0
    
    # RULE
    if(whereToFind.lower() == "rule"):
        for row in range(len(AssociationRules)):
            if((len(AssociationRules['HEAD'][row]) + len(AssociationRules['BODY'][row])) == size):
                count += 1
                minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
    # HEAD
    elif(whereToFind.lower() == "head"):
        for row in range(len(AssociationRules)):
            if(len(AssociationRules['HEAD'][row]) == size):
                count += 1
                minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
    # BODY
    elif(whereToFind.lower() == "body"):
        for row in range(len(AssociationRules)):
            if(len(AssociationRules['BODY'][row]) == size):
                count += 1
                minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
    
    for i in range(len(minedRules)):
        minedRules['HEAD'][i] = str( minedRules['HEAD'][i] )
        minedRules['BODY'][i] = str( minedRules['BODY'][i] )
        minedRules['CONFIDENCE'][i] = str( minedRules['CONFIDENCE'][i] )
    
    minedRules = minedRules.drop_duplicates()
    
    print("\n*****************************\ncount = " ,  len(minedRules), "\n*****************************\n")



##############################################################################
# Template 2 Parser
##############################################################################
def parseTemplate2(query,minedRules):
    
    query = query[19:]
    queryParts = query.split(",")
    
    # RULE / HEAD / BODY
    whereToFind = (queryParts[0].split("\""))[1]
    
    size = eval((queryParts[1])[1])
    
    #print("Rule = " , whereToFind, "\nSize = " , size)
    
    template2(whereToFind, size, minedRules)

		
def template_One_One(condition,whereToFindRule1,typeToFindRule1,whatToFindRule1,whereToFindRule2,typeToFindRule2,whatToFindRule2,minedRules):
    
    count = 0
    
    mineRule1 = pd.DataFrame(columns=['HEAD','BODY','CONFIDENCE'])
    mineRule2 = pd.DataFrame(columns=['HEAD','BODY','CONFIDENCE'])
    tempRules = pd.DataFrame(columns=['HEAD','BODY','CONFIDENCE'])
    # 1 AND 1
    if(condition[1].lower() == "and"):
        template1(whereToFindRule1, typeToFindRule1, whatToFindRule1, mineRule1)
        template1(whereToFindRule2, typeToFindRule2, whatToFindRule2, mineRule2)
        
        if(len(mineRule1) > 0):
            for i in range(len(mineRule1)):
                mineRule1['HEAD'][i] = str( mineRule1['HEAD'][i] )
                mineRule1['BODY'][i] = str( mineRule1['BODY'][i] )
                mineRule1['CONFIDENCE'][i] = str( mineRule1['CONFIDENCE'][i] )
                
        if(len(mineRule2) > 0):
            for i in range(len(mineRule2)):
                mineRule2['HEAD'][i] = str( mineRule2['HEAD'][i] )
                mineRule2['BODY'][i] = str( mineRule2['BODY'][i] )
                mineRule2['CONFIDENCE'][i] = str( mineRule2['CONFIDENCE'][i] )
        
        tempRules = pd.merge(mineRule1,mineRule2)
    
    # 1 OR 1
    elif(condition[1].lower() == "or"):
        template1(whereToFindRule1, typeToFindRule1, whatToFindRule1, tempRules)
        template1(whereToFindRule2, typeToFindRule2, whatToFindRule2, tempRules)
        
        
    minedRules = tempRules 
    
    
    
    if(len(minedRules) > 0):
        for i in range(len(minedRules)):
            minedRules['HEAD'][i] = str( minedRules['HEAD'][i] )
            minedRules['BODY'][i] = str( minedRules['BODY'][i] )
            minedRules['CONFIDENCE'][i] = str( minedRules['CONFIDENCE'][i] )
    
    minedRules = minedRules.drop_duplicates()
    
    
    
    
    print("\n*****************************\ncount = " ,  len(minedRules),"\n*****************************\n")
    
    #print(minedRules)
	
def template_One_Two(condition,whereToFindRule1,typeToFindRule1,whatToFindRule1,whereToFindRule2,sizeRule2,minedRules):
    
    count = 0

    tempMineRule1 = pd.DataFrame(columns=['HEAD','BODY','CONFIDENCE'])
    mineRule1 = pd.DataFrame(columns=['HEAD','BODY','CONFIDENCE'])
    mineRule2 = pd.DataFrame(columns=['HEAD','BODY','CONFIDENCE'])
   
    # 1 AND 2
    if(condition[1].lower() == "and"):
        # Call template 1 and find the rules
        template1(whereToFindRule1, typeToFindRule1, whatToFindRule1 ,tempMineRule1)
        # Find all the rules that satisfy 2nd condition
        if(len(tempMineRule1) > 0):
            # Condition 2 rule
            if(whereToFindRule2.lower() == "rule"):
                for row in range(len(tempMineRule1)):
                    if((len(tempMineRule1['HEAD'][row]) + len(tempMineRule1['BODY'][row])) == sizeRule2):
                        count += 1
                        mineRule1.loc[len(mineRule1)] = pd.Series({'HEAD':tempMineRule1['HEAD'][row],'BODY':tempMineRule1['BODY'][row] ,'CONFIDENCE':tempMineRule1['CONFIDENCE'][row]})
            # Condition 2 head
            elif(whereToFindRule2.lower() == "head"):
                for row in range(len(tempMineRule1)):
                    if(len(tempMineRule1['HEAD'][row]) == sizeRule2):
                        count += 1
                        mineRule1.loc[len(mineRule1)] = pd.Series({'HEAD':tempMineRule1['HEAD'][row],'BODY':tempMineRule1['BODY'][row] ,'CONFIDENCE':tempMineRule1['CONFIDENCE'][row]})
            # Condition 2 BODY
            elif(whereToFindRule2.lower() == "body"):
                for row in range(len(tempMineRule1)):
                    if(len(tempMineRule1['BODY'][row]) == sizeRule2):
                        count += 1
                        mineRule1.loc[len(mineRule1)] = pd.Series({'HEAD':tempMineRule1['HEAD'][row],'BODY':tempMineRule1['BODY'][row] ,'CONFIDENCE':tempMineRule1['CONFIDENCE'][row]})

        minedRules = mineRule1
    
    # 1 OR 2
    elif(condition[1].lower() == "or"):
        # Call template 1 and find the rules
        template1(whereToFindRule1, typeToFindRule1, whatToFindRule1 ,minedRules)
        # Condition 2 RULE
        if(whereToFindRule2.lower() == "rule"):
            for row in range(len(AssociationRules)):
                if((len(AssociationRules['HEAD'][row]) + len(AssociationRules['BODY'][row])) == sizeRule2):
                    count += 1
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # Condition 2 HEAD
        elif(whereToFindRule2.lower() == "head"):
            for row in range(len(AssociationRules)):
                if(len(AssociationRules['HEAD'][row]) == sizeRule2):
                    count += 1
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # Condition 2 BODY
        elif(whereToFindRule2.lower() == "body"):
            for row in range(len(AssociationRules)):
                if(len(AssociationRules['BODY'][row]) == sizeRule2):
                    count += 1
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})

    for i in range(len(minedRules)):
        minedRules['HEAD'][i] = str( minedRules['HEAD'][i] )
        minedRules['BODY'][i] = str( minedRules['BODY'][i] )
        minedRules['CONFIDENCE'][i] = str( minedRules['CONFIDENCE'][i] )
    
    minedRules = minedRules.drop_duplicates()
    
    
    print("\n*****************************\ncount = " ,  len(minedRules),"\n*****************************\n")
    
	
def template_Two_Two(condition,whereToFindRule1,sizeRule1,whereToFindRule2,sizeRule2,minedRules):
    
    count = 0

    # 2 AND 2
    if(condition[1].lower() == "and"):
        # head , body
        if(whereToFindRule1.lower() == "head" and whereToFindRule2.lower() == "body"):
            for row in range(len(AssociationRules)):
                if( (len(AssociationRules['HEAD'][row]) == sizeRule1) and  (len(AssociationRules['BODY'][row]) == sizeRule2) ):
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # body, head
        elif(whereToFindRule1.lower() == "body" and whereToFindRule2.lower() == "head"):
            for row in range(len(AssociationRules)):
                if( (len(AssociationRules['BODY'][row]) == sizeRule1) and  (len(AssociationRules['HEAD'][row]) == sizeRule2) ):
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
    # 2 OR 2
    elif(condition[1].lower() == "or"):
        # head , body
        if(whereToFindRule1.lower() == "head" and whereToFindRule2.lower() == "body"):
            for row in range(len(AssociationRules)):
                if( (len(AssociationRules['HEAD'][row]) == sizeRule1) or  (len(AssociationRules['BODY'][row]) == sizeRule2) ):
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
        # body, head
        elif(whereToFindRule1.lower() == "body" and whereToFindRule2.lower() == "head"):
            for row in range(len(AssociationRules)):
                if( (len(AssociationRules['BODY'][row]) == sizeRule1) or  (len(AssociationRules['HEAD'][row]) == sizeRule2) ):
                    minedRules.loc[len(minedRules)] = pd.Series({'HEAD':AssociationRules['HEAD'][row],'BODY':AssociationRules['BODY'][row] ,'CONFIDENCE':AssociationRules['CONFIDENCE'][row]})
                    
    for i in range(len(minedRules)):
        minedRules['HEAD'][i] = str( minedRules['HEAD'][i] )
        minedRules['BODY'][i] = str( minedRules['BODY'][i] )
        minedRules['CONFIDENCE'][i] = str( minedRules['CONFIDENCE'][i] )
    
    minedRules = minedRules.drop_duplicates()
    
    print("\n*****************************\ncount = " ,  len(minedRules),"\n*****************************\n")

##############################################################################
# Template 3 Parser
##############################################################################

def parseTemplate3(query,minedRules):
    
    query = query[19:]
    queryParts = query.split(",")
    
    condition = []
    condition.append(eval(((queryParts[0]).split("\"")[1])[0]))
    condition.append(((queryParts[0]).split("\"")[1])[1:len(((queryParts[0]).split("\"")[1]))-1])
    condition.append(eval(((queryParts[0]).split("\"")[1])[len(((queryParts[0]).split("\"")[1]))-1]))
    
    condition11 = False
    condition12 = False
    condition22 = False

    if(condition[0] == 1 and condition[2] == 1):
        condition11 = True
        operation = condition[1]
        whereToFindRule1 = eval(queryParts[1])
        typeToFindRule1 = eval(queryParts[2])
        whatToFindRule1 = eval(queryParts[3])
        whereToFindRule2 = eval(queryParts[4])
        typeToFindRule2 = eval(queryParts[5])
        temp = queryParts[6]
        whatToFindRule2 = eval(temp[temp.find('['):temp.find(']')+1])
        
        #print("\nCondidtion = ", condition, "\nRule1 = ", whereToFindRule1, "\ntype1 = ",typeToFindRule1, "\n what1 = ", whatToFindRule1, "\nRule2 = ", whereToFindRule2, "\ntype2 = typeToFindRule2", "\n what2 = ", whatToFindRule2)
    else:
        if(condition[0] == 1 and condition[2] == 2):
            condition12 = True
            operation = condition[1]
            whereToFindRule1 = eval(queryParts[1])
            typeToFindRule1 = eval(queryParts[2])
            whatToFindRule1 = eval(queryParts[3])
            whereToFindRule2 = eval(queryParts[4])
            queryParts[5] = queryParts[5].replace(')','')
            sizeRule2 = eval(queryParts[5])
            #print("\nCondidtion = ", condition, "\nRule1 = ", whereToFindRule1, "\ntype1 =", typeToFindRule1, "\n what1 = ", whatToFindRule1, "\nRule2 = ", whereToFindRule2, "\nSize = ",sizeRule2)
        else:
            if(condition[0] == 2 and condition[2] == 2):
                condition22 = True
                operation = condition[1]
                whereToFindRule1 = eval(queryParts[1])
                sizeRule1 = eval(queryParts[2])
                whereToFindRule2 = eval(queryParts[3])
                queryParts[4] = queryParts[4].replace(')','')
                sizeRule2 = eval(queryParts[4])
                #print("\nCondidtion = ", condition, "\nRule1 = ", whereToFindRule1,  "\nSize = ",sizeRule1, "\nRule2 = ", whereToFindRule2, "\nSize = ",sizeRule2)
          
    
    if(condition11):
        template_One_One(condition,whereToFindRule1,typeToFindRule1,whatToFindRule1,whereToFindRule2,typeToFindRule2,whatToFindRule2,minedRules)
    elif(condition12):
        template_One_Two(condition,whereToFindRule1,typeToFindRule1,whatToFindRule1,whereToFindRule2,sizeRule2,minedRules)
    elif(condition22):
        template_Two_Two(condition,whereToFindRule1,sizeRule1,whereToFindRule2,sizeRule2,minedRules)
	
	

	
print("Enter the query below : ")

query = input()
count = 0
# Creates an empty dataframe to store mined rules



if(query[18] == "1"):
	parseTemplate1(query,minedRules)
else:
	if(query[18] == "2"):
		parseTemplate2(query,minedRules)
	
	else:
		if(query[18] == "3"):
			parseTemplate3(query,minedRules)
		else:
			print("\nQuery not recognised!!!\n Try again\n")
