from mcstructure import Structure

def create_list(struct):
    block_count = {}

    for x in range(len(struct)):
        for y in range(len(struct[x])):
            for z in range(len(struct[x][y])):
                if struct[x][y][z].namespace_and_name[1] == 'air':
                    continue

                if struct[x][y][z].namespace_and_name[1] in block_count:
                    block_count[struct[x][y][z].namespace_and_name[1]] += 1
                else:
                    block_count[struct[x][y][z].namespace_and_name[1]] = 1

    return block_count

def main():

    print("hello")

    with open("./test_files/house.mcstructure", "rb") as f:
        struct = Structure.load(f)

    print(create_list(struct.get_structure()))








if __name__ == "__main__":
    main()