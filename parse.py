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

def correct_item_names(data):
    name = ""
    match data['Name']:
        case "minecraft:banner":
            match data['Damage']:
                case 0:
                    name = "minecraft:black_banner"
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
        case "minecraft:bed":
            match data['Damage']:
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
        case "minecraft:undyed_shulker_box":
            name = "minecraft:shulker_box"
        case "minecraft:normal_stone_stairs":
            name = "minecraft:stone_stairs"
        case "minecraft:leather_chestplate":
            name = "minecraft:leather_tunic"
        case "minecraft:leather_helmet":
            name = "minecraft:leather_hat"
        case "minecraft:leather_leggings":
            name = "minecraft:leather_pants"
        case "minecraft:writable_book":
            name = "minecraft:book_and_quill"
        case _:
            name = data["Name"]

    return name


def beautify(struct: dict):
    new_struct = {}
    for key in struct.keys():
        meta = key.split(":")[1]
        words = meta.split("_")
        for i in range(len(words)):
            words[i] = words[i].capitalize()
        name = words[0]
        for j in range(len(words) - 1):
            name = name + " " + words[j + 1]

        new_struct[name] = struct[key]

    return {k: v for k, v in reversed(sorted(new_struct.items(), key=lambda item: item[1]))}




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
        item_name = ""

        if str(count) in data:

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
                            name ="minecraft:black_banner"
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
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']
                case "minecraft:chest":
                    for item in entity['block_entity_data']['Items']:
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']
                case "minecraft:barrel":
                    for item in entity['block_entity_data']['Items']:
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']
                case str(x) if 'shulker' in x:
                    if name == 'minecraft:undyed_shulker_box':
                        name = "minecraft:shulker_box"
                    for item in entity['block_entity_data']['Items']:
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']
                case "minecraft:glow_frame":
                    name = "minecraft:glow_item_frame"
                    if "Item" in entity['block_entity_data']:
                        item_name = correct_item_names(entity['block_entity_data']['Item'])
                        if item_name in blocks:
                            blocks[item_name] += 1
                        else:
                            blocks[item_name] = 1
                case "minecraft:frame":
                    name = "minecraft:item_frame"
                    if "Item" in entity['block_entity_data']:
                        item_name = correct_item_names(entity['block_entity_data']['Item'])
                        if item_name in blocks:
                            blocks[item_name] += 1
                        else:
                            blocks[item_name] = 1
                case "minecraft:dropper":
                    for item in entity['block_entity_data']['Items']:
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']
                case "minecraft:hopper":
                    for item in entity['block_entity_data']['Items']:
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']
                case "minecraft:chiseled_bookshelf":
                    if 'Items' in entity['block_entity_data']:
                        for item in entity['block_entity_data']['Items']:
                            item_name = correct_item_names(item)
                            if item_name in blocks:
                                blocks[item_name] += item['Count']
                            else:
                                blocks[item_name] = item['Count']
                case "minecraft:furnace":
                    for item in entity['block_entity_data']['Items']:
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']
                case "minecraft:lectern":
                    if "book" in entity['block_entity_data']:
                        if "minecraft:book_and_quill" in blocks:
                            blocks['minecraft:book_and_quill'] += 1
                        else:
                            blocks['minecraft:book_and_quill'] = 1
                case "minecraft:dispenser":
                    for item in entity['block_entity_data']['Items']:
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']
                case "minecraft:blast_furnace":
                    for item in entity['block_entity_data']['Items']:
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']
                case "minecraft:trapped_chest":
                    for item in entity['block_entity_data']['Items']:
                        item_name = correct_item_names(item)
                        if item_name in blocks:
                            blocks[item_name] += item['Count']
                        else:
                            blocks[item_name] = item['Count']

        match name:
            case "minecraft:normal_stone_stairs":
                name = "minecraft:stone_stairs"
            case "minecraft:waxed_copper":
                name = "minecraft:waxed_block_of_copper"
            case "minecraft:end_brick_stairs":
                name = "minecraft:end_stone_brick_stairs"
            case "minecraft:brick_block":
                name = "minecraft:bricks"
            case "minecraft:hay_block":
                name = "minecraft:hay_bale"
            case "minecraft:normal_stone_slab":
                name = "minecraft:stone_slab"
            case "minecraft:silver_glazed_terracotta":
                name = "minecraft:light_gray_glazed_terracotta"
            case "minecraft:lapis_block":
                name = "minecraft:block_of_lapis_lazuli"
            case "minecraft:hardened_clay":
                name = "minecraft:terracotta"
            case "minecraft:fence_gate":
                name = "minecraft:oak_fence_gate"
            case "minecraft:trapdoor":
                name = "minecraft:oak_trapdoor"
            case "minecraft:end_bricks":
                name = "minecraft:end_stone_bricks"
            case "minecraft:nether_brick":
                name = "minecraft:nether_bricks"
            case "minecraft:standing_sign":
                name = "minecraft:oak_sign"
            case "minecraft:darkoak_standing_sign":
                name = "minecraft:dark_oak_sign"
            case str(x) if 'standing_sign' in x:
                name = name[:-13]
                name = name + "sign"
            case "minecraft:wooden_pressure_plate":
                name = "minecraft:oak_pressure_plate"
            case "minecraft:unpowered_repeater":
                name = "minecraft:repeater"
            case "minecraft:powered_repeater":
                name = "minecraft:repeater"
            case "minecraft:unlit_redstone_torch":
                name = "minecraft:redstone_torch"
            case "minecraft:lit_redstone_lamp":
                name = "minecraft:redstone_lamp"
            case "minecraft:stonecutter_block":
                name = "minecraft:stonecutter"
            case "minecraft:unpowered_comparator":
                name = "minecraft:comparator"
            case "minecraft:powered_comparator":
                name = "minecraft:comparator"
            case "minecraft:target":
                name = "minecraft:target_block"
            case "minecraft:wooden_button":
                name = "minecraft:oak_button"
            case "minecraft:redstone_wire":
                name = "minecraft:redstone"
            case "minecraft:daylight_detector_inverted":
                name = "minecraft:daylight_detector"
            case "minecraft:snow_layer":
                name = "minecraft:snow"
            case "minecraft:melon_block":
                name = "minecraft:melon"
            case "minecraft:grass_path":
                name = "minecraft:dirt_path"
            case "minecraft:dirt_with_roots":
                name = "minecraft:rooted_dirt"
            case "minecraft:small_dripleaf_block":
                name = "minecraft:small_dripleaf"
            case "minecraft:quartz_ore":
                name = "minecraft:nether_quartz_ore"
            case "minecraft:azalea_leaves_flowered":
                name = "minecraft:flowering_azalea_leaves"
















        if name in blocks:
            blocks[name] += inc
        else:
            blocks[name] = inc

        count += 1

    if '' in blocks:
        del blocks['']
    if 'minecraft:air' in blocks:
        del blocks['minecraft:air']
    for key in blocks.keys():
        blocks[key] = int(blocks[key])

    return beautify(blocks)
