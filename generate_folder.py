import os, sys
import shutil
import csv

# obtain user input for number of partitions
num_partitions = int(raw_input("How many partitions do you need: "))
print(num_partitions)
print("")

# Paths to be created
paths = []
for i in range(num_partitions):
    paths.append("./partition-"+str(i+1))

# create new directory with 
for path in paths:
  try:
    os.mkdir(path, 0777);
    print("directory " + path + " is created")
  except:
    print("directory " + path + " existed already!")
print("")

# copy contents to the folders
for path in paths:
  for file in os.listdir("./"):
    # add credential files to each partition
    if file == "generate_folder.py":
      continue
    if os.path.isfile(file):
      shutil.copy(file,path)
      print(str(file)+" copied to " + path)
print("")

# update each partition's categories.csv file
num_categories = len(open("categories.csv").readlines())-1

# calculate category start line index for each partition
categories_per_partition = num_categories / num_partitions
missing_part = num_categories - categories_per_partition*num_partitions
categories_start_index = [0]
for i in range(1,num_partitions):
  categories_start_index.append(categories_start_index[i-1] + categories_per_partition)
if missing_part > categories_per_partition/2:
  categories_start_index[num_partitions-1] += missing_part

# create partition for the categories.csv file for each folder 
currentPartitionIdx = 0
for path in paths:
  filepath = os.path.join(path, "categories.csv")
  with open("./categories.csv") as inf, open(filepath, 'w') as outf:
      reader = csv.reader(inf, delimiter=',')
      writer = csv.writer(outf, delimiter=',', lineterminator='\n')
      line_num = 0
      for line in reader:
          if line_num == 0:
              writer.writerow(line)
          elif line_num > categories_start_index[currentPartitionIdx]:
            if currentPartitionIdx != num_partitions-1:
              if categories_start_index[currentPartitionIdx+1] < line_num:
                break
            writer.writerow(line)
          line_num += 1
  print(path+'/categories.csv ' + "is updated!")
  currentPartitionIdx+=1

# categories_per_partition = num_categories / num_partitions
# missing_part = num_categories - categories_per_partition*num_partitions
# categories_start_index = [1]
# for i in range(1,num_partitions):
#   categories_start_index.append(categories_start_index[i-1] + categories_per_partition)

# print(categories_start_index)
# if missing_part > categories_per_partition/2:
#   categories_start_index[num_partitions-1] += missing_part

# print(categories_start_index)