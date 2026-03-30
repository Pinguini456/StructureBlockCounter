<div align="center">

<img src="https://img.shields.io/badge/Minecraft-Bedrock%20Edition-62B47A?style=for-the-badge&logo=minecraft&logoColor=white" alt="Minecraft Bedrock Edition"/>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"/>
<img src="https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey?style=for-the-badge" alt="CC BY-NC 4.0"/>

# Structure Block Counter (WIP)

### A powerful material list generator for Minecraft Bedrock Edition structures


</div>

---

## Overview

**Structure Block Counter** is a desktop application that parses Minecraft Bedrock Edition `.mcstructure` files and generates comprehensive material lists. Perfect for builders who need to calculate exact resource requirements for their creations.

### Key Features

- **NBT Parsing**: Deep analysis of structure files including container contents (chests, shulkers, furnaces, etc.)
- **Smart Calculations**: Automatic conversion to stacks and shulker boxes
- **Save & Load**: Store material lists for future reference
- **Beautiful UI**: Minecraft-styled interface with authentic fonts and item icons
- **Container Support**: Reads items from chests, barrels, shulker boxes, hoppers, droppers, dispensers, furnaces, smokers, blast furnaces, lecterns, item frames, and more
- **Block State Handling**: Properly identifies colored variants (beds, banners, signs) and legacy block IDs

---

## Screenshots

<div align="center">

| Main Window | Material List View |
|:---:|:---:|
| ![Main Window](https://via.placeholder.com/300x200?text=Main+Window) | ![Material List](https://via.placeholder.com/400x300?text=Material+List+View) |

</div>

---

## Installation

### Option 1: Download Pre-built Executable (Recommended)

1. Go to the **[Releases](https://github.com/yourusername/StructureBlockCounter/releases)** page
2. Download the latest `StructureBlockCounter.exe`
3. Run the executable — no installation required!

### Option 2: Run from Source

**Prerequisites:**
- Python 3.10 or higher
- Windows

**Steps:**
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/StructureBlockCounter.git
   cd StructureBlockCounter
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application
   ```bash
   python main.py
   ```

---

## Usage

### Generating a Material List

1. Launch the application
2. Click **Browse** to select your `.mcstructure` file
3. Enter a name for your build
4. Click **Count** to generate the material list

### Reading the Output

| Column | Description |
|--------|-------------|
| **Icon** | Visual representation of the item |
| **Name** | Formatted item name |
| **Stacks** | Total count in stack notation (e.g., "15 + 32" = 15 full stacks + 32 items) |
| **Shulkers** | Equivalent number of shulker boxes needed |

> **Note**: Stack calculations automatically adjust for unstackable items (tools, weapons, armor) and quarter-stackable items (signs, buckets, banners).

### Saved Builds

All material lists are automatically saved to the `SavedBuilds/` directory as JSON files. Access them anytime via **File → Load saved build**.

---

## Supported Block Entities

The application scans and counts items stored in:

- Chests (including trapped chests)
- Barrels
- Shulker Boxes (all colors)
- Furnaces, Smokers, Blast Furnaces
- Hoppers
- Droppers & Dispensers
- Item Frames & Glow Item Frames
- Chiseled Bookshelves
- Lecterns

---

## File Structure

```
StructureBlockCounter/
├── main.py              # Application entry point
├── window.py            # UI components and windows
├── parse.py             # NBT parsing and block counting logic
├── constant.py          # Item categorization data
├── fonts/               # Minecraft font assets
├── icons/               # Item icon textures
├── SavedBuilds/         # Saved material lists (JSON)
└── test_structures/     # Sample structure files
```

---

## How It Works

1. **File Selection**: User selects a `.mcstructure` file exported from Minecraft Bedrock Edition
2. **NBT Parsing**: The `pynbt` library reads the little-endian NBT data
3. **Block Analysis**: The parser iterates through:
   - Block indices and palette to count placed blocks
   - Block entity data to count stored items
4. **Name Correction**: Legacy block IDs and damage values are converted to modern names
5. **Beautification**: Results are formatted with proper capitalization and sorted by quantity
6. **Display**: Results shown in a scrollable, categorized list with icons

---

## Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

- Check if the issue already exists
- Include the structure file that causes the problem
- Provide your Python version and operating system

---

## Technical Details

### Supported NBT Structures

The parser handles Bedrock Edition's specific NBT format:

```python
structure: {
  block_indices: [...],
  palette: {
    default: {
      block_palette: [...],
      block_position_data: {...}
    }
  }
}
```

### Stack Size Logic

| Category | Stack Size | Examples |
|----------|------------|----------|
| Standard | 64 | Most blocks and items |
| Unstackable | 1 | Tools, weapons, armor, potions |
| Quarter | 16 | Signs, buckets, eggs, ender pearls, banners |

---

## Known Limitations

- Only supports **Bedrock Edition** `.mcstructure` files (Java Edition uses a different format)
- Entities (mobs, item frames with items) are partially supported
- Some legacy block IDs may not be recognized

---

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

**You are free to:**
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **NonCommercial** — You may not use the material for commercial purposes

[View full license](https://creativecommons.org/licenses/by-nc/4.0/)

---

## Acknowledgments

- **Minecraft** is a trademark of Mojang Studios. This project is not affiliated with Mojang.
- Built with [pynbt](https://github.com/Towster/pynbt) for NBT parsing
- All icons and custom artwork created specifically for this project

---

<div align="center">

Made by a Minecraft builder, for Minecraft builders

⭐ Star this repo if you find it useful! ⭐

</div>
