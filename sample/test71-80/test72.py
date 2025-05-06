#"Apple","banana","Cherry","lemon"
#という要素が入っているリストwordsがあります
#modify_wordsという関数を作成してください
#modify_words関数は文字列を一つの引数に受け取りその文字列を全て大文字に変換して返す関数です
#先頭の文字が大文字でない場合はそのままの文字列を返します
#modify_words関数を使ってwordsの各要素が変換された新しいリストを作成して出力してください

words=["Apple","banana","Cherry","lemon"]

#def modify_words(words, func):
#    for word in words:
##        print(func(word))

#def sample_func(word):
#    return word.capitalize()

#modify_words(words,sample_func)

def modify_words(word):
    first_char=word[0]
    if first_char.isupper():
        return word.upper()
    else:
        return word

modified_words=[]
for word in words:
    m_word=modify_words(word)
    modified_words.append(m_word)

print(modified_words)