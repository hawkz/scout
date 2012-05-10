# scout/folders.py
'''Support for quering a calendar.'''

def itercalendar(client,
                 user,
                 startDate,
                 endDate):
    '''Iterate over calendar items'''

    #
    # Create FindItem request.
    #

    find_item_request = client.factory.create('FindItemType')

    #
    # Specify what to return, in this case everything available, as text.
    #

    shape_types = client.factory.create('ns1:DefaultShapeNamesType')
    body_types = client.factory.create('ns1:BodyTypeResponseType')

    shape_type = client.factory.create('ns1:ItemResponseShapeType')
    shape_type.BaseShape = shape_types.AllProperties
    shape_type.BodyType = body_types.Text

    find_item_request.ItemShape = shape_type

    #
    # Specify how to traverse over items.
    #

    find_item_traversal_types = client.factory.create('ns1:ItemQueryTraversalType')
    find_item_request._Traversal = find_item_traversal_types.Shallow;

    #
    # Specify what user's calendar to look at. This can be any user provided
    # Exchange's permission model allows it.
    #

    folder_id_types = client.factory.create('ns1:DistinguishedFolderIdNameType')

    mailbox_types = client.factory.create('ns1:MailboxTypeType')
    mailbox = client.factory.create('ns1:EmailAddressType')
    mailbox.EmailAddress = user
    mailbox.MailboxType = mailbox_types.Mailbox

    folder_id_type = client.factory.create('ns1:DistinguishedFolderIdType')
    folder_id_type.Mailbox = mailbox
    folder_id_type._Id = folder_id_types.calendar

    folder_ids = client.factory.create('ns1:NonEmptyArrayOfBaseFolderIdsType')
    folder_ids.DistinguishedFolderId = folder_id_type

    find_item_request.ParentFolderIds = folder_ids

    # 
    # Limit results by date
    #

    calendar_view = client.factory.create('ns1:CalendarViewType')
    calendar_view._StartDate = startDate
    calendar_view._EndDate = endDate

    find_item_request.CalendarView = calendar_view

    # 
    # Must mark request as not-wrapped or suds will encode incorrectly.
    #

    client.service.FindItem.method.soap.input.body.wrapped = False

    find_item_response = client.service.FindItem(find_item_request)

    count = find_item_response.FindItemResponseMessage.RootFolder._TotalItemsInView

    if not count:
        return

    for (itemsType,items) in find_item_response.FindItemResponseMessage.RootFolder.Items:
        for item in items:
            if item.IsCancelled:
                continue

            #
            # Not all fields are present for all calendar searches
            # In particular, Location seems to missing for certain kinds
            # of events, but not for resource calendars...
            #

            #
            # For shared resource calendars, the subject and organizer
            # can end up being the same.
            #

            organizer = item.Organizer.Mailbox.Name and item.Organizer.Mailbox.Name.strip() or None
            subject = item.Subject and item.Subject.strip() or None
            location = item.Location and item.Location.strip() or None
            start = item.Start
            end = item.End
            all_day = item.IsAllDayEvent

            people = set()

            if item.DisplayTo:
                for name in item.DisplayTo.split(';'):
                    if name != location:
                        people.add(name.strip())

            if item.DisplayCc:
                for name in item.DisplayCc.split(';'):
                    people.add(name.strip())
                    
            yield (subject, organizer, location, start, end, all_day, people)



