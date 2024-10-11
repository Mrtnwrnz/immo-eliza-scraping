import os

# put all urls into list, add quotes
path = os.path.join("data", "house_apt_url.csv")
all_urls = []
with open(path, "r") as f:
    for i in range(161669):
        line = f.readline()
        all_urls.append(f'"{line.strip()}"')

all_urls.pop(0)

# remove postal codes from abroad
all_urls = [i for i in all_urls if len(i.split("/")[-2]) == 4]

# save to new csv
output_path = os.path.join("data", "filtered_urls2.csv")
with open(output_path, "w") as f:
    f.write(",".join(all_urls))

# making a new file with first 1000 urls
input_path = os.path.join("data", "filtered_urls.csv")
new_output_path = os.path.join("data", "first_1000_urls.csv")
with open(input_path, "r") as input_file, open(new_output_path, "w") as output_file:
    for i in range(1000):
        line = input_file.readline()
        output_file.write(line)