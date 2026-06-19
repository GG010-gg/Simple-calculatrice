import math as m
from fractions import Fraction
#initialiser les caractères  (types)
chiffre="0123456789."
calc="/*-+%()^²"
equal="=><!"
alph="abcdefghijklmnopqrstuvwxyz"
eq=["or","and","nor","nand"]
mots=["abs","floor","ceil","round","sqrt","cos","sin","tan","acos","asin","atan"]
#décoder le calcul, renvoie les inconnues, leur valeur (donnée par l'utilisateur), les membres du calcul décodé : "3+2" renvoie ["3","+","2"]
def decode(value):
    term=[]
    for k,i in enumerate(value):
        if term==[]:
            if i=="-":term.append("0")
            term.append(i)
        elif value[k-1]==" ":term.append(i)
        else:
            last=str(term[len(term)-1])
            if i==" ":continue
            elif last[len(last)-1] in alph:
                if i in alph:term[len(term)-1]+=i
                else:term.append(i)
            elif last[len(last)-1] in calc:
                if last[len(last)-1]==")" and i in chiffre:term.append("*")
                if last[len(last)-1]=="("  and i =="-":term.append("0")
                if last[len(last)-1]=="-" and i in chiffre:
                    x=term[len(term)-2]
                    if x[len(x)-1] in chiffre or x[len(x)-1] in alph:term.append(i)
                    else:term[len(term)-1]+=i
                else:term.append(i)
            elif last[len(last)-1] in chiffre:
                if i=="(":
                    if last[len(last)-1] in chiffre:term.append("*")
                if i in chiffre:term[len(term)-1]+=i
                elif i in alph:term.append("*");term.append(i)
                else:term.append(i)
            elif last[len(last)-1] in equal:
                if i in equal:term[len(term)-1]+=i
                else:term.append(i)
    inc=inconnues(term);vinc=[0]*len(inc)
    if inc!=[]:
        for i in range(len(inc)):
            vinc[i]=input("Entrez la valeur de l'inconnue "+inc[i]+" : ")
        i=0
        while i<len(term):
            if term[i]=="pi":term[i]=pi
            elif term[i] in inc:
                term[i]=vinc[inc.index(term[i])]
                if i>0:
                    if term[i-1]==")" or term[i-1][len(term[i-1])-1] in chiffre:
                        term.insert(i,"*")
                elif i<len(term):
                    if term[i+1]=="(" or term[i+1][len(term[i+1])-1] in chiffre:
                        term.insert(i+1,"*")
            i+=1
    d=["1"]*len(term)
    return(term,d,inc,vinc)
#effectuer l'opération
def text(n1,n2,v,d1,d2):
    if v=="sqrt": return(False,m.sqrt(float(n2)/float(d2)),1)
    if v=="cos": return(False,m.cos(float(n2)/float(d2)),1)
    if v=="sin": return(False,m.sin(float(n2)/float(d2)),1)
    if v=="tan": return(False,m.tan(float(n2)/float(d2)),1)
    if v=="acos": return(False,m.acos(float(n2)/float(d2)),1)
    if v=="asin": return(False,m.asin(float(n2)/float(d2)),1)
    if v=="atan": return(False,m.atan(float(n2)/float(d2)),1)
    if v=="floor": return(False,m.floor(float(n2)/float(d2)),1)
    if v=="ceil": return(False,m.ceil(float(n2)/float(d2)),1)
    if v=="round": return(False,round(float(n2)/float(d2)),1)
    if v=="abs": return(False,abs(float(n2)),abs(float(d2)))
    x=float(d1)
    ne1=float(n1)*float(d2)
    nd=float(d1)*float(d2)
    ne2=float(n2)*x
    if v=="^": return(True,pow(float(n1)/float(d1),float(n2)/float(d2)),nd)
    if v=="+" or v=="-":
        nu1,de1=simplifier(n1,d1)
        nu2,de2=simplifier(n2,d2)
        if v=="+":return(True,nu1*de2+nu2*de1,de1*de2)
        else:
            return(True,nu1*de2-nu2*de1,de1*de2)
    if v=="*":return(True,float(n1)*float(n2),float(d1)*float(d2))
    if v=="/":return(True,float(n1)*float(d2),float(n2)*float(d1))
    if v=="%":
        mod=abs(float(ne1))%abs(float(ne2))
        if ne1<0 or ne2<0:
            if not (ne1<0 and ne2<0):mod*=-1
        return(True,mod,nd)
    if v=="=": return(True,0+(ne1==ne2),1)
    if v=="!=": return(True,0+(float(ne1)!=float(ne2)),1)
    if v=="<=": return(True,(float(ne1)<=float(ne2))+0,1)
    if v==">=": return(True,(float(ne1)>=float(ne2))+0,1)
    if v=="<": return(True,0+(float(ne1)<float(ne2)),1)
    if v==">": return(True,0+(float(ne1)>float(ne2)),1)
    if v=="and": return(True,0+(float(ne1) and float(ne2)),1)
    if v=="or": return(True,0+(float(ne1) or float(ne2)),1)
    if v=="nor": return(True,1-(float(ne1) or float(ne2)),1)
    if v=="nand": return(True,1-(float(ne1) and float(ne2)),1)
#modifier la liste une fois le sous-calcul effectué
def val(k,v,p,p_d):
    if k==0:n1=0;d1=1
    else:n1=p[k-1];d1=p_d[k-1]
    if k==len(p)-1:n2=1;d2=1
    else:n2=p[k+1];d2=p_d[k+1]
    r1,res,resd=text(n1,n2,v,d1,d2)
    p.pop(k+1);p_d.pop(k+1)
    p[k]=str(res);p_d[k]=str(resd)
    if r1:p.pop(k-1);p_d.pop(k-1)
    return p,p_d
#effectuer un calcul (sans parenthèses)
#l'ordre de priorité est respecté, et on scanne vers l'avant pour éviter des erreurs
def calcul(p,p_d):
    k=0
    while k<len(p):
        if p[k]=="-" and (k==0 or p[k-1] in (calc+equal)):
            p[k+1]=str(-float(p[k+1]))
            p.pop(k)
            p_d.pop(k)
        else:
            k+=1
    for k in range(len(p)-1,-1,-1):
        v=p[k]
        if not v in eq and v and v[0] in alph or v == "^":
            p,p_d=val(k, v, p,p_d)
    k=0
    while k<len(p):
        v=p[k]
        if v in ["/","*","%"]:
            p,p_d=val(k, v, p,p_d)
        else:
            k+=1
    k=0
    while k<len(p):
        v=p[k]
        if v in ["+","-"]:
            p,p_d=val(k, v, p,p_d)
        else:
            k+=1
    boleen_type=0;k=0
    while k<len(p):
        v=p[k]
        vd=p_d[k]
        if v[0] in equal:# =;<;>
            p,p_d=val(k, v, p,p_d)
            boleen_type=1
        else:k+=1
    k=0
    while k<len(p):
        v=p[k]
        vd=p_d[k]
        if v in eq:#or, and, nor, nand
            p,p_d=val(k, v, p,p_d)
            boleen_type=1
        else:k+=1
    return (str(p[0]),boleen_type,str(p_d[0]))
def simplifier(nu, de):#simplifier une fraction avec le module Fraction (le coder en dur aurait été fastidieux)
    f1=Fraction(nu);f2=Fraction(de);f=f1/f2;return f.numerator,f.denominator
def inconnues(term):#chercher les inconnues (texte pas recensé)
    inc=[]
    for i in term:
        if i[len(i)-1] in alph:
            if not (i in eq or i in mots):
                if not i in inc:
                    inc.append(i)
    return inc
def calculer(value,term,d,inc,vinc):
    if term!=[]:#Scanner toutes les parenthèses pour envoyer son contenu dans la parenthèse à la fonction calcul()
        while ")" in term:
            i=0
            p,p_d=[],[]
            while i<len(term) and term[i] !=")":
                i+=1
            if i==len(term):
                print("Erreur : parenthèse fermante manquante");return
            term.pop(i)
            d.pop(i)
            i-=1
            while i>=0 and term[i]!="(":
                p.append(term[i]);p_d.append(d[i])
                term.pop(i)
                d.pop(i)
                i-=1
            if i<0:print("Erreur : parenthèse ouvrante manquante");return
            term.pop(i);d.pop(i);p.reverse();p_d.reverse()
            resf,bol,df=calcul(p, p_d);term.insert(i,resf);d.insert(i,df)
    resf,bol,df=calcul(term,d)#une fois toutes les parenthèses supprimées, calcul final
    resf,df=simplifier(resf,df)
    resf,df=str(resf),str(df)
    #retour du résultat, boléen ou non
    if bol:
        if float(resf)/float(df):
            print(value+" is True")
        else:
            print(value+ " is False")
    elif df=="1":
        print(value+" = "+resf)
    elif df=="-1":
        print(value+" = "+str(-int(resf)))
    else:
        print(value+" = "+resf +"/"+ df)
        print(f"≈{int(resf)/int(df):.5f}")
def ca(value):
    #éxécute les fonctions
    term,d,inc,vinc=decode(value)
    calculer(value,term,d,inc,vinc)
    return(inc,vinc)
value=input("Entrer le calcul : ")
inc,vinc=ca(value)
while True:#boucle
    if inc==[]:
        print("----------------------")
        value=input("Entrer le calcul : ")
    else:
        c=input("Entrer un nouveau calcul (Enter) ou modifier les inconnues (M) ? ")
        if c!="M":
            print("----------------------");value=input("Entrer le calcul : ")
    inc,vinc=ca(value)