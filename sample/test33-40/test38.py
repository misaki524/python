#group_aは1,2,3,4,5の要素を持つ集合です
#group_bは4,5,6,7,8の要素を持つ集合です

#group_aとgroup_bを合わせた集合を作成してください


group_a={1,2,3,4,5}
group_b={4,5,6,7,8}
new_list=group_a | group_b
print(new_list)