## coding:utf-8
from access_db_operate import *
from binary_search import *


def get_all_sensitiveAPI(db):
    fin = open("sensitive_func_sorted.pkl", 'rb')
    list_sensitive_funcname = pickle.load(fin)
    fin.close()

    _dict = {}
    
    pdg_db_path = "pdg_db"
    list_testID = os.listdir(pdg_db_path)
    print('list_testID: ', list_testID)
    
    query_str = "g.V().properties['functionId']"
    results = db.runGremlinQuery(query_str)
    print(results)
    for node in results:
        print(node)
        ele = node.properties['code'].split(' ')
        if binary_search_bisect(list_sensitive_funcname, ele):
        	file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
        	testID = file_path.split('/')[-2]
        	list_callee_cfgnodeID.append([testID, ([str(cfgnode._id)], str(cfgnode.properties['functionId']), func_name)])
        	print('testID: ', testID)
        	
    if list_callee_cfgnodeID != []:
    	for _l in list_callee_cfgnodeID:
    		print('_l[0]: ', _l[0])
                print('_l[1]: ', _l[1])
                if _l[0] in _dict.keys():
                    _dict[_l[0]].append(_l[1])
                else:
                    _dict[_l[0]] = [_l[1]]    


    print('Dict: ', _dict)
    return _dict


def get_all_pointer(db):
    _dict = {}
    list_pointers_node = get_pointers_node(db)
    for cfgnode in list_pointers_node:
        file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
        testID = file_path.split('/')[-2]
        pointer_defnode = get_def_node(db, cfgnode._id)
        pointer_name = []
        for node in pointer_defnode:
            name = node.properties['code'].replace('*', '').strip()
            if name not in pointer_name:
                pointer_name.append(name)

        if testID in _dict.keys():
            _dict[testID].append(([str(cfgnode._id)], str(cfgnode.properties['functionId']), pointer_name))
        else:
            _dict[testID] = [([str(cfgnode._id)], str(cfgnode.properties['functionId']), pointer_name)]

    return _dict


def get_all_array(db):
    _dict = {}
    list_arrays_node = get_arrays_node(db)
    for cfgnode in list_arrays_node:
        file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
        testID = file_path.split('/')[-2]
        array_defnode = get_def_node(db, cfgnode._id)
        array_name = []
        for node in array_defnode:
            name = node.properties['code'].replace('[', '').replace(']', '').replace('*', '').strip()
            if name not in array_name:
                array_name.append(name)

        if testID in _dict.keys():
            _dict[testID].append(([str(cfgnode._id)], str(cfgnode.properties['functionId']), array_name))
        else:
            _dict[testID] = [([str(cfgnode._id)], str(cfgnode.properties['functionId']), array_name)]

    return _dict


def get_all_pointer_use(db):
    _dict = {}
    list_pointers_node = get_pointers_node(db)
    for cfgnode in list_pointers_node:
        file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
        testID = file_path.split('/')[-2]
        pointer_defnode = get_def_node(db, cfgnode._id)
        
        _temp_list = []
        for node in pointer_defnode:
            name = node.properties['code'].strip()
            list_usenodes = get_all_use_bydefnode(db, node._id)
            list_defnodes = get_all_def_bydefnode(db, node._id)

            i = 0
            while i < len(list_defnodes):
                if list_defnodes[i]._id == cfgnode._id:
                    del list_defnodes[i]
                else:
                    i += 1

            list_usenodes += list_defnodes
            
            print(len(list_usenodes))
            for i in list_usenodes:
            	#if str(i).find("location")==-1:
                if str(i).find(",location")==-1:
                    list_usenodes.remove(i)
            loc_list=[]
            final_list=[]
            for i in list_usenodes:
                #print(i)
                #if 'location' in str(i):
                if ',location' in str(i):
                    print(str(i))
                    #location=str(i).split(",type:")[0].split("location:")[1][1:-1].split(":")
                    location=str(i).split(",type:")[0].split(",location:")[1][1:-1].split(":")
                    count=int(location[0])
                    loc_list.append(count)
            print(loc_list)
            if len(loc_list)!=0:
                a=loc_list.index(max(loc_list))
                final_list.append(list_usenodes[a])
            for use_node in final_list:
                if use_node._id in _temp_list:
                    continue
                else:
                    _temp_list.append(use_node._id)

                if testID in _dict.keys():
                    _dict[testID].append(([str(use_node._id)], str(use_node.properties['functionId']), name))
                else:
                    _dict[testID] = [([str(use_node._id)], str(use_node.properties['functionId']), name)]

    return _dict


def get_all_array_use(db):
    _dict = {}
    list_arrays_node = get_arrays_node(db)
    for cfgnode in list_arrays_node:
        file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
        testID = file_path.split('/')[-2]
        array_defnode = get_def_node(db, cfgnode._id)
        _temp_list = []
        for node in array_defnode:
            name = node.properties['code'].strip()
            list_usenodes = get_all_use_bydefnode(db, node._id)
            list_defnodes = get_all_def_bydefnode(db, node._id)

            i = 0
            while i < len(list_defnodes):
                if list_defnodes[i]._id == cfgnode._id:
                    del list_defnodes[i]
                else:
                    i += 1

            list_usenodes += list_defnodes
			
            for use_node in list_usenodes:
                if use_node._id in _temp_list:
                    continue
                else:
                    _temp_list.append(use_node._id)

                if testID in _dict.keys():
                    _dict[testID].append(([str(use_node._id)], str(use_node.properties['functionId']), name))
                else:
                    _dict[testID] = [([str(use_node._id)], str(use_node.properties['functionId']), name)]

    return _dict


def get_all_integeroverflow_point(db):
    _dict = {}
    list_exprstmt_node = get_exprstmt_node(db)
    for cfgnode in list_exprstmt_node:
        if cfgnode.properties['code'].find(' = ') > -1:
            code = cfgnode.properties['code'].split(' = ')[-1]
            pattern = re.compile("((?:_|[A-Za-z])\w*(?:\s(?:\+|\-|\*|\/)\s(?:_|[A-Za-z])\w*)+)")                
            result = re.search(pattern, code)
       
            if result == None:
                continue
            else:
                file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
                testID = file_path.split('/')[-2]
                name = cfgnode.properties['code'].strip()

                if testID in _dict.keys():
                    _dict[testID].append(([str(cfgnode._id)], str(cfgnode.properties['functionId']), name))
                else:
                    _dict[testID] = [([str(cfgnode._id)], str(cfgnode.properties['functionId']), name)]

        else:
            code = cfgnode.properties['code']
            pattern = re.compile("(?:\s\/\s(?:_|[A-Za-z])\w*\s)")
            result = re.search(pattern, code)
            if result == None:
                continue

            else:
                file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
                testID = file_path.split('/')[-2]
                name = cfgnode.properties['code'].strip()

                if testID in _dict.keys():
                    _dict[testID].append(([str(cfgnode._id)], str(cfgnode.properties['functionId']), name))
                else:
                    _dict[testID] = [([str(cfgnode._id)], str(cfgnode.properties['functionId']), name)]

    return _dict


if __name__ == '__main__':
    j = JoernSteps()
    j.connectToDatabase()
    
    _dict = get_all_sensitiveAPI(j)
    '''
    f = open("sensifunc_slice_points.pkl", 'wb')
    pickle.dump(_dict, f, True)
    f.close()
    print(_dict)
    
    _dict = get_all_pointer(j)
    f = open("pointuse_slice_points.pkl", 'wb')
    pickle.dump(_dict, f, True)
    f.close()
    print(_dict) 
    
    _dict = get_all_array(j)
    f = open("arrayuse_slice_points.pkl", 'wb')
    pickle.dump(_dict, f, True)
    f.close()
    print(_dict)
    
    _dict = get_all_integeroverflow_point(j)
    f = open("integeroverflow_slice_points_new.pkl", 'wb')
    pickle.dump(_dict, f, True)
    f.close()
    '''
	
    
