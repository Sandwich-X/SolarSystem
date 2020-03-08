total_list = [ [] ]
print("\ntotal_list =", total_list, "\n\n")
mult_list = [ [ 1, 2, 3 ],
              [ "a", "b", "c" ],
	            [ 10., 20. ],
	            [ True, False, None ]
	          ]
for add_list in mult_list:
  print("add_list =", add_list, ":\n")
  total_list = [ x1+[x2] for x1 in total_list for x2 in add_list ]
  print("total_list =", total_list, "\n\n")
