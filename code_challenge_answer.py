import os

#function for parsing the mempool csv file
def parse_mempool_csv():
    data = []
    d = {}
    count = 0
    with open('mempool.csv') as f:
        data = f.readlines()
    for line in data:
        count += 1
        tx_id, fee, weight, parents = line.strip().split(',')
        parents = parents.split(';')
        d[tx_id] = [count, fee, weight, False] + parents
    return d

#function for writing the desired tx_ids into the block.txt file
#I have used a greedy approach here to get the desired answer, the dynamic programming approach took considerably more amount of time than the greedy approach
def write_to_block(W, wgt, n):
    log = open("block.txt", "a")
    wgt = sorted(wgt)[::-1]
    weight = 0
    c = 0
    trans = []
    for i in wgt:
        c += i[0]
        weight += i[1]
        if weight > W:
            weight -= i[1]
            c -= i[0]
            break
        trans.append(i[2])
        log.write(i[2])
        log.write("\n")  
    log.close()
    
    
if __name__ == "__main__":
    log = open("data.txt", "a") 
    
    d = parse_mempool_csv()
    
    for i in d.keys():
        if d[i][-1] == '':
            d[i][3] = True
        else:
            flag = 0
            parents = d[i][4:]
            for parent in parents:
                if d[parent][0] > d[i][0]:
                    flag = 1
                    break
            if flag == 0:
                d[i][3] = True

    valid_transactions = []
    
    log.write("Valid transactions : \n")
    for i in d.keys():
        if d[i][3] == False:
            print(i)
        else:
            valid_transactions.append(i)
            log.write(i)
            log.write("\n")
    log.close()
    
    val = []
    weight = []
    
    for transaction in valid_transactions:
        weight.append((int(d[transaction][1]),int(d[transaction][2]), transaction))
    
    write_to_block(4000000, weight, len(weight))