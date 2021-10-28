import os
import requests
from tabulate import tabulate
import json

TOKEN = os.getenv('TOKEN')
url = 'https://scim-provisioning.service.newrelic.com/scim/v2/{}'
usr = 'Users'
grp = 'Groups'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {TOKEN}",
}

os.system('clear')

def clearScreen():
    input("Press ENTER to continue..")
    os.system('clear')

def getUsers():
    userResponse = requests.get(url=url.format(usr), headers=headers)
    userJsonData = userResponse.json()
    groupResponse = requests.get(url=url.format(grp), headers=headers)
    groupJsonData = groupResponse.json()
    list = []
    
    for userName in userJsonData['Resources']:
        groupList = []
        for groupName in groupJsonData['Resources']:
            if len(groupName['members']) != 0:
                 for grpName in groupName['members']:
                    if userName['id'] == grpName['value']:
                        groupList.append(groupName['displayName'])
        user = userName['userName'], userName['name']['givenName'], userName['name']['familyName'],  userName[
            'urn:ietf:params:scim:schemas:extension:newrelic:2.0:User']['nrUserType'], userName['id'],groupList
        list.append(user)

    hds = ['Email', 'First Name', 'Last Name', 'User Type', 'ID', 'Group']
    pretty = tabulate(list, headers=hds)
    print(pretty)
    print()
def getGroups():
    response = requests.get(url=url.format(grp), headers=headers)
    jsonData = response.json()
    list = []
    for groupName in jsonData['Resources']:
        user = groupName['displayName'], groupName['id']
        list.append(user)

    hds = ['Group', 'Group Id']
    pretty = tabulate(list, headers=hds)
    print(pretty)
    print()

def createUsers(fName,lName,email,userType):
    with open("util/users.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data['userName'] = email
    data['emails'][0]['value'] = email 
    data['name']['givenName'] = fName
    data['name']['familyName'] = lName
    data['urn:ietf:params:scim:schemas:extension:newrelic:2.0:User']['nrUserType'] = userType + ' User'
    
    with open("util/users.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    jsonFile = open('util/users.json','rb')
    users=jsonFile.read()
    response = requests.post(url=url.format(usr), headers=headers, data=users)
    jsonData = response.json()
    print(jsonData)
    jsonFile.close()
    print()

def createGroups(groupName):
    with open("util/groups.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data['displayName'] = groupName
    with open("util/groups.json", "w") as jsonFile:
        json.dump(data, jsonFile)    
    jsonFile = open('util/groups.json','rb')
    users=jsonFile.read()
    response = requests.post(url=url.format(grp), headers=headers, data=users)
    jsonData = response.json()
    print(jsonData)
    jsonFile.close()
    print() 

def usersGroups(userId,groupId):
    with open("util/usersGroup.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data['Operations'][0]['op'] = 'Add'
    data['Operations'][0]['value'][0]['value'] = userId
    with open("util/usersGroup.json", "w") as jsonFile:
        json.dump(data, jsonFile)    
    jsonFile = open('util/usersGroup.json','rb')
    users=jsonFile.read()
    response = requests.patch(url=url.format(grp+'/'+groupId), headers=headers, data=users)
    jsonData = response.json()
    print(jsonData)
    jsonFile.close()
    print()
def deleteUser(userId):
    response = requests.delete(url=url.format(usr+'/'+userId), headers=headers)
    print(response)
    print()
def deleteGroup(groupId):
    response = requests.delete(url=url.format(grp+'/'+groupId), headers=headers)
    print(response)
    print()

def menu():   
    print("[1] View Users")
    print("[2] View Groups")
    print("[3] Create User")
    print("[4] Create Group")
    print("[5] Add a User to a group")
    print("[6] Delete a user")
    print("[7] Delete a group")
    print("[0] Exit")

menu()
selection = int(input("Enter selection: "))

while selection != 0:
    if selection == 1:
        os.system('clear')
        getUsers()
        clearScreen()
    elif selection == 2:
        os.system('clear')
        getGroups()
        clearScreen()
    elif selection == 3:
        os.system('clear')
        fName = input('Enter User First Name: ')
        lName = input('Enter User Last Name: ')
        email = input('Enter User email: ')
        userType = input('Enter User typer(Full/Basic): ')
        createUsers(fName,lName,email,userType)
        clearScreen()
    elif selection == 4:
        os.system('clear')
        groupName = input('Enter Group Name: ')
        createGroups(groupName)
        clearScreen()
    elif selection == 5:
        os.system('clear')
        getUsers()
        print()
        userId = input('Please copy and paste from list above the user ID: ')
        os.system('clear')
        getGroups()
        groupId = input('Please copy and paste from list above the group ID: ')
        usersGroups(userId,groupId)
        clearScreen()
    elif selection == 6:
        os.system('clear')
        getUsers()
        print()
        userId = input('Please copy and paste the user ID to delete: ')
        deleteUser(userId)
        clearScreen()
    elif selection == 7:
        os.system('clear')
        getGroups()
        print()
        groupId = input('Please copy and paste the Group ID to delete: ')
        deleteGroup(groupId)
        clearScreen()    
    else:
        os.system('clear')
        print()
        print("Invalid Option!!! Please select only options shown below")
        print()

    menu()
    selection = int(input("Enter selection: "))
