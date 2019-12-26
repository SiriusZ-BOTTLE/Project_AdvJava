with open('../../CSV/评论分词/word_vec_new1.txt', 'w',encoding='utf-8') as f:
    with open('../../CSV/评论分词/word_vec_new.txt', 'r',encoding='utf-8') as fp:

        flag=0
        for line in fp:
            for i in line:
                if i==',':
                    flag=1
                    break

            if flag==0:
                line = str(line).replace("\n", "")
                f.write(line)
            else:
                line = str(line).replace("\n", "")
                f.write('\n'+line)

            flag=0

