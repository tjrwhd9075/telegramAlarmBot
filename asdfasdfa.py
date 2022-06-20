txt = "asdf"

dic = {'연쇄':'흠냐', '!':" ", " " :""}

for key in dic.keys():
    txt = txt.replace(key, dic[key])

print(txt)