# def even_fib(m):
#     a = 0
#     b = 1
#     lst = [0]
#     for _ in range(m):
#         a, b = b, a + b
#         lst.append(a)
#     print(lst)
#     x = sum(1 for value in lst[:-1] if value % 2 == 0 and value != 0)
#     return x
#
# print((even_fib(5)))




# def parts_sums(ls):
#     sums = [sum(ls)]
#     for i in ls:
#         sums.append(sums[-1]-i)
#     return sums

    #return [sum(ls[value:]) for value in range(len(ls) + 1)]
    #return [sum(ls[index:]) for index, value in enumerate(ls)] +[0]

# print(parts_sums([1, 2, 3, 4, 5, 6]))

#print(sum([1, 2, 3, 4, 5, 6][1:]))



# def digital_root(n):
#     a = n
#     while a >= 10:
#         a = sum(int(i) for i in str(a))
#     return a
#
# print(digital_root(10))


# def array_diff(a, b):
#     # lst = []
#     # for index in a:
#     #     if index not in b:
#     #         lst.append(index)
#     return [index for index in a if index not in b]
#
# print(array_diff([1, 2, 2, 2, 3], [1, 2]))


# def spin_words(sentence):
#     # Your code goes here
#     # lst = []
#     # a = sentence.split()
#     # for index in a:
#     #     if len(index) >= 5:
#     #         lst.append(index[::-1])
#     #     else:
#     #         lst.append(index)
#     return ' '.join([index[::-1] if len(index) >= 5 else index for index in sentence.split()])
#
# print(spin_words("Hey fellow warriors"))



# def generate_hashtag(s):
#     #your code here
#     #return '#' + s[0]
#     return '#' + ''.join((s.title().split())) if 0 < len(s) <= 140 else False
#
# print(generate_hashtag('CodeWars is nice'))


# def pig_it(text):
#     #your code here
#     # a = text.split()
#     # lst = []
#     # for index in a:
#     #     if index not in '!,?.':
#     #         b = index[1:] + index[0] + 'ay'
#     #         lst.append(b)
#     #     else:
#     #         lst.append(index)
#     return ' '.join(index[1:] + index[0] + 'ay' if index not in '!,?.' else index for index in text.split())
#
# print(pig_it('O tempora o mores !'))

a='ca'
b='dbaabbccdac'

count = 0

for index in b:
	if index in a:
		count += 1

print(count)