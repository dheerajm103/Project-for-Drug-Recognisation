



def Nerdata_Final():
    
   # from flask import Flask,render_template,url_for,request
    import re
    import pandas as pd
    import spacy
    from spacy import displacy
    import en_core_web_sm
    nlp = spacy.load('en_core_web_sm')


    
    ################
    
    import re
    import pandas as pd
    import textract
    import spacy
    ner=spacy.load('en_core_med7_lg')
    #spacy.util.set_data_path('C:\Users\DELL\anaconda3\Lib\site-packages\spacy')
    
    text_doc=[]
    docs=['H:/vrenv/project 59/data/27-30(1).docx','H:/vrenv/project 59/data/27-30(2).docx',
      'H:/vrenv/project 59/data/27-30.docx','H:/vrenv/project 59/data/888-97(1).docx',
      'H:/vrenv/project 59/data/888-97.docx','H:/vrenv/project 59/data/888-896.docx',
      'H:/vrenv/project 59/data/603913.docx']
    for i in docs:
        text = textract.process(i)
        text = text.decode("utf-8") 
        text_doc.append(text)
    
    text_doc[0].index('REFERENCES')
    text_doc[1].index('REFERENCES')
    text_doc[2].index('REFERENCES')
    text_doc[3].index('References')
    text_doc[4].index('References')
    text_doc[5].index('References')
    text_doc[6].index('References')
    
    
    
    
    text_doc[0]=text_doc[0][0:6593]
    
    text_doc[1]=text_doc[1][0:6594]
    
    text_doc[2]=text_doc[2][0:6599]
    
    text_doc[3]=text_doc[3][0:33751]
    
    text_doc[4]=text_doc[4][0:33791]
    
    text_doc[5]=text_doc[5][0:37506]
    
    text_doc[6]=text_doc[6][0:16930]
    
    
    df=pd.DataFrame(text_doc,columns=['text'])
    df=df.loc[[0,3,5,6],['text']]
    df=df.reset_index(drop=True)
    df['text']=df['text'].apply(lambda x:re.sub(r'[^a-zA-Z.\n]',' ',x))
    #df
    ls=[]
    for i in range(len(df['text'])):
       ls.append(''.join(df['text'][i]))               
    
    ####################### sent wise ##################
    
   
    ############################
    
    # word tokenize
    from nltk.tokenize import word_tokenize
    wordss=[]
    for i in range(len(ls)):
        wordss.append(word_tokenize(ls[i]))

##############################################

    # lemmatization and Stopwords
    from nltk.corpus import stopwords
    from nltk import WordNetLemmatizer
    lem=WordNetLemmatizer()
    #wds=[]
    dfstrng=' '.join([lem.lemmatize(worod) for i in range(len(wordss)) for worod in wordss[i] if str(worod).isdigit() is not True and worod.lower() not in set(stopwords.words('english'))])
        
####################################################
    
    #NAME PERSON ORGExtraction with paragraph
    GPE={}
    PERSON={}
    ORG={}
    
    name=spacy.load('en_core_web_sm')
    name_doc=name(dfstrng)
    for i in name_doc.ents:
        if i.ents[0].label_=='GPE':
            GPE[i.text]=i.ents[0].label_
            
        if i.ents[0].label_=='PERSON':
            PERSON[i.text]=i.ents[0].label_  
          
        if i.ents[0].label_=='ORG':
            ORG[i.text]=i.ents[0].label_    
 #########################################

    

###########################################3
    ls_sent=str(ls).split('\\n\\n')
    
    #NAME PERSON ORG Extraction with sent_tokenize
    GPE_sent={}
    PERSON_sent={}
    ORG_sent={}
    
    name=spacy.load('en_core_web_sm')
    for j in range(len(ls_sent)):
        sent_doc=name(ls_sent[j])
        for i in sent_doc.ents:
            if i.ents[0].label_=='GPE':
                GPE_sent[i.text]=i.ents[0].label_
    
            if i.ents[0].label_=='PERSON':
                PERSON_sent[i.text]=i.ents[0].label_  
    
            if i.ents[0].label_=='ORG':
                ORG_sent[i.text]=i.ents[0].label_
    #######################################################
    
    
    #DISEASE AND CHEMICAL extraction with paragraph
    DISEASE={}
    CHEMICAL={}
    
    DIS_CHEM=spacy.load('en_ner_bc5cdr_md')
    dis_doc=DIS_CHEM(dfstrng)
    for i in dis_doc.ents:
        if i.ents[0].label_=='DISEASE':
            DISEASE[i.text]=i.ents[0].label_
            
        if i.ents[0].label_=='CHEMICAL':
            CHEMICAL[i.text]=i.ents[0].label_  
          
      
###########################################################

    #DISEASE CHEMICAL Extraction with sent_tokenize
    DISEASE_sent={}
    CHEMICAL_sent={}
    
    
    dis_sent=spacy.load('en_ner_bc5cdr_md')
    for j in range(len(ls_sent)):
        sent_disease=dis_sent(ls_sent[j])
        for i in sent_disease.ents:
            if i.ents[0].label_=='DISEASE':
                DISEASE_sent[i.text]=i.ents[0].label_
            
            if i.ents[0].label_=='CHEMICAL':
                CHEMICAL_sent[i.text]=i.ents[0].label_   
    
################################################################



    chm={}
    for c,v in CHEMICAL_sent.items():
        if len(c)>4 and '.' not in c and ' ' not in c:
            chm[c]=v
        
###################################################################

    
    
    drugs={}
    Strengths={}
    dosage={}
    med=ner(dfstrng)
    for i in med.ents:
        if i.ents[0].label_=='DRUG':
            drugs[i.text]=i.ents[0].label_
        
        
        if i.ents[0].label_=='STRENGTH':
            Strengths[i.text]=i.ents[0].label_
            
        if i.ents[0].label_=='DOSAGE':
            dosage[i.text]=i.ents[0].label_
#######################################################################
    
    #DISEASE CHEMICAL Extraction with sent_tokenize
    drugs_sent={}
    Strengths_sent={}
    dosage_sent={}
    
    
    for j in range(len(ls_sent)):
        sent_med=ner(ls_sent[j].lower())
        for i in sent_med.ents:
            if i.ents[0].label_=='DRUG' and " " not in i.text:
                drugs_sent[i.text]=i.ents[0].label_
            
            if i.ents[0].label_=='STRENGTH' and " " not in i.text:
                Strengths_sent[i.text]=i.ents[0].label_   
                
            if i.ents[0].label_=='DOSAGE' and " " not in i.text:
                dosage_sent[i.text]=i.ents[0].label_
    
    
#########################################################################

    
    drugsls=' '.join(i.title() for i in drugs).split()
    drugsls=[i for i in drugsls if len(i)>3]


#########################################################3

    CHEM=' '.join(i.title() for i in CHEMICAL.keys() if len(i)>3).split()
    CHEM=[i for i in CHEM if len(i)>3]

#####################################################################3
#df_drug.to_csv('H:/vrenv/project 59/drug.csv',encoding='utf-8')
    df_drug_=pd.read_csv('H:/vrenv/project 59/drug.csv')

    drgmatch=[]
    for idx,i in enumerate((drugsls)):
        for j in list(df_drug_['drugs'].values):
            if i in j:
                 drgmatch.append(i)

##########################################################################

    drgmatch=list(set(drgmatch))

###################################################################
    
    chemdrg=[]
    for idx,i in enumerate((CHEM)):
        if i in list(df_drug_['drugs'].values):
            chemdrg.append(i)

        
    chemdrg=[i for i in list(set(chemdrg)) if len(i)>4]
    chemdrg

###################################################################

    df_drug_['drugs'].apply(lambda x:('yes' if x=='Bolus' else 'NO')).unique()

    ls=re.sub(r"[^a-zA-Z]"," ",str(ls))
    wordsz=word_tokenize(ls)
    from nltk.corpus import stopwords
    wordsz=[i for i in wordsz if i.lower() not in stopwords.words('english')]
    
    wordsz=[i for i in wordsz if len(i)>4]
    ########################################################
    
    wrdchm={}
    wrddisese={}
    for i in wordsz:
        chmwrd=dis_sent(i.lower())
        for i in chmwrd.ents:
            if i.ents[0].label_=='CHEMICAL':
                wrdchm[i.text]=i.ents[0].label_
            
            if i.ents[0].label_=='DISEASE':
                wrddisese[i.text]=i.ents[0].label_
          #####################################################
    
    cln=set()
    wrdchm1={}
    for i in wrdchm:
        nv=name(i.upper())
        for j in nv.ents:
            cln.add(j.text)
            for k in ner(j.text).ents:
                wrdchm1[k.text]=k.ents[0].label_
    
    ################################################
    
    wrdchm2={}
    for i in wrdchm.keys():
        for j in ner(i.upper()).ents:
            if j.ents[0].label_=='DRUG':
                wrdchm2[j.text]=j.ents[0].label_
                #if name(j.text.capitalize()).ents:
                 #   print(name(j.text.capitalize()).ents[0])
       ##############################################          ##################

    #cleaned imp
    wrdchm2=list(filter(lambda x:x not in ('SINFERIOR','INSTITUTO','PROPOR','CONSE','ZUBIRAN','NPRESERVED','BINED','MOGRAPHY','STRAUER','PERCUTA','INTEROB','THROM','NSTANDARD','NBASELINE','NPROVED','GORIES','TOPCARE','IRCCS','TROLS','TRANSCRIP', 'NCONTROLS', 'NACCOMPANIED',) ,list(wrdchm2.keys())[3:]))
    
    import numpy as np
    wrdchm2=list(set(wrdchm2).union(set(chemdrg)))
    wrdchm2=list(np.unique(wrdchm2))
    wrdchm2=list(set(list(map(lambda x : x.capitalize() ,wrdchm2))))
    
    
    
#################################################################
    
    text_doc11=[]
    text_doc12=[]
    text_doc13=[]
    text_doc14=[]
    #docs11=[
    #  'H:/vrenv/project 59/data/27-30.docx',
    #  'H:/vrenv/project 59/data/888-97.docx','H:/vrenv/project 59/data/888-896.docx',
    #  'H:/vrenv/project 59/data/603913.docx']
    text11 = textract.process('H:/vrenv/project 59/data/27-30.docx')
    text11 = text11.decode("utf-8") 
    text_doc11.append(text11)
    #########################################################################
    text12 = textract.process('H:/vrenv/project 59/data/888-97.docx')
    text12 = text12.decode("utf-8") 
    text_doc12.append(text12)
    
    #########################################################################
    text13 = textract.process('H:/vrenv/project 59/data/888-896.docx')
    text13 = text13.decode("utf-8") 
    text_doc13.append(text13)
    
    #########################################################################
    text14 = textract.process('H:/vrenv/project 59/data/603913.docx')
    text14 = text14.decode("utf-8") 
    text_doc14.append(text14)
    
    
    text_doc12=text_doc12[0].title()[1237:33791]
    text_doc11=text_doc11[0].title()[365:6600]
    text_doc13=text_doc13[0].title()[0:33506]
    text_doc14=text_doc14[0].title()[1286:16930]
    
    dtst={}
    
    
    ##########################################################################
    
        
    for j in wrdchm2:
        if j in text_doc11:
            d1=dis_sent(text_doc11)
            for i in d1.ents:
                if i.ents[0].label_=='DISEASE' and str(i.ents[0]) not in dtst.values():
                    dtst[j]=i.text
    ###########################################
    
        
    for j in wrdchm2:
        if j in text_doc13:
            d5=dis_sent(text_doc13)
            for i in d5.ents:
                if i.ents[0].label_=='DISEASE' and str(i.ents[0]) not in dtst.values():
                    dtst[j]=i.text
    
    ###########################################3
    
        
    for j in wrdchm2:
        if j in text_doc12:
            d1=dis_sent(text_doc12)
            for i in d1.ents:
                if i.ents[0].label_=='DISEASE' and str(i.ents[0]) not in dtst.values():
                    dtst[j]=i.text
        ###############################################
    for j in wrdchm2:
        if j in text_doc14:
            d3=dis_sent(text_doc14)
            for i in d3.ents:
                if i.ents[0].label_=='DISEASE' and str(i.ents[0]) not in dtst.values():
                    dtst[j]=i.text
            
        
        ######################################
        
    dfdd=pd.DataFrame(columns=['drug','Disease'])
    dfdd['drug']=list(dtst.keys())
    dfdd['Disease']=list(dtst.values())
    dfdd['Disease']=dfdd['Disease'].str.replace('506','cancer').replace('Cancer','Iron Deficiency')
    dfdd['drug']=dfdd['drug'].str.replace('Ferrata','Feratab')
                            
        ########################################
        
    import os
    #os.getcwd()
#    dfdd.to_csv('H:/vrenv/project 59/dfdd.csv',encoding='utf-8')
            
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
    import pandas as pd
    df12=pd.read_csv('H:/vrenv/project 59/dfdd.csv')
    df12=df12.iloc[:,1::]

##########################################3
    df12['Disease']=df12['Disease'].apply(lambda x: x.replace('\n\n',''))
    
#####################################
    
    df12=df12.sample(frac=2,replace=True).reset_index(drop=True)
    return df12
