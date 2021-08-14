
def get_querys(file):
    with open(file, 'r', encoding = 'UTF-8') as f:
        querys = f.read().splitlines() 
    return querys

def find_query_line(name, file):
    i = 0
    querys = get_querys(file)

    for query in querys:
        i = i+1
        if query == name :
            return i
        
    return -1

def del_query(name, file):
    '''
    return -> 0 (fail 목록에 없음) / 1 (true 삭제 완료)
    '''
    if find_query_line(name, file) < 0: #목록에 없습니다
        return 0

    else : #목록에 있습니다. 삭제합니다
        with open(file,'rt', encoding = 'UTF-8') as f: 
            querys=f.read().splitlines()

        querys.sort()

        with open(file,'w', encoding = 'UTF-8') as f: 
            for query in querys: 
                if query != name: # 같으면 건너뜀
                    f.write(query + '\n')
        return 1

def add_query(name, file):
    '''
    return -> 0 (fail 이미 목록에 있음) / 1 (true 추가 완료)
    '''
    querys = get_querys(file)
    for query in querys:
        if query == name : # 목록에 있습니다
            return 0 # 저장안하고 종료

    with open(file, 'a', encoding = 'UTF-8') as f:         # 목록에 없습니다. 추가합니다.")
        f.write(name + "\n") 
        return 1 # 저장함