import sys
p=print
d=[(ord((c:=m.split(" "))[0])-65,ord(c[1][0])-88) for m in sys.stdin.readlines()]
p(sum(1+b+3*((b-a+1)%3) for a,b in d))
p(sum(3*b+(1+(a+b+2)%3) for a,b in d))