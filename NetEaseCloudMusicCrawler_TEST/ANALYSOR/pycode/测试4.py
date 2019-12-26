def get_word_vector(path):
    ip = open(path, 'r', encoding='utf-8')
    content = ip.readlines()
    vecs = []

    for words in content:
        # vec = np.zeros(2).reshape((1, 2))
        vec = np.zeros(50).reshape((1, 50))
        count = 0
        words = remove_some(words)
        for word in words[1:]:
            try:
                count += 1
                # vec += model[word].reshape((1, 2))
                vec += model[word].reshape((1, 50))
                # print(vec)
            except KeyError:
                continue
        vec /= count
        vecs.append(vec)
    return vecs
