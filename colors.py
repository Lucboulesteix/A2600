import csv, os
os.chdir('C:/Users/lucco/Desktop/emulator project')

# Open the text file and read the contents
with open("TIA_color_raw.txt", "r") as file:
    text = file.read()

# Split the text into separate lines
lines = text.split("title=")

# Create an empty list to store the rows of the CSV file
rows = []
rows.append(("A2600 hex code NTSC", "RGB code"))

# Loop through each line
for line in lines:
    hex_idx = line.find(":")
    hex_end = line.find("/")
    RGB_idx = line.find("#")

    hex_code = line[hex_idx +2:hex_end];
    RGB_code = line[RGB_idx+1: RGB_idx + 7]
    rows.append((hex_code, RGB_code))

rows.remove(rows[1])

# Open a CSV file for writing
with open("colors.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Write the rows to the CSV file
    for row in rows:
        writer.writerow(row)
