from Tools.scripts.texi2html import increment
from pynbt import BaseTag, NBTFile, TAG_Compound, TAG_Int, TAG_List, TAG_String
from typing import Any


# Turns an NBT tree into a python tree.
def _into_pyobj(tag: BaseTag) -> Any:

    if isinstance(tag, (TAG_Compound, dict)):
        res = {}
        for key, value in tag.items():
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res[key] = value
        return res

    if isinstance(tag, (TAG_List, list)):
        res = []
        for value in tag:
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res.append(value)
        return res

    if isinstance(tag, BaseTag):
        return tag.value

    return tag



def load(f):
    nbt = NBTFile(f, little_endian=True)
    indices = []
    palette = []
    for i in range(len(nbt['structure']['block_indices'][0])):
        indices.append(nbt['structure']['block_indices'][0][i].value)

    for j in range(len(nbt['structure']['palette']['default']['block_palette'])):
        palette.append([
            nbt['structure']['palette']['default']['block_palette'][j]['name'].value,
            _into_pyobj(nbt['structure']['palette']['default']['block_palette'][j]['states'].value)
        ])


    data = _into_pyobj(nbt['structure']['palette']['default']['block_position_data'])

    return indices, palette, data

def total(indices, palette, data):
    blocks = {}
    count = 0
    for i in indices:
        name = palette[i][0]
        inc = 1

        if str(count) in data:
            # try:
            #     temp = blocks[palette[i][0]]["data"]
            #     blocks[palette[i][0] + str(count)] = {"amount": 1}
            #     blocks[palette[i][0] + str(count)]["data"] = data[str(count)]
            # except KeyError:
            #     blocks[palette[i][0]]["data"] = data[str(count)]

            entity = data[str(count)]
            match name:
                case "minecraft:bed":
                    inc = 0.5
                    match entity['block_entity_data']['color']:
                        case 0:
                            name = "minecraft:white_bed"
                        case 1:
                            name = "minecraft:orange_bed"
                        case 2:
                            name = "minecraft:magenta_bed"
                        case 3:
                            name = "minecraft:light_blue_bed"
                        case 4:
                            name = "minecraft:yellow_bed"
                        case 5:
                            name = "minecraft:lime_bed"
                        case 6:
                            name = "minecraft:pink_bed"
                        case 7:
                            name = "minecraft:gray_bed"
                        case 8:
                            name = "minecraft:light_gray_bed"
                        case 9:
                            name = "minecraft:cyan_bed"
                        case 10:
                            name = "minecraft:purple_bed"
                        case 11:
                            name = "minecraft:blue_bed"
                        case 12:
                            name = "minecraft:brown_bed"
                        case 13:
                            name = "minecraft:green_bed"
                        case 14:
                            name = "minecraft:red_bed"
                        case 15:
                            name = "minecraft:black_bed"
                case "minecraft:standing_banner":
                    match entity['block_entity_data']['Base']:
                        case 0:
                            name ="minecraft_black_banner"
                        case 1:
                            name = "minecraft:red_banner"
                        case 2:
                            name = "minecraft:green_banner"
                        case 3:
                            name = "minecraft:brown_banner"
                        case 4:
                            name = "minecraft:blue_banner"
                        case 5:
                            name = "minecraft:purple_banner"
                        case 6:
                            name = "minecraft:cyan_banner"
                        case 7:
                            name = "minecraft:light_gray_banner"
                        case 8:
                            name = "minecraft:gray_banner"
                        case 9:
                            name = "minecraft:pink_banner"
                        case 10:
                            name = "minecraft:lime_banner"
                        case 11:
                            name = "minecraft:yellow_banner"
                        case 12:
                            name = "minecraft:light_blue_banner"
                        case 13:
                            name = "minecraft:magenta_banner"
                        case 14:
                            name = "minecraft:orange_banner"
                        case 15:
                            name = "minecraft:white_banner"
                case "minecraft:wall_banner":
                    match entity['block_entity_data']['Base']:
                        case 0:
                            name = "minecraft_black_banner"
                        case 1:
                            name = "minecraft:red_banner"
                        case 2:
                            name = "minecraft:green_banner"
                        case 3:
                            name = "minecraft:brown_banner"
                        case 4:
                            name = "minecraft:blue_banner"
                        case 5:
                            name = "minecraft:purple_banner"
                        case 6:
                            name = "minecraft:cyan_banner"
                        case 7:
                            name = "minecraft:light_gray_banner"
                        case 8:
                            name = "minecraft:gray_banner"
                        case 9:
                            name = "minecraft:pink_banner"
                        case 10:
                            name = "minecraft:lime_banner"
                        case 11:
                            name = "minecraft:yellow_banner"
                        case 12:
                            name = "minecraft:light_blue_banner"
                        case 13:
                            name = "minecraft:magenta_banner"
                        case 14:
                            name = "minecraft:orange_banner"
                        case 15:
                            name = "minecraft:white_banner"
                case "minecraft:smoker":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case "minecraft:chest":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case "minecraft:barrel":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case str(x) if 'shulker' in x:
                    if name == 'minecraft:undyed_shulker_box':
                        name = "minecraft:shulker_box"
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case "minecraft:glow_frame":
                    name = "minecraft:glow_item_frame"
                    if "Item" in entity['block_entity_data']:
                        if entity['block_entity_data']["Item"]["Name"] in blocks:
                            blocks[entity['block_entity_data']["Item"]["Name"]] += 1
                        else:
                            blocks[entity['block_entity_data']["Item"]["Name"]] = 1
                case "minecraft:frame":
                    name = "minecraft:item_frame"
                    if "Item" in entity['block_entity_data']:
                        if entity['block_entity_data']["Item"]["Name"] in blocks:
                            blocks[entity['block_entity_data']["Item"]["Name"]] += 1
                        else:
                            blocks[entity['block_entity_data']["Item"]["Name"]] = 1
                case "minecraft:dropper":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case "minecraft:hopper":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case "minecraft:chiseled_bookshelf":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case "minecraft:furnace":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case "minecraft:lectern":
                    if "book" in entity['block_entity_data']:
                        if "minecraft:book_and_quill" in blocks:
                            blocks['minecraft:book_and_quill'] += 1
                        else:
                            blocks['minecraft:book_and_quill'] = 1
                case "minecraft:dispenser":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case "minecraft:blast_furnace":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']
                case "minecraft:trapped_chest":
                    for item in entity['block_entity_data']['Items']:
                        if item['Name'] in blocks:
                            blocks[item['Name']] += item['Count']
                        else:
                            blocks[item['Name']] = item['Count']


        if name in blocks:
            blocks[name] += inc
        else:
            blocks[name] = inc

        count += 1

    del blocks['']
    for key in blocks.keys():
        blocks[key] = int(blocks[key])

    print(blocks)


with open('TestFiles/test22.mcstructure', 'rb') as f:
    a, b, c = load(f)
    total(a, b, c)