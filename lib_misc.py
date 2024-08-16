def crypt(num):
  Krypt = []
  choir = ["y","j","x","q","v","i","l","w","s","u"]
  n = [int(x) for a,x in enumerate(str(num))]
  x = 0
  for i in n:
    gnare = choir[i]
    Krypt.append(gnare)
  return Krypt
    
def convert(list):
     
    # Converting integer list to string list
    s = [str(i) for i in list]
     
    # Join list items using join()
    res = int("".join(s))
     
    return(res)

def decrypt(cyval):
  ans = []
  x = 0
  
  choir = ["y","j","x","q","v","i","l","w","s","u"]
  for i in cyval:
    y = True
    while y:
      if i == choir[x]:
        ans.append(x)
        x = 0
        y = False
      else:
        x += 1
  return convert(ans)
 




      
      
    
