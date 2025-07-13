from collections import defaultdict
text='Beckham and Oldman make the British honors list Soccer star David Beckham and actor Gary Oldman were knighted on June 14. The two are among some 1,200 people in King Charles III’s Birthday Honors list for this year. Former England soccer captain Beckham, 50, won the silver award for FIFA World Player of the Year in 1999 and 2001. Veteran actor Gary Oldman (67) won the Oscar for best actor for playing Winston Churchill in the 2017 film Darkest Hour.'
text_list=[s.strip('.').strip('(').strip(')').lower() for s in text.split()]
d=defaultdict(int)
for word in text_list:
    d[word]+=1
print(d)

group_a = ["A", "B", "C", "D"]
group_b = ["C", "D", "E", "F"]

not_in_b=[e for e in group_a if e not in group_b]
print(not_in_b)
print(set(group_a)&set(group_b))#両方
print(set(group_a)-set(group_b))#Aだけ
print(set(group_b)-set(group_a))#Bだけ