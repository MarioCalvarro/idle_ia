import matplotlib.pyplot as plt 

prod = 1
oro = 0
x = []
t = []

for i in range(900):
    t.append(i)
    oro += prod
    if i <= 900 - 15:
        prod += (oro / 15)
        x.append(oro / 15)
        oro = oro % 15
    else:
        x.append(0)



# plotting the points  
plt.plot(t, x) 
  
# naming the x axis 
plt.xlabel('t - axis') 
# naming the y axis 
plt.ylabel('x - axis') 
  
# giving a title to my graph 
plt.title('My first graph!') 
  
# function to show the plot 
plt.show() 

print(oro)
