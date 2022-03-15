import json
from collections import Counter
from collections import defaultdict

l1 = []
l2 = []
userId = {}
dict1 = defaultdict(list)

with open("train.json", 'r') as f:
    try:
        while True:
            temp = json.loads(f.readline())
            if temp:
                # print(temp)
                # print(temp['business_id'])
                # print(temp['review_id'])
                # print(temp['user_id'])
                # print(temp['text'])
                # print(temp['user_id'])
                l1.append(temp['user_id'])
                # if temp['user_id']=='IZXnSMdOkVdFH-mw6zQBbA':
                #     print(temp['business_id'])
                #     l1.append(temp['business_id'])
                    # print(temp['review_id'])
                    # print(temp['text'])
                    # print('--------------------')
            else:
                break
    except:
        f.close()

def findAllBusinessId(str):
    with open("train.json", 'r') as f1:
        try:
            while True:
                temp1 = json.loads(f1.readline())
                if temp1:
                    if temp1['user_id'] == str :
                        #print(temp1['business_id'])
                        l2.append(temp1['business_id'])
                        dict1[str].append(temp1['business_id'])
                else:
                    break
        except:
            f1.close()


def findSameBusinessId(str):
    #l3 = dict(Counter(dict1[str]))
    #print(dict1[str])
    #print(l3)
    print({value : count for value, count in Counter(dict1[str]).items() if count > 1})  # 展现重复元素和重复次数

userId = set (l1)
print(len(userId))
print(userId)

for i in userId:
    findAllBusinessId(i)
    findSameBusinessId(i)



