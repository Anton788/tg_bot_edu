import sqlite3
import parsering
import dateparser
import matplotlib.pyplot as plt
import collections


def describe_topic(name):
    cursor.execute('SELECT DISTINCT title_t, title_doc, url_doc, doc_text'
                   ' from (ITEM INNER JOIN DOC ON ITEM.url = DOC.main_url) as X'
                   ' WHERE title_t = ?', (name, ))
    characters = dict()
    doc_text = list()
    count_words = collections.Counter()
    info = cursor.fetchall()
    freq = collections.Counter()
    for i in info:
        doc_text.append(i)
    for doc_data in doc_text:
        number_word = 0
        generator_of_words = generator_word(doc_data[3])
        for words in generator_of_words:
            freq[words] += 1
            number_word += 1
        count_words[(str(doc_data[1]), doc_data[2])] = number_word
    sum_all_count_words = 0
    diagram = plt.figure()
    x = [j for j in freq.keys()]
    y = [j for j in freq.values()]
    plt.title("Frequence")
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.xticks(rotation="vertical")
    plt.bar(x[:40], y[:40], label = "first", color = 'g')
    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.savefig('my.png')
    for i in count_words.values():
        sum_all_count_words += i
    return ((sum_all_count_words / len(count_words)), len(info))


def generator_word(line1):
    nword = ''
    for i in line1:
        if ord(i) >= 192 and i != '–' and i != '…':
            nword += i
            nword = nword.lower()
        if (ord(i) < 192 or i == line1[len(line1) - 1]) and nword != '':
            yield nword
            nword = ''


def top_n(count):
    cursor.execute('SELECT title_doc'
               ' from (select title_doc, url_doc, time, data'
               ' from DOC ORDER BY data DESC, time ASC LIMIT {}) as X'.format(count))
    return cursor.fetchall()


def top(n):
    cursor.execute('SELECT title_t '
                   'FROM ITEM LIMIT {}'.format(n))
    return cursor.fetchall()

conn = sqlite3.connect('new_database.db', check_same_thread=False)
cursor = conn.cursor()

if __name__ == '__main__':
    item_table_data = parsering.get_main_titles()
    doc_table_data = parsering.finally_parse()

    cursor.execute(''' DROP TABLE IF EXISTS ITEM''')
    cursor.execute('''DROP TABLE IF EXISTS DOC''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ITEM(
        url text, title_t text, description text
        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS DOC (
        main_url text, title_doc text, url_doc text,
        data text, time text, doc_text text, tags text)''')

    for i in item_table_data:
        a = i.title
        b = i.description
        c = i.url
        t = (c, a, b)
        cursor.execute('''INSERT INTO ITEM
                          VALUES (?, ?, ?)''', t)

    for i in doc_table_data:
        for k in i:
            for doc in k:
                data_time = doc.data
                data = str(dateparser.parse(data_time))
                data = data.split()
                z = (doc.main_url, doc.title, doc.url, data[0], data[1], doc.text, str(doc.tags))
                cursor.execute('''INSERT INTO DOC
                                VALUES (?, ?, ?, ?, ?, ?, ?)''', z)
    #top(4)
    #describe_topic('ПМЭФ-2018')
    conn.commit()
