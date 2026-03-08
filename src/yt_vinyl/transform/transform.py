# gets unprocessed data

# transforms the data

# loads the data into silver

# updates the bronze table to confirm successfully processed

# think they should be in the same database then can commit to bronze and silver in the same tran
# different databases for different applications maybe

import re


def silver_transform(bronze_data: list[dict]) -> list[dict]:

    lst_of_dcts = []

    for dct in bronze_data:
        desc = dct["snippet"]["description"]

        tracklist_string = re.compile(r"\n\n(.*)", re.DOTALL).findall(desc)[0]

        tracklist_list = tracklist_string.split("\n")

        for track in tracklist_list:
            elements = track.split(" - ")
            if elements[0].isnumeric():
                lst_of_dcts.append(
                    {"Artist": elements[1].strip(), "Track": elements[2].strip()}
                )

    return lst_of_dcts
