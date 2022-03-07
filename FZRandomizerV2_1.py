bl_info = {
    "name": "FZRandomizer",
    "author": "FruitZeus",
    "version": (2, 1),
    "blender": (3, 0, 0),
    "location": "Properties > Object Data Properties",
    "description": "Randomize Characters & Mesh Objects",
    "warning": "",
    "doc_url": "www.youtube.com/fruitzeus",
    "category": "Mesh",
}

import bpy
import random
import csv

"""GLOBAL VARS"""
hostNameWarning = ""


def main(context, func):

    objs = context.selected_objects

    if func == "rand":
        """Send each object to be randomized"""
        a = 0
        while a < len(objs):
            randShapeKey(objs[a])
            a +=1
    elif func == "reset":
            
        a = 0
        
        while a < len(objs):
            resetSK(objs[a])
            a +=1
        
    else:
        a = 0
        
        while a < len(objs):
            setParams(objs[a])
            a +=1

    
    
def randShapeKey(obj):
    
    
    if obj.type == "MESH" or obj.type == "LATTICE":
        """randomize shapekey list here"""
        k = obj.data.shape_keys
        
         
        
        """randomize all shape keys"""
        if k != None:
            kb = k.key_blocks
            kNum = len(kb)
            a = 0
            while a < kNum:
                r = random.random()
                min = kb[a].slider_min
                max = kb[a].slider_max
                ans = min + ((max - min) * r)
                kb[a].value = ans
                a += 1
                
            print(kb[0].value)


def resetSK(obj):
    if obj.type == "MESH" or obj.type == "LATTICE":
        """randomize shapekey list here"""
        k = obj.data.shape_keys
        
        """randomize all shape keys"""
        if k != None:
            kb = k.key_blocks
            kNum = len(kb)
            a = 0
            while a < kNum:
                min = kb[a].slider_min
                max = kb[a].slider_max
                if min > 0:
                    ans = min
                elif max < 0:
                    ans = max
                else:
                    ans = 0
                kb[a].value = ans
                a += 1
                
            print(kb[0].value)

def setParams (obj):
    
    param = bpy.context.scene.sk_prefix
    
    if obj.type == "MESH":
        """randomize shapekey list here"""
        print (obj.data.shape_keys)
        k = obj.data.shape_keys.key_blocks
        kNum = len(k) 
        
        """randomly select 1 hair style"""
        if kNum > 0:
            a = 0
            
            """count applicable parameters"""
            paramNum = 0
            appParamList = []
            
            while a < kNum:
                
                keyName = k[a].name
                prefix = keyName[0:len(param)]
                
                """is prefix 'param'. If so, add it to list of Shape Keys to be in the randomizer"""
                
                if prefix == param:
                    appParamList.append(k[a])
                    print (keyName)
                a += 1
            
            """
            
            We've found all the parameters to be considered in the random pool.
            Now, reset all those parameters to 1 (which means they will be scaled to 0)
            & find the lucky parameter to remain as a value of 0 (which means is is at full scale)
            
            """
            
            a = 0
            paramNum = len(appParamList)
            if paramNum > 0:
                randParam = random.randint(0,paramNum-1)
                
                while a < paramNum:
                    appParamList[a].value = 1
                    a += 1
                appParamList[randParam].value = 0
                
                print ("The Random Parameter Selected Was " + appParamList[randParam].name)
            else:
                print ("No Parameters")
            



"""-------------------------------------TINY--TOOLS-------------------------------------"""

def collExists(name):
    allColl = bpy.data.collections
    
    x = 0
    hostExists = False
    
    while x < len(allColl):
        if allColl[x].name == name:
            hostExists = True
            x = len(allColl)
        else:
            hostExists = False
            x += 1
    
    return hostExists

def setRootCollActive():
    scene_collection = bpy.context.view_layer.layer_collection
    bpy.context.view_layer.active_layer_collection = scene_collection

def collAtRoot(coll):
    """GET COLLECTIONS AT ROOT LAYER INITIALLY"""
    rootColls = bpy.context.view_layer.layer_collection.children
    
    exists = collExists(coll)
    
    atRoot = False
    
    if exists == True:
        """PROCEED"""
        
        
        for x in rootColls:
            if x.name == coll:
                atRoot = True
            else:
                """DO NOTHING"""       
    else:
        """DO NOTHING"""
    
    return atRoot
    
    
def freshConsole(lines):
    x = 0
    
    while x < lines:
        print("\n")
        x += 1
        

               
def appDataSheet(meta, overwrite):

    filepath = bpy.path.abspath("//") + bpy.context.scene.csv_doc_name

    # open the file in the write mode
    if overwrite == True:
        f = open(filepath, 'w', newline = '')
        
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(meta)

        # close the file
        f.close()
    else:
        f = open(filepath, 'a', newline = '')
        
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(meta)

        # close the file
        f.close()
    

def findMyColl(obj):
    
    for coll in bpy.data.collections:
        for x in coll.objects:
            if obj == x:
                print("coll found: " + coll.name)
                return coll
                
def setSubData(obj):
    coll = findMyColl(obj)
    obj['Sub Origin'] = coll.name
    
    return None

def listHostSubs():
    subs = []
    host = bpy.data.collections[bpy.context.scene.char_collection]
    
    for coll in host.children:
        subs.append(coll.name)
        
    return subs
        
def subTicketCounter(sub):
    
    """GIVEN AN ORIGIN SUB, FIND THE TOTAL TICKET IN POOL"""
    total = 0
    for obj in sub.objects:
        total += obj.fzRarity
    
    return total


"""----------------------------MAJOR--FUNCTIONS-------------------------------------"""
              
            
def multiOBJ(context):
    
    freshConsole(5)
    print("-----------GENERATING VARIANTS------------")
    freshConsole(1)
    
    '''bpy.types.Scene.char_collection'''
    name = bpy.context.scene.char_collection
    generations = bpy.context.scene.var_gen
    
    
    warning = ""
    
    
    """CHECK AND SEE IF HOST NAME EXISTS"""
    allColl = bpy.data.collections
    
    
    hostExists = collExists(name)
    atRoot = collAtRoot(name)
    if hostExists == True:
        bpy.context.view_layer.layer_collection.children[name].exclude = False
        poss = possibilities()
    else:
        warning = "Host name does not exist."
        poss = 0
        
    uniquePossible = True
    
    if bpy.context.scene.unique_variants == True:
        if generations > poss:
            uniquePossible = False
            if warning != "Host name does not exist.":
                warning = "Not Enough Variation For " + str(bpy.context.scene.var_gen) + " Unique Generations."
            """LIST REASON HERE"""
        else:
            """REMOVE REASON"""
    
    
    """CONDITIONS LIST TO RUN MULTI GEN TOOL"""
    conditions = []
    conditions.append(hostExists)
    conditions.append(atRoot)
    conditions.append(uniquePossible)
    
    
    clearToLaunch = True
    
    """ARE ALL CONDITIONS TRUE FOR MULTIGEN LAUNCH"""
    for x in conditions:
        if x == False:
            clearToLaunch = False
        else:
            """CLEAR TO LAUNCH IS TRUE BY THAT CONTITION"""
    
            
    if clearToLaunch == True:
        genCodesList = []
        buildChars(name, generations, genCodesList)
        
        if bpy.context.scene.autoSpawn == True:
            spawnVars()

    else:
        """HOST DID NOT EXIST"""
        print ('nope')
        bpy.context.scene.host_name_warning = warning




def buildChars(name, generations, genCodesList):
    
    genCSV = bpy.context.scene.gen_csv
    overwrite = bpy.context.scene.overwrite_csv
    
    """HOST EXISTS - CONTINUE"""
    hostExists = True
    

    host = bpy.data.collections[name]
    
    props = host.children
    
    folderName = 'Variants'
    varNames = 'Variant'
    
    """GENERATE VARIANTS FOLDER IF IT DOESNT ALREADY EXIST"""
    
    collCleaner(folderName)
    
    variantColl = bpy.context.blend_data.collections.new(name=folderName)
    bpy.context.scene.collection.children.link(variantColl)
    
    v = 0
    
    win = bpy.context.window_manager

    
    """PRIME ATTRIBUTES - SET ATTRIBUTE PROPERTIES FOR EACH ATTRIBUTE"""
    #send the host collection to prime all objects inside
    setAllSubOrigins(host)
    
    """BEGIN BUILDING CHARACTERS"""

    win.progress_begin(0, generations)
    
    while v < generations:
        buildChar (host, props, varNames + " " + str(v+1), genCodesList)
        linkMats("Variant " + str(v + 1))
        win.progress_update(v)
        v += 1

    v = 0
            
    win.progress_end()
    
    
    
    
    
    
    
    
    
    """IF NEEDED TO WRITE TO CSV DO HERE"""
    
    if genCSV == True:
    
        win.progress_begin(0, generations)
        
        print("Writing to CSV...")
        
        
        
        """DETERMINE HOW MANY COLUMNS AND COLUMN NAMES"""
        firstRow = [""]
        
        fCount = 0
        hostSubs = listHostSubs()
        extraObjects = bpy.data.collections["Variant 1"].objects
        
        while fCount < len(hostSubs):
            
            """Each Column"""
            firstRow.append(hostSubs[fCount] + " Name")
            firstRow.append(hostSubs[fCount] + " Material")
            firstRow.append(hostSubs[fCount] + " Tickets")
            firstRow.append(hostSubs[fCount] + ": Total Tickets")
            firstRow.append(hostSubs[fCount] + " Odds (% chance)")
            
            fCount += 1
        
        
            
        """WRITE THE HEADER OF DOCUMENT"""
        appDataSheet(firstRow, overwrite)   
        
        """WRITE EACH ROW OF VARIANT DATA"""
        while v < generations:
            variant_to_csv("Variant " + str(v + 1))
            win.progress_update(v)
            v += 1
        
        print("CSV Document generated.")
        
        win.progress_end()
    
    
    
    bpy.context.scene.host_name_warning = "Host Located: " + bpy.context.scene.char_collection
    
    

def variant_to_csv(collName):
    
    
    
    dataEntry = [collName]
    
    subs = listHostSubs()
    
    for sub in subs: 
        for obj in bpy.data.collections[collName].objects:
            
            """CHECK AND SEE IF THAT OBJECT IS FIRST IN LINE FOR DATA ENTRY"""
            """THIS IS ALPHABETIC ORDER OF SUBCOLLECTIONS, NOT OBJECT NAMES"""
            
            if obj['Sub Origin'] == sub:
                
                """ADD OBJECT NAME"""
                dataEntry.append(obj.name)
                
                
                """ADD MATERIAL NAME"""
                if len(obj.material_slots) > 0:
                    if obj.material_slots[0].material != None:
                        dataEntry.append(obj.material_slots[0].material.name)
                    else:
                        dataEntry.append("No Material")
                else:
                    dataEntry.append("No Material")
                
                """ADD OBJECT TICKETS"""
                dataEntry.append(obj.fzRarity)
                
                """ADD OBJECT SUB TOTAL TICKETS"""
                subColl = bpy.data.collections[obj['Sub Origin']]
                totalTickets = subTicketCounter(subColl)
                dataEntry.append(totalTickets)
                
                """ADD OBJECT ODDS"""
                objOdds = round(obj.fzRarity/totalTickets*100)
                dataEntry.append(objOdds)
                
    appDataSheet(dataEntry, False)
            
            
            
#def hideVPR():
#         """set all objects in collection to off except winner"""
#    
#    a = 0
#    print ("Collection: " + props[x].name)
#    print ("Turn Off:")
#    while a < objCount:
#        props[x].objects[a].hide_render = hvpr
#        props[x].objects[a].hide_viewport = hvpr
##            print (props[x].objects[a].name)
#        a += 1
#    
    
    
    
    
    
def linkMats(collName):
    """TAKE A LIST OF OBJECTS AND FIND MATERIALS THAT NEED TO LINK - LINKS THEM"""
    
    objs = bpy.data.collections[collName].objects
    
    #------
    matCode = "lm0_"
    
    #LIST OF ALL LINKMAT GROUPS STARTS EMPTY
    linkMatGroups = []
    
    #--POSSIBLE TO GEN UP TO 10 LINKMAT GROUPS
    groups = 10
    
    #FILL MATS WITH 10 EMPTY LINKMAT GROUPS
    x = 0
    while x < groups:
        lmGroup = []
        linkMatGroups.append(lmGroup)
        x += 1 
    
    
    for obj in objs:
        
        #is the obj name even long enough to be a linkmat?
        if len(obj.name) >= 4:
            
            #check and see if the first 4 characters match a linkmat group
            x = 0
            while x < groups:
                matCode = "lm" + str(x) + "_"
                if obj.name[0:4] == matCode:
                    
                    #---FOUND AN OBJECT THAT IS IN A LINKMAT GROUP
                    bpy.context.view_layer.objects.active = obj
                    #print (bpy.context.object.active_material.name)
                    
                    #PUTS OBJECT IN ACCORDING LINKMAT GROUP
                    linkMatGroups[x].append(obj)
                x += 1
    
    #print("Linked Materials:")
    
    x = 0
    
    while x < groups:
        linkObjs = len(linkMatGroups[x])
        
        if linkObjs > 1:
            """HEY"""
            #print (linkMatGroups[x])
            linkMat(linkMatGroups[x])
        
        x += 1
            
            

    #print("Linked Materials Printed...")
    
    
    
def linkMat(objs):
    
    mlExists = False
    matLib = None
    
    amt = len(objs)
    
    libName = "MATLIB"
    
    
    for obj in objs:
        if obj.name[4:10] == libName:
            mlExists = True
            matLib = obj
            
    #-------IF MATLIBRARY IS PRESENT----------
    if mlExists == True:
        
        #print ("MATLIBRARY FOUND........")
        setMLMats(objs, matLib)
        
        
    #-------------OTHERWISE-----------------    
    else:
        #Randomly delegate one in the group to be the material giver
        matNum = random.randint(0,amt-1)
        setMats(objs, objs[matNum])
    
    
    
def setMLMats(objs, matLib):
    #HOW MANY MATERIALS IN MAT LIBRARY    
    libLen = len(matLib.material_slots)
    if libLen > 0:
        matNum = random.randint(0,libLen-1)
        transferMat = matLib.material_slots[matNum].material
        
        for obj in objs:
            #print("Object " + obj.name + ": " + str(len(obj.material_slots)))
            if len(obj.material_slots) > 0 and obj != matLib:
                #only transfer the data if the material link is set to the object
                if obj.material_slots[0].link == 'OBJECT':
                    obj.material_slots[0].material = transferMat
            
        #print ("Transfer Material Located: " + transferMat.name)

def setMats(objs, matObj):
    if len(matObj.material_slots) > 0:
        transferMat = matObj.material_slots[0].material
        for obj in objs:
            print("Object " + obj.name + ": " + str(len(obj.material_slots)))
            if len(obj.material_slots) > 0:
                #only transfer the data if the material link is set to the object
                if obj.material_slots[0].link == 'OBJECT':
                    obj.material_slots[0].material = transferMat
                else:
                    #save the material incase#
                    """tempMat = obj.material_slots[0].material"""
                    
                    #change slot to object#
                    obj.material_slots[0].link = 'OBJECT'
                    
                    #apply New material
                    obj.material_slots[0].material = transferMat
            
        #print ("Transfer Material Located: " + transferMat.name)
    

def setLMName(obj, slot, isLM):
    
    name = obj.name
    
    currentlyLM = False
    
    """SEE IF THE LM EXISTS"""
    x = 0
    while x < 10:
        prefix = "lm" + str(x) + "_"
        print (prefix)
        if name[0:4] == prefix:
            currentlyLM = True
            print ("Prefix Match")

        x += 1
    
    """IF IT DOES, REMOVE IT"""
    if currentlyLM == True:
        print ("currentlyLM True")
        l = len(name)
        newName = obj.name[4:]
        print (newName)
        obj.name = newName
        print (obj.name)
        

    
    
    """SET OBJ NAME TO LMx_ IF NEED TO"""
    if isLM == True:
        prefix = "lm" + str(slot) + "_"
        obj.name = prefix + obj.name
        
    
    

  

def possibilities():
    
    hostName = bpy.context.scene.char_collection
    
    poss = 1
    
    if collExists(hostName):
        
        """hostColl is the Main Collection"""
        
        hostColl = bpy.data.collections[hostName]
        
        
        """HOW MANY VARIABLE COLLECTIONS"""
        
        for x in hostColl.children:
            
            """COUNT OBJ IN VARIABLE COLLECTION"""
            objs = x.objects
            count = len(objs)
            
            if count > 0:
                poss = poss * count
        
        warning = "Host Located: " + hostName
        bpy.context.scene.host_name_warning = warning
        
    else:
        poss = 0
        
        warning = "Host name does not exist."
        bpy.context.scene.host_name_warning = warning    
            
        
    return poss
        
def genRandomCode(props, unique):
    
    genCode = []
    
    x = 0
    
    while x < len(props):
        """randomize each collection parameter"""
        
        """get count of objects in collection"""
        
        ticketPool = 0
        
        objCount = len(props[x].objects)
        
        for prop in props[x].objects:
            ticketPool += prop.fzRarity
        


        
        """pick a winner based on whether its random or no Dups"""
        
        """RANDOM / UNIQUE RAND SEL"""
        
        ticket = random.randint(0, ticketPool-1)
        
        print (ticket)
        
        
        """find the owner of that ticket"""
        ticketCounter = 0
        propNum = 0
        for prop in props[x].objects:

            if ticket >= ticketCounter:
                if ticket < ticketCounter + prop.fzRarity:
                    print ("Selected is " + prop.name + " with " + str(prop.fzRarity) + " tickets.")
                    selObj = propNum
        
            ticketCounter += prop.fzRarity
            propNum += 1
                
        
        
        
        print (selObj)
        genCode.append(selObj)
        x += 1
    
    readCode(genCode, unique)
    return genCode



def readCode(gc, unique):
    
    code = ""
    
    for x in gc:
        code = code + str(x)    
    
    if unique == False:
        print(code)

def consolidateCode(gc):
    
    code = ""
    
    for x in gc:
        code = code + "-" + str(x)  
    
    code = code[1:]  

    return(code)





def buildChar (host, props, folder, genCodesList):     

    x = 0
    
    """Hide Viewport Check Box Thingy"""
    hvpr = bpy.context.scene.hide_layers_bool
    
    
    characterParams = []
    
    
    """PUT ALL THE OBJECTS AT ROOT LEVEL INTO THE CHARACTER PARAMETERS"""
    while x < len(host.objects):
        characterParams.append(host.objects[x])
        x += 1
    
    
    x = 0
    
    """randomize each character"""    
    if bpy.context.scene.unique_variants == True:
        
        codeIsUnique = False
        while codeIsUnique == False:
            genCode = genRandomCode(props, True)
            codeIsUnique = isUnique(genCode, genCodesList)
        
    else:    
        
        """Make 1 genCode and it doesnt matter what it is"""
        genCode = genRandomCode(props, False)
    
    
    
    """FOUND RANDOM CANDIDATE VIA genCode - GenCandidate NOW"""
    genCodesList.append(genCode)
    

    
    x = 0
    
    """BLANK LIST FOR NAMES TO GO IN CSV LIST"""
    
    
    for prop in props:
        
                
        """set all objects in collection to off except winner"""
        
#        hideVPR()
        
        winner = prop.objects[genCode[x]]
        winner.hide_render = False
        winner.hide_viewport = False  
        

        characterParams.append(winner)
#        print (winner.name)
        
        x +=1
    
    
    
    """Reset our counter to 0. Use this to loop through all of the selecter Character Parameters"""    
    x = 0
    cpCount = len(characterParams)
    
    variant = bpy.context.blend_data.collections.new(name=folder)
    bpy.data.collections['Variants'].children.link(variant)
    
    varRecipe = []
    
    while x < cpCount:
        dupToNewColl (characterParams[x], variant.name)
        x += 1
    reTargArmature (variant.name)
    #bpy.context.view_layer.layer_collection.children['Variants'].children[variant.name].exclude = True
    




def isUnique(code, codes):
    """CHECKS IF CODE EXISTS IN CODES"""
    """IF IT DOES, RETURN FALSE. IF NOT, RETURN TRUE"""
    for c in codes:
        
        if consolidateCode(c) == consolidateCode(code):
            #HERES THE PROBLEM#######
            print ("code: " +consolidateCode(code) + " - previously generated.")
            return False
    print ("code: " +consolidateCode(code))
    return True
    


    
def dupToNewColl (obj, collName):
    """Receive an object, make a LINKED duplicate, place that duplicate in a specific collection"""
    
    """What collection is main object in"""
    fromColl = whatCollection(obj)
    
    if bpy.context.scene.instBool == True:
        ob_dup = obj.copy()
        ob_dup.name = obj.name + " " + collName
        
        """SET CUSTOM PROPERTY FROM ITS BIRTH ORIGIN"""
        
        
        #print (obj.name + " spawned a new: " + ob_dup.name)
        bpy.data.collections[collName].objects.link(ob_dup)
        
    if bpy.context.scene.instBool == False:
        

        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        
        bpy.context.view_layer.objects.active = obj
        
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        dupName = bpy.context.active_object.name
        ob_dup = bpy.data.objects[dupName]
        ob_dup.name = obj.name + " " + collName
        
        """SET CUSTOM PROPERTY FROM ITS BIRTH ORIGIN"""
        #setSubData(ob_dup)
        
#        print (obj.name + " spawned a new: " + ob_dup.name)
        bpy.data.collections[collName].objects.link(ob_dup)
        fromColl.objects.unlink(ob_dup)

def whatCollection(obj):
    for coll in bpy.data.collections:
        for o in coll.objects:
            if o.name == obj.name:
                return coll
            
    return None
    
    
def instToNewColl (collName, location):
    """Receive a collection. Instance That Collection to specific location"""


 
def reTargArmature(collName):
    """CHECK IF HAS ARMATURE - ASSIGN PROPER ARMATURE"""
    charData = bpy.data.collections[collName].objects
    
    x = 0
    
    """Are you MESH, ARMATURE, or OTHER"""
    
    meshList = []
    armList = []
    otherList = []
    latList = []
    
    while x < len(charData):
        if charData[x].type == 'MESH':
            meshList.append(charData[x])
        elif charData[x].type == 'ARMATURE':
            armList.append(charData[x])
        elif charData[x].type == 'LATTICE':
            latList.append(charData[x])
        else:
            otherList.append(charData[x])
        x += 1
    
    """ASSIGN ALL VIABLE MESH TO COLL ARMATURE"""
    
    x = 0
    
    while x < len(meshList):
        name = meshList[x].name
        mods = bpy.data.objects[name].modifiers
          
        a = 0
        while a < len(mods):
            if mods[a].type == 'ARMATURE':
#                print ("Found The Armmy")
                if len(armList) > 0:
                    mods[a].object = armList[0]
            if mods[a].type == 'LATTICE':
                if len(latList) > 0:
                    mods[a].object = latList[0]
            else:
                """"""
            a += 1
        x += 1
    
def setAllSubOrigins(host):
    """RECEIVE A HOST COLLECTION - MAKE ALL OBJECTS INSIDE TO THEIR RESPECTIVE SUB DATA PROPERTIES"""
    for obj in host.all_objects:
        setSubData(obj)
    
def collCleaner(delCol):
    
    allColls = bpy.data.collections
    vFolderExists = False
    x = 0
    
    
    
    win = bpy.context.window_manager
    win.progress_begin(0, 100)
    
    while x < len(allColls):
        if allColls[x].name == delCol:
            vFolderExists = True
        else:
            """DO NOTHING"""
        x += 1
        
        
    win.progress_update(25)
    
    if vFolderExists:
        collection = bpy.data.collections.get(delCol)    
        collections = collection.children
        x = 0
        
        
        delContFolder = bpy.context.view_layer.layer_collection.children[delCol]
        delContFolder.exclude = False
        
        while x < len(collections):
            delContFolder.children[x].exclude = False
#            print (collections[x])
            x += 1
        objs = collection.all_objects
        
        win.progress_update(50)
        
        
        while len(objs) > 0:
            bpy.ops.object.select_all(action='DESELECT')
            objs[0].select_set(True)

#            print ('Removing ' + objs[0].name)
            bpy.data.objects.remove(objs[0])

    
        win.progress_update(75)  
            
#        print ('len(collections) = ' + str(len(collections)))
        
        x = 0
        while len(collections) > 0:
#            print(collections[0])
            bpy.data.collections.remove(collections[0])
            x+= 1
        bpy.data.collections.remove(collection) 
    else:
        """DO NOTHING"""

    win.progress_end()


def spawnVars():
    
    freshConsole(2)
    print("-----------SPAWN VARIANT INSTANCES------------")
    freshConsole(1)
    
    distConst = 0.2
    
    placeVector = [bpy.context.scene.spawnfloat_x, bpy.context.scene.spawnfloat_y, bpy.context.scene.spawnfloat_z]
    
    x = 0
    
    """CHECK AND SEE IF VARIANTS HAVE BEEN GENERATED YET"""
    varCollExists = collExists('Variants')
    
    
    if varCollExists == True:
        vars = len(bpy.data.collections['Variants'].children)
        varColl = bpy.data.collections['Variants'].children
        """THE NAME OF SPAWNS FOLDER - SPAWNS"""
        sName = 'SPAWNS'
        
        """EMPTY ANY OLD VERSIONS OF SPAWNS"""
        collCleaner(sName)
        
        """NEW COLLECTION FOR SPAWNS"""
        spawnsColl = bpy.context.blend_data.collections.new(name=sName)
        bpy.context.scene.collection.children.link(spawnsColl)
        
        
        """INSTANCE COLLECTION HERE"""
        
        setRootCollActive()
        
        while x < vars:
            bpy.ops.object.collection_instance_add(collection=varColl[x].name, align='WORLD', location=(placeVector[0] * (x+1), placeVector[1] * (x+1), placeVector[2] * (x+1)), scale=(1, 1, 1))
            x += 1
            inst = bpy.context.active_object
            inst.name = "Spawn " + str(x)
            bpy.context.scene.collection.objects.unlink(inst)
            bpy.data.collections[sName].objects.link(inst)
            print (inst.name)
        
        varFolder = bpy.context.view_layer.layer_collection.children['Variants']
        varFolder.exclude = True
    
    else:
        """NO VARS TO SPAWN - SORRY BUD"""

def vScrambler():
    """currently on or off"""
    if collExists('Variants'):
        state = bpy.context.view_layer.layer_collection.children['Variants'].exclude
        
        varFolder = bpy.context.view_layer.layer_collection.children['Variants']
        varFolder.exclude = False
        
        for coll in varFolder.children:
            coll.exclude = False
            
        objs = bpy.data.collections['Variants'].all_objects
        
        """send objs to the scrambler"""
        for obj in objs:
            randShapeKey(obj)
        
        varFolder.exclude = state


def queueBatch():
    print("I WILL QUEUE BATCH NOW")
    
    collName = 'SPAWNS'     
   
    
    
    
    if collExists(collName):
        scn = bpy.context.scene
    
        coll = bpy.data.collections[collName]
   
        queueLen = len(coll.objects)
   
        bpy.context.scene.frame_end = queueLen
        
        x = 0
        #ONLY USE FOR SPAWN COLLECTION
        while x < len(coll.objects):
           
            obj = coll.objects[x]
           
            frm = x
           
            obj.hide_render = True
            obj.hide_viewport = True
            obj.keyframe_insert('hide_render', frame=frm)
            obj.keyframe_insert('hide_viewport', frame=frm)

            obj.hide_render = False
            obj.hide_viewport = False
            obj.keyframe_insert('hide_render', frame=frm+1)
            obj.keyframe_insert('hide_viewport', frame=frm+1)

            obj.hide_render = True
            obj.hide_viewport = True
            obj.keyframe_insert('hide_render', frame=frm+2)
            obj.keyframe_insert('hide_viewport', frame=frm+2)
           
            x += 1    
            
def remSpawns():
    """REMOVES SPAWNS"""
    freshConsole(2)
    print("-----------REMOVED VARIANT INSTANCES------------")
    freshConsole(1)
    
    collCleaner('SPAWNS')
            

def setLMs(context, state):
    """DO STUFF HERE"""
    objs = context.selected_objects
    slot = bpy.context.scene.matgroup
    for obj in objs:
        setLMName(obj, slot, state)        

"""-----------------------CLASSES-------------------------------------"""

class FZR_Operator(bpy.types.Operator):
    """Randomize Shape Keys"""
    bl_idname = "object.fzr_operator"
    bl_label = "Shape Key Scrambler"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, "rand")
        return {'FINISHED'}
    
class FZR_multiOBJ(bpy.types.Operator):
    """Randomize Shape Keys"""
    bl_idname = "object.fzr_multiobj_operator"
    bl_label = "GENERATE"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        multiOBJ(context)
        return {'FINISHED'}


class queueForBatchRender(bpy.types.Operator):
    """Queue Spawns For A Batch Render"""
    bl_idname = "object.queue_batch_operator"
    bl_label = "Queue For Batch Render"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        queueBatch()
        return {'FINISHED'}

def collDims(col):
    objs = col.all_objects
    for obj in objs:
        print (obj.name)

class resetShapeKeys(bpy.types.Operator):
    """Set All Shape Keys To Zero"""
    bl_idname = "object.reset_shape_key_rand_operator"
    bl_label = "Reset Shape Keys"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, "reset")
        return {'FINISHED'}
    

class setLinkMatName(bpy.types.Operator):
    """Set Object Name To Reflect LinkMats"""
    bl_idname = "object.obj_lm_name_operator"
    bl_label = "Set LinkMat"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        setLMs(context, True)
        return {'FINISHED'}
    
class remLinkMatName(bpy.types.Operator):
    """Set Object Name To Reflect LinkMats"""
    bl_idname = "object.rem_obj_lm_name_operator"
    bl_label = "Rem LinkMat"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        setLMs(context, False)
        return {'FINISHED'}

class calcPoss(bpy.types.Operator):
    """Calculate All Possibilities"""
    bl_idname = "object.calc_poss_operator"
    bl_label = "Calculate Possibilities"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.scene.possibleGen = possibilities()
        return {'FINISHED'}
 

class selParam(bpy.types.Operator):
    """Set All Shape Keys To Zero"""
    bl_idname = "object.rand_sel_param_operator"
    bl_label = "Randomize Parameter"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, "selParam")
        return {'FINISHED'}

class spawnVariants(bpy.types.Operator):
    """Spawn Variants"""
    bl_idname = "object.spawn_var_operator"
    bl_label = "Spawn Variants"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print ('SPAWNED ' + str(bpy.context.scene.var_gen) + ' VARIANTS...')
        spawnVars()
        return {'FINISHED'}

class removeSpawns(bpy.types.Operator):
    """Remove Spawns"""
    bl_idname = "object.rem_spawn_operator"
    bl_label = "Remove Spawns"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print ('SPAWNED ' + str(bpy.context.scene.var_gen) + ' VARIANTS...')
        remSpawns()
        return {'FINISHED'}

class delVariants(bpy.types.Operator):
    """Delete Variants"""
    bl_idname = "object.del_var_operator"
    bl_label = "DELETE VARIANTS"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print ('DELETED ' + str(bpy.context.scene.var_gen) + ' VARIANTS...')
        collCleaner('Variants')
        return {'FINISHED'}

class variantScrambler(bpy.types.Operator):
    """Variants Scrambler"""
    bl_idname = "object.var_scrambler_operator"
    bl_label = "Variant Scrambler"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        vScrambler()
        return {'FINISHED'}

class FZR_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "FZRandomizer"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    
    def draw(self, context):
        layout = self.layout

        obj = context.object
        objs = context.selected_objects
        scn = context.scene
        
        
            
            
        
    



        row = layout.row()
        
        row.prop (scn, "char_collection")
        row.prop (scn, "unique_variants")
        row.prop (scn, "instBool")
        
        
        row = layout.row()
        row.prop(scn, "useRarity",
            icon="TRIA_DOWN" if scn.useRarity else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )        
        row.label(text = "Rarity")
        row.label(text="Active Object: " + obj.name)

        if scn.useRarity:
            objColl = whatCollection(obj)
            if objColl != None:
                
                row = layout.row()
                row.label(text="Sub Collection: " + objColl.name)
            
                row.prop (obj, "fzRarity")
                
                ticketPool = 0
                for x in objColl.objects:
                    ticketPool += x.fzRarity
                
                row = layout.row()
                row.label(text="Rarity: " + str(obj.fzRarity) + "/" + str(ticketPool))
                row.label(text=str(round(obj.fzRarity/ticketPool*100)) + "% chance")
                row = layout.row()
                row.label(text="")
        

        row = layout.row()
            

        
        
        
        row = layout.row()
        row.prop (scn, "var_gen")
        row = layout.row()
        
        row.operator("object.fzr_multiobj_operator")
        
        row = layout.row()
        
        row.operator("object.calc_poss_operator")
        row.label(text=str(round(bpy.context.scene.possibleGen)))

        
        row = layout.row()
        row.prop(scn, "gen_csv")
        row.prop(scn, "csv_doc_name")
        row.prop(scn, "overwrite_csv")
        
        
        row = layout.row()      
        row.operator("object.del_var_operator")
        row = layout.row()
        row.label(text=bpy.context.scene.host_name_warning)
        
        
        row = layout.row()
        row.label(text="")
        
        row = layout.row()
        row.label(text="Selected Objects: " + str(len(objs)))
        
        """SPAWN TOOLS COLLAPSE"""
        
        row = layout.row()
        row.prop(scn, "spawnexpanded",
            icon="TRIA_DOWN" if scn.spawnexpanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row.label(text="Spawn Tools")
        
        if scn.spawnexpanded:
        
            row = layout.row(align = True) 
            row.prop (scn, "spawnfloat_x")
            row.prop (scn, "spawnfloat_y")
            row.prop (scn, "spawnfloat_z")
            
            
            
            row = layout.row()
            row.operator("object.spawn_var_operator") 
            row.operator("object.rem_spawn_operator")      
        
            row = layout.row()
            row.prop (scn, "autoSpawn")
            row = layout.row()
            row.operator("object.queue_batch_operator")  
            
            row = layout.row()
            row.label (text="")
        
        
        """LINKMAT COLLAPSE"""
        row = layout.row()

        row.prop(scn, "expanded",
            icon="TRIA_DOWN" if scn.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row.label(text = "Advanced Material Options")
        
        if scn.expanded:
            
            row = layout.row()
            row.prop (context.scene, "matgroup")       
            row = layout.row()
            row.operator("object.obj_lm_name_operator")
            row = layout.row()
            row.operator("object.rem_obj_lm_name_operator")
            
            row = layout.row()
            
            row.label(text = "")
        
 
            
        
        """SHAPEKEYS COLLAPSE"""
        row = layout.row()
        row.prop(scn, "skexpanded",
            icon="TRIA_DOWN" if scn.skexpanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row.label(text = "Shape Key Tools")

        if scn.skexpanded:
            
            row = layout.row()
            row.prop (context.scene, "sk_prefix")
            
            sub = row.row(align = True)
            sub.scale_x = 1.5
            sub.operator("object.rand_sel_param_operator")

            row = layout.row()
            row.label(text="")

            row = layout.row()
            row.operator("object.var_scrambler_operator")
                            
            row = layout.row()
            row.operator("object.fzr_operator")

            
            row = layout.row()
            row.operator("object.reset_shape_key_rand_operator")

def register():
    bpy.utils.register_class(FZR_Operator)
    bpy.utils.register_class(FZR_multiOBJ)    
    bpy.utils.register_class(spawnVariants)
    bpy.utils.register_class(removeSpawns)
    bpy.utils.register_class(queueForBatchRender)
    bpy.utils.register_class(setLinkMatName)
    bpy.utils.register_class(calcPoss)
    bpy.utils.register_class(remLinkMatName)
    bpy.utils.register_class(variantScrambler)
    bpy.utils.register_class(delVariants)
    bpy.utils.register_class(resetShapeKeys)
    bpy.utils.register_class(selParam)
    bpy.utils.register_class(FZR_Panel)
    
    bpy.types.Object.fzRarity = bpy.props.IntProperty(name = "Tickets", default=1, min=1)
    
    bpy.types.Scene.expanded = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.autoSpawn = bpy.props.BoolProperty(name = "Auto Spawn", default=True)
    bpy.types.Scene.skexpanded = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.spawnexpanded = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.spawnfloat_x = bpy.props.FloatProperty(name = "", default=0)
    bpy.types.Scene.spawnfloat_y = bpy.props.FloatProperty(name = "", default=0)
    bpy.types.Scene.spawnfloat_z = bpy.props.FloatProperty(name = "", default=0)
    bpy.types.Scene.instBool = bpy.props.BoolProperty(name = "Instance", default=True)
    bpy.types.Scene.useRarity = bpy.props.BoolProperty(name = "Rarity", default=False)
    bpy.types.Scene.gen_csv = bpy.props.BoolProperty(name = "Write To CSV", default=False)
    bpy.types.Scene.overwrite_csv = bpy.props.BoolProperty(name = "Overwrite", default=True)
    bpy.types.Scene.possibleGen = bpy.props.FloatProperty(name = "Possibilities", default = 0)
    bpy.types.Scene.sk_prefix = bpy.props.StringProperty \
      (
      name = "Prefix",
      default = "hair_",
      description = "Define the prefix of the Shape Key group to be randomized.",
      )
     
    bpy.types.Scene.hide_layers_bool = bpy.props.BoolProperty \
      (
      name = "Hide VP/R",
      default = True,
      description = "Define the prefix of the Shape Key group to be randomized.",
      )
      
    bpy.types.Scene.unique_variants = bpy.props.BoolProperty \
      (
      name = "Unique",
      default = False,
      description = "Variants generated are to be individually unique",
      )
      
    """The Collection Name"""
    bpy.types.Scene.char_collection = bpy.props.StringProperty \
      (
      name = "Host",
      default = "Character",
      description = "Name of the collection to be randomized.",
      )

    bpy.types.Scene.csv_doc_name = bpy.props.StringProperty \
      (
      name = "CSV Name",
      default = "variant_data.csv",
      description = "Name of the csv to be written. CSV document is saved at the root of this project folder.",
      )


    """HOST NAME WARNING"""
    bpy.types.Scene.host_name_warning = bpy.props.StringProperty \
      (
      name = "Host Name Warning",
      default = "",
      description = "Host Name Warning.",
      )

    """Variants"""
    
    bpy.types.Scene.var_gen = bpy.props.IntProperty \
      (
      name = "Variants",
      default = 10,
      min = 1,
      description = "Number of total variants to generate.",
      )

    bpy.types.Scene.matgroup = bpy.props.IntProperty \
      (
      name = "LinkMat Group",
      default = 0,
      description = "Number of total variants to generate.",
      )

def unregister():
    bpy.utils.unregister_class(FZR_Operator)
    bpy.utils.unregister_class(FZR_multiOBJ)
    bpy.utils.unregister_class(setLinkMatName)
    bpy.utils.unregister_class(remLinkMatName)
    bpy.utils.unregister_class(resetShapeKeys)
    bpy.utils.unregister_class(variantScrambler)
    bpy.utils.unregister_class(selParam)
    bpy.utils.unregister_class(calcPoss)
    bpy.utils.unregister_class(queueForBatchRender)
    bpy.utils.unregister_class(spawnVariants)
    bpy.utils.unregister_class(removeSpawns)
    bpy.utils.unregister_class(delVariants)    
    bpy.utils.unregister_class(FZR_Panel)
    del bpy.types.Object.fzRarity
    del bpy.types.Scene.sk_prefix
    del bpy.types.Scene.possibleGen
    del bpy.types.Scene.char_collection
    del bpy.types.Scene.csv_doc_name
    del bpy.types.Scene.host_name_warning
    del bpy.types.Scene.var_gen
    del bpy.types.Scene.hide_layers_bool
    del bpy.types.Scene.unique_variants
    del bpy.types.Scene.matgroup
    del bpy.types.Scene.expanded
    del bpy.types.Scene.skexpanded
    del bpy.types.Scene.spawnexpanded
    del bpy.types.Scene.spawnfloat_x
    del bpy.types.Scene.spawnfloat_y
    del bpy.types.Scene.spawnfloat_z
    del bpy.types.Scene.instBool
    del bpy.types.Scene.autoSpawn
    del bpy.types.Scene.useRarity
    del bpy.types.Scene.gen_csv
    del bpy.types.Scene.overwrite_csv
    
if __name__ == "__main__":
    register()
    
    
