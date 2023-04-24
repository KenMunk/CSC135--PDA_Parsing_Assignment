'''
Modified by Kenneth Munk
CSC 135 Spring 2023 @ 10:30am
'''

class scanner:
    # toks[i] must evaluate to the i-th token in the token stream.
    # Assumes toks does not change during parsing
    def __init__(self,toks):
        self._toks = toks
        self._i = 0
    
    # If no more tokens exist or current token isn't s, raise exception.
    # Otherwise pass over the current one and move to the next.
    def match(self,s):
        if (self._i < len(self._toks)) and (self._toks[self._i] == s):
            self._i += 1
        else:
            raise Exception
            
    # If any tokens remain return the current one. If no more, return None.
    def next(self):
        if self._i < len(self._toks):
            return self._toks[self._i]
        else:
            return None


def appendToks(stack, toks):
    for x in range(len(toks)):
        indexVal = ((-1)*x)-1
        #print("Appending token: " + toks[indexVal])
        stack.append(toks[indexVal])

# Input can be any type where len(input) is defined and input[i] yields a
# string (ie, string, list, etc). Raises Exception on a parse error.
# S → <AB
# A → aAb | b
# B → bB | >
def parse1(input):
    toks = scanner(input)
    stack = ['S']
    while len(stack) > 0:
    
        tok = toks.next()      # None indicates token stream empty
        tokString = ""
        
        
        #print("'" + str(tok) + "' cmp $" + str(stack))
        
        top = stack.pop()      # Always pop top of stack
        
        #print(top)
        
        
        if top in ('a', 'b', '<', '>'):     # Matching stack top to token
            toks.match(top)
            #print("terminal found: " + top)
        elif top == 'S' and tok == '<':  # S -> aSa must be the next
            appendToks(stack,"<AB")
            '''
            stack.append('B')            # production to follow here
            stack.append('A')
            stack.append('<')
            '''
        elif top == 'A' and tok == 'a':  # S -> bSb must be the next
            appendToks(stack,"aAb")
        elif top == 'A' and tok == 'b':  # S -> x must be the next
            appendToks(stack,"b")
        elif top == 'B' and tok == 'b':  # S -> x must be the next
            appendToks(stack,"bB")
        elif top == 'B' and tok == '>':  # S -> x must be the next
            appendToks(stack,">")
        else:
            raise Exception    # Unrecognized top/tok combination
    if toks.next() != None:
        raise Exception


# Input can be any type where len(input) is defined and input[i] yields a
# string (ie, string, list, etc). Raises Exception on a parse error.
# S → BA
# A → +BA | -BA | λ
# B → DC
# C → *DC | /DC | λ
# D → a | (S)
def parse2(input):
    toks = scanner(input)
    stack = ['S']
    while len(stack) > 0:
        tok = toks.next()      # None indicates token stream empty
        #print("'" + str(tok) + "' cmp $" + str(stack))
        top = stack.pop()      # Always pop top of stack
        if top in ('a', '*', '/', '(', '+', '-', ')'):     # Matching stack top to token
            toks.match(top)
        elif top in ('A','C') and tok == None: # next == $ 
            pass # "pass" is how you say do nothing in Python
        elif top == 'S' and tok in ('a','('):  # S -> BA must be the next
            appendToks(stack,"BA")
        elif top == 'A' and tok in ('+','-'):  # S -> +BA must be the next
            appendToks(stack,str(tok)+"BA")
        elif top == 'C' and tok in ('+','-'):  # S -> +BA must be the next
            pass
        elif top == 'B' and tok in ('a','('):  # S -> BA must be the next
            appendToks(stack,"DC")
        elif top == 'C' and tok in ('*','/'):  # S -> +BA must be the next
            appendToks(stack,str(tok)+"DC")
        elif top == 'A' and tok in ('*','/'):  # S -> +BA must be the next
            pass
        elif top in ('A','C') and tok in ('(',')'):
            pass
        elif top == 'D' and tok == 'a':  # D -> a must be the next
            appendToks(stack,"a")
        elif top == 'D' and tok == '(':  # D -> (S) must be the next
            appendToks(stack,"(S)")
        else:
            raise Exception    # Unrecognized top/tok combination
    if toks.next() != None:
        raise Exception


'''

Making my work easier for testing the code

'''

def test1(input):
    try:
        parse1(input)
    except:
        print("Reject: " + input)
    else:
        print("Accept")

def test2(input):
    try:
        parse2(input)
    except:
        print("Rejected: " + input)
    else:
        print("Accept")


# The following is a trick to make this testing code be ignored
# when this file is being imported, but run when run directly
# https://codefather.tech/blog/if-name-main-python/
if __name__ == '__main__':
    #test1("<ab>") #reject case
    #test1("<aabb>") #reject case
    test1("<aabbb>")
    test1("<abbb>")
    #test1("<aaabbb>") #reject case
    #test1("<aabb>b>") #reject case
    test1("<aabbbb>")
    test1("<aaabbbb>")
    
    
    test2("a")
    test2("(a)")
    test2("a+a")
    test2("a-a")
    test2("(a)+a")
    test2("(a)-a")
    test2("a*a")
    test2("a/a")
    test2("a*(a)")
    test2("a/(a)")
    test2("(a)*a")
    test2("(a)/a")
    test2("a+a*a")
    test2("a-a*a")
    test2("a+a/a")
    test2("a-a/a")
    test2("a*(a*a)")
    test2("(a+a)*(a-a)")
    test2("(a+a)/(a*a)")
    test2("a*(a+a)+a")
    test2("a/(a-a)+a")
    test2("a*(a-a)*a")
    test2("a+(a*a)-a")
    test2("a*(a/(a+a))")
    test2("(a-a)*(a+a)")
    test2("a+(a/(a-a))")
    test2("a*(a+a)-a")