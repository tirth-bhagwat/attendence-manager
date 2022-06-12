import matplotlib.pyplot as plt

# plt.bar(['1', '2'], [10, 4])
# plt.bar([['1','10'], ['2','20']], [[10,3], [4,9]])

fig, ax = plt.subplots()

b1=ax.bar([1-0.25,2-0.25], [10, 4],width=0.25)
b2=ax.bar([1,2], [2, 6],width=0.25)
b3=ax.bar([1+0.25,2+0.25], [3, 9],width=0.25)

ax.bar_label(b1)
ax.bar_label(b2)
ax.bar_label(b3)

plt.show()
