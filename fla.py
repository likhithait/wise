def flatten_list(f_list):
    listed=[]
    for item in f_list:
        listed.append(item)
    print(listed)




nested_list=list(map(int,input("List: ").split(',')))
flatten_list(nested_list)