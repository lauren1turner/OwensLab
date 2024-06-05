# Lauren Turner (npa5gv)
# Owens Lab -- Transponder Reprogramming

# Put the name of the existing/most recent master MAP file and deleted file
master = "Owens Lab Master yyyy_mm_dd.MAP"
deleted = "yyyy-mm-dd-deleted Transponders.txt"

# This will convert the raw file into a list
deleted_handle = open(deleted, 'r')
deleted_contents = deleted_handle.read()
deleted_list = deleted_contents.strip().split('\n')

master_handle = open(master, 'r')
master_contents = master_handle.read()
master_list = master_contents.strip().split('\n')

# Input the name of the new master file with all transponders deleted
#   Example: 'Owens Lab Master 2024_05_23.MAP'
final_master = 'Owens Lab Master yyyy_mm_dd.MAP'


def remove_repeated_deleted(raw_deleted):
    """
    This function serves to get rid of any duplicates of transponders that were scanned twice in the deleting process,
    and it will also remove any null transponders that have already been cleared (NO MAP FOUND).
    :param raw_deleted: The deleted list created at the top of the program (deleted_list) will be the input.
    :return: This will return a new deleted list that contains no repetitions or null transponders (corrected_deleted).
    """
    unique_items = set()
    repeated_items = set()
    seen_items = set()
    nulls = set()

    for item in raw_deleted:
        if item in seen_items:
            repeated_items.add(item)
        if "NO MAP FOUND" in item:
            nulls.add(item)
        else:
            unique_items.add(item)
            seen_items.add(item)

    return unique_items, len(unique_items), list(repeated_items), list(nulls)


corrected_deleted, unique_deleted_number, repeated_delete, null_delete = remove_repeated_deleted(deleted_list)


def remove_repeated_master(raw_master):
    """
    This function serves to get rid of any duplicates of transponders that were scanned twice, and it will also remove
    any null transponders that have already been cleared (NO MAP FOUND).
    :param raw_master: The master list created at the top of the program (master_list) will be the input.
    :return: This will return a new master list that contains no repetitions or null transponders (unique_master).
    """
    unique_items = set()
    repeated_items = set()
    seen_items = set()
    nulls = set()

    for item in raw_master:
        if item in seen_items:
            repeated_items.add(item)
        if "NO MAP FOUND" in item:
            nulls.add(item)
        else:
            unique_items.add(item)
            seen_items.add(item)

    return unique_items, len(unique_items), list(repeated_items), list(nulls)


unique_master, unique_master_number, repeated_mas, null_mas = remove_repeated_master(master_list)


def remove_old_ids(raw_master2):
    """
    This serves to catch any human error from previous files in which there may be 2 Mouse ID numbers to
    the same transponder.
    :param raw_master2: The new list created by the remove_repeated_master function (unique_master) will be the input.
    :return: This will return a corrected master file that should have only the most recent Mouse ID
    for each transponder.
    """
    # Dictionary to store the highest number item for each prefix
    most_recent = {}
    # Set to keep track of prefixes with duplicates
    duplicates = set()

    for transponder in raw_master2:
        # Extract the prefix (first 10 characters) and the number (after the last space)
        prefix = transponder[:10]
        number = int(transponder.split()[-1])

        # Check if the prefix is already in the dictionary
        if prefix in most_recent:
            # Compare the current item number with the stored one
            current_number = int(most_recent[prefix].split()[-1])
            if number > current_number:
                most_recent[prefix] = transponder
            # Indicate that a duplicate was found
            duplicates.add(prefix)
        else:
            most_recent[prefix] = transponder

    # Return the list of the highest items for each prefix and the set of duplicates
    return list(most_recent.values()), duplicates


corrected_master, duplicates = remove_old_ids(unique_master)


def delete_transponders(master_file, del_file):
    """
    This serves to remove the transponders in the deleted file from the master file.
    :param master_file: The master list created from the remove_old_ids function (corrected_master) will be the input.
    :param del_file: The deleted list created from the remove_repeated_deleted function (corrected_deleted).
    :return: This will return either a success message if everything ran as expected or an error message if
    something goes wrong with the files. It will also create a new master file that can be named at the top of
    the program under the variable final_master.
    """
    # Extract prefixes from the small list
    deleted_prefixes = set(item[:10] for item in del_file)

    # Filter big_list and small_list based on the presence of prefixes in small_list
    master_updated = [
        item for item in master_file
        if item[:10] not in deleted_prefixes
    ]
    # Sort the list into numeric order by Mouse ID #
    master_updated.sort(key=lambda x: int(x[20:]))

    # calculate lengths
    master_length = len(master_file)
    deleted_length = len(del_file)
    difference = master_length - deleted_length
    updated_length = len(master_updated)
    erased_length = master_length - updated_length

    if difference != updated_length:
        print("\033[91mOops! There were "+str(deleted_length)+" transponders, but "+str(erased_length) +
              " were deleted from the master file.\033[0m")
    elif difference == updated_length:
        print("\033[92mSuccess! "+str(erased_length)+" transponders were deleted.\033[0m")

    # write file for new master
    with open(final_master, 'w') as new_master:
        for transponder in master_updated:
            new_master.write(f"{transponder}\n")

    return master_updated


# Remove items from both lists that have matching prefixes in duplicates
final = delete_transponders(corrected_master, corrected_deleted)
