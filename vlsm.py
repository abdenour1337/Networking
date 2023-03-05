import sqlite3
import random
import string

def generateRandomString():
    # lower string of 10 length
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(10))
    return result_str


databaseName =  generateRandomString()
connexion = sqlite3.connect(databaseName)
cursor = connexion.cursor()




cursor.execute("CREATE TABLE IF NOT EXISTS vlsm(NetworkId INTEGER PRIMARY KEY AUTOINCREMENT, HostsNumber INT, MaxHostsNumber INT, CIDR INT, NetworkIpAddress TEXT, NetworkMask TEXT, FirstIpAddres TEXT, LastIpAddress TEXT, BroadcastIpAddress TEXT)")

def firstInsert(HostsNumber, MaxHostsNumber, CIDR, NetworkMask ):
    query = '''INSERT INTO vlsm(HostsNumber, MaxHostsNumber, CIDR, NetworkMask) VALUES ({HostsNumber}, {MaxHostsNumber}, {CIDR}, '{NetworkMask}')'''.format(HostsNumber=HostsNumber, MaxHostsNumber=MaxHostsNumber, CIDR=CIDR, NetworkMask=NetworkMask)
    cursor.execute(query)
    connexion.commit() 


def insertSpecificDataIntoTable(columnName, columnValue, networkID):
    cursor.execute("update vlsm set {}='{}' WHERE NetworkId={}".format(columnName, columnValue, networkID))
    connexion.commit()  


def getCIDRBasedOnNetworkID(networkID):
    result  = cursor.execute("SELECT CIDR FROM vlsm WHERE networkId = {}".format(networkID))
    return result.fetchone()




ipAddress = '192.168.1.0/30'
ipAddress = str(input("IP Address [0.0.0.0/0] > "))



ipAddr = ipAddress.split('/')[0]

cidr = ipAddress.split('/')[1]


def getMaxHostNumbers(cidr):
    if int(cidr) <= 30:
        return ( 2 ** ( 32 - int(cidr)) ) - 2 
    else:
         raise Exception("This Network suffix can't address hosts")


def getIpAddressBlock(ipAddress, blockId) -> str:
    #A function that return an octet of the ip address based on the BlockId
    #It takes as argument an ip addr (str) and a block id (int)
    if blockId == 3:
        return ipAddress.split('.')[blockId].split('/')[0]    
    return ipAddress.split('.')[blockId]
    


def decimalToBinary(decimal) -> str:
    #decimal is string
    #this function returns a binary representation (string datatype) of a given deciamal value 
    return bin(int(decimal)).replace('0b', '')




def paddingBinary(binaryString ):
    while len(binaryString) != 8:
        binaryString = '0' + binaryString
    
    return binaryString


def getPowerBasedOnNetworkHosts(netwrokHosts):
    for  power in range(0,30):
        if 2 ** power - 2 >= int(netwrokHosts):
            return int(power)







NETWORKS = []

NETWORKS_NUMBER = int(input("Networks Numbers > "))
for _ in range(NETWORKS_NUMBER):
    NETWORKS.append(int(input("Hosts Number > ")))


def getNetworks():
    NETWORKS.sort(reverse=True)
    return NETWORKS



def getMaskBasedOnCIDR(cidr):

    if cidr > 30:
        raise Exception("This network Suffix Can't address Hosts")
    mask = ''
    for x in range(cidr):
        mask += '1'

    while len(mask) != 32:
        mask += '0'

    Maskblock1 = mask[0:8]    
    Maskblock2 = mask[8:16]    
    Maskblock3 =  mask[16:24]
    Maskblock4 =  mask[24:]
    return ( str(int(Maskblock1, 2)) +'.'+str(int(Maskblock2, 2))+'.'+str(int(Maskblock3, 2))+'.'+str(int(Maskblock4, 2)))






for HostsNumber in getNetworks():
    cidr = 32 - getPowerBasedOnNetworkHosts(HostsNumber)
    MaxHostNumber = getMaxHostNumbers(cidr)
    NetworkMask = getMaskBasedOnCIDR(cidr)

    firstInsert(int(HostsNumber), int(MaxHostNumber),int(cidr), str(NetworkMask))


currentIpAddress = ipAddr
networkAddress = currentIpAddress
for _ in range(len(getNetworks())):

    
    cidr = getCIDRBasedOnNetworkID(_+1)[0]
    if  cidr >= 24:

        FirstIpAddress = getIpAddressBlock(networkAddress,0) +'.'+getIpAddressBlock(networkAddress,1)+'.'+getIpAddressBlock(networkAddress,2)+'.'+  str(    int ( getIpAddressBlock(networkAddress,3)) + 1  )
        BroadcastIpAddress = getIpAddressBlock(networkAddress,0) +'.'+getIpAddressBlock(networkAddress,1)+'.'+getIpAddressBlock(networkAddress,2)+'.'+  str(    int ( getIpAddressBlock(networkAddress,3))  + (2 **(32 - getCIDRBasedOnNetworkID(_+1)[0])) - 1 )
        LastIpAddress = getIpAddressBlock(BroadcastIpAddress,0) +'.'+getIpAddressBlock(BroadcastIpAddress,1)+'.'+getIpAddressBlock(BroadcastIpAddress,2)+'.'+  str(    int ( getIpAddressBlock(BroadcastIpAddress,3)) - 1   )


    nextIpAddressFourthBlock = int( getIpAddressBlock(networkAddress,3) ) + (2 ** (32 - cidr)) 

    difference = 256 // nextIpAddressFourthBlock

    if difference > 1:
        nextIpAddressFourthBlock = int( getIpAddressBlock(networkAddress,3) ) + (2 ** (32 - cidr))
        nextIpAddressthirdBlock =               int( getIpAddressBlock(networkAddress,2) )
    elif difference < 1:
        nextIpAddressthirdBlock = int( getIpAddressBlock(networkAddress,2) ) +   difference
        nextIpAddressFourthBlock = 0

    else :
        nextIpAddressFourthBlock = int( getIpAddressBlock(networkAddress,3) ) + (2 ** (32 - cidr))
        nextIpAddressthirdBlock =               int( getIpAddressBlock(networkAddress,2) )

    



    # print(networkAddress)
    # print(FirstIpAddress)
    # print(LastIpAddress)
    # print(BroadcastIpAddress)

    #NetworkIpAddress, NetworkMask, FirstIpAddres, LastIpAddress, BroadcastIpAddress
    insertSpecificDataIntoTable('NetworkIpAddress', networkAddress, _+1 )
    insertSpecificDataIntoTable('FirstIpAddres', FirstIpAddress, _+1 )
    insertSpecificDataIntoTable('LastIpAddress', LastIpAddress, _+1 )
    insertSpecificDataIntoTable('BroadcastIpAddress', BroadcastIpAddress, _+1 )




####################### L3JAJA HNAAAAAAAAYA  #######################################################################################
    try:
        networkAddress = getIpAddressBlock(networkAddress,0) +'.'+getIpAddressBlock(networkAddress,0)+'.'+str(nextIpAddressthirdBlock)+'.'+str(nextIpAddressFourthBlock)
    except:
        networkAddress = getIpAddressBlock(networkAddress,0) +'.'+getIpAddressBlock(networkAddress,0)+'.'+str(nextIpAddressthirdBlock)+'.'+str(nextIpAddressFourthBlock)
    
#####################################################################################################################################


    

    # print(getIpAddressBlock(ipAddress, 3))
    # print(_+1)













# print( paddingBinary( decimalToBinary(  getIpAddressBlock(ipAddress.split('/')[0], 3))))








def fetchAll():
    result = cursor.execute("SELECT * FROM vlsm")
    for x in result.fetchall():
        print(x)

fetchAll()