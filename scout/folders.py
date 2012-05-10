# scout/folders.py
'''Support for quering user folders.'''

def iterfolders(client):
    '''Iterate over available folders'''

    #
    # Create folder request and set up boilerplate.
    #

    find_folder_request = client.factory.create('FindFolderType')

    traversal_types = client.factory.create('ns1:FolderQueryTraversalType')

    shape_types = client.factory.create('ns1:DefaultShapeNamesType')
    folder_shape = client.factory.create('ns1:FolderResponseShapeType')
    folder_shape.BaseShape.value = shape_types.Default

    folder_id_types = client.factory.create('ns1:DistinguishedFolderIdNameType')
    parent_folder_ids = client.factory.create('ns1:NonEmptyArrayOfBaseFolderIdsType')
    parent_folder_ids.DistinguishedFolderId = client.factory.create('ns1:DistinguishedFolderIdType')
    
    #
    # Different folder types will give different results
    #

    parent_folder_ids.DistinguishedFolderId._Id = folder_id_types.root
    #parent_folder_ids.DistinguishedFolderId._Id = folder_id_types.msgfolderroot
    #parent_folder_ids.DistinguishedFolderId._Id = folder_id_types.searchfolders
    #parent_folder_ids.DistinguishedFolderId._Id = folder_id_types.publicfoldersroot

    #
    # Traversal type controls whether the output is recursive (Deep) or not (Shallow).
    # Recursive traversal is not allowed for all folder types (e.g. public folders).
    # 

    find_folder_request._Traversal = traversal_types.Shallow
    find_folder_request.FolderShape = folder_shape
    find_folder_request.ParentFolderIds = parent_folder_ids

    # 
    # Must mark request as not-wrapped or suds will encode incorrectly.
    #

    client.service.FindFolder.method.soap.input.body.wrapped = False

    find_folder_response = client.service.FindFolder(find_folder_request)
    
    root = find_folder_response.FindFolderResponseMessage.RootFolder
    num = root._TotalItemsInView

    if not num:
        # no folders
        return

    #
    # Folder type can include Folder, CalendarFolder, ContactsFolder, SearchFolder, TasksFolder
    # all of which may render slightly differently
    #

    for (folderType,rest) in root.Folders:
        if type(rest) == type([]):
            for folder in rest:
                yield folderType, folder.DisplayName
            else:
                yield folderType, rest.DisplayName
