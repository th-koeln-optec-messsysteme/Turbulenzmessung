i = 0
previous_row = 0
my_List = []

with open('SondenDatenWichtig.csv') as file:
        for line in file:
              row_data = line.strip().split('\n')
              a = row_data[0]
              if str(a) == str(previous_row):
                  print(a)
                  i +=1
                  previous_row = a
              else:
                    my_List.append(str(row_data[0]))
                    previous_row = a
        print("Es gab " + str(i) + " Dopplungen")
        i = 0
        
with open ('New_Radiosonde.csv', 'w') as putIn:
      for attributes in my_List:
            putIn.writelines(attributes + '\n')
