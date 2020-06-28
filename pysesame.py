from urllib.request import urlopen
from urllib.parse import quote_plus
from simplejson import loads
from rdflib import Graph,plugin
from rdflib.util import guess_format, check_context
from rdflib.serializer import Serializer
import rdflib_jsonld

def eng_to_viet(string):
    diction={'subClassOf': 'con của lớp', 'isDefinedBy': 'khái niệm','@type':'loại','type':'loại','domain': 'miền giá trị'}
    return diction.get(string)

def trans_output(q):
    for i in q:
        if eng_to_viet(i[1])!=None:
            i[1]=eng_to_viet(i[1])
    return q

def viet_to_eng(string):
    string=string.lower()
    diction={'con của lớp': 'subClassOf', 'khái niệm': 'isDefinedBy','loại':'@type','miền giá trị': 'domain'}
    return diction.get(string)

def convert_input(q):
    q=q.lower()
    q=q.capitalize()
    return q

def trans_input(q):
    if viet_to_eng(q)!=None:
        q=viet_to_eng(q)
    return q

def take_second(elem):
    return elem[1]

def sort_output(q):
    q=sorted(q,key=take_second)
    return q

def get_string(q,res):
    #print(q)
    subject=q.get('@id')
    try:
        subject=subject.split('#',1)[1]
    except:
        subject=subject
    for i in q.keys():
        if i!='@id':
            try:
                name=i.split('#',1)[1]    
            except:
                name=i

            try:                
                contxt=list(q.get(i)[0].values())[0]
                try:
                    contxt=contxt.split('#',1)[1]
                except:
                    contxt=contxt
                res.append([subject,name,contxt])

            except: 
                contxt=q.get(i)

                try:
                    contxt=contxt.split('#',1)[1]
                except:
                    try:
                        for j in q.get(i):
                            contxt=j
                            contxt=contxt.split('#',1)[1]
                            res.append([subject,name,contxt])
                    except:
                        contxt=contxt
                        res.append([subject,name,contxt])
    return

def get_all(q):
    #print(q)
    res=[]
    for i in q:
        get_string(i,res)
#    for i in q:
        #print(res)
    return sort_output(res)

def get_predication(q,method):
    all_res = get_all(q)
    res=[]
    for i in all_res:
        if i[1]==method:
            res.append(i) 
    return sort_output(res)

def remove_predication(q,method):
    #print(method)
    all_res = get_all(q)
    res=[]
    for i in all_res:
        if i[1]!=method:
            res.append(i) 
    return sort_output(res)

class connection:
    def __init__(self,url):
        self.baseurl=url
        self.sparql_prefix=""
    
    def addnamespace(self,id,ns):
        self.sparql_prefix+='PREFIX %s:<%s>\n' % (id,ns) 
    
    def __getsparql__(self,method):
        #print(self.baseurl+method)
        g = Graph().parse(self.baseurl+method, format='xml')
        data=g.serialize(format='json-ld',indent=4)
        result=loads(data)

        return result
    
    def repositories(self):
        return self.__getsparql__('repositories')
        
    def use_repository(self,r):
        self.repository=r
    
    def query_one_para(self,q):
        q=convert_input(q)
        q="describe <urn:absolute:127.0.0.1/5000/mydatabase#"+q.replace(" ","_")+">"
        q='repositories/'+self.repository+'?query='+quote_plus(self.sparql_prefix+q)
        json_file= self.__getsparql__(q)
        return trans_output(get_all(json_file))
    
    def query_two_para(self,q,pred):
        q=convert_input(q)
        q="describe <urn:absolute:127.0.0.1/5000/mydatabase#"+q.replace(" ","_")+">"
        q='repositories/'+self.repository+'?query='+quote_plus(self.sparql_prefix+q)
        json_file= self.__getsparql__(q)
        return trans_output(get_predication(json_file,trans_input(pred)))
   
    def query_remove_para(self,q,pred):
        q=convert_input(q)
        q="describe <urn:absolute:127.0.0.1/5000/mydatabase#"+q.replace(" ","_")+">"
        q='repositories/'+self.repository+'?query='+quote_plus(self.sparql_prefix+q)
        json_file= self.__getsparql__(q)
        return trans_output(remove_predication(json_file,trans_input(pred)))
    
    def construct_query(self,q):
        q='repositories/'+self.repository+'?query='+quote_plus(self.sparql_prefix+q)
        data=urlopen(self.baseurl+q).read()
        return data
    
    def postdata(self,data):
        #/openrdf-sesame/repositories/mem-rdf/statements
        host=baseurl+'/repositories/'+self.repository+'/statements'
        res=urlopen(host,data)
        return res

        
if __name__=='__main__':

    c=connection('http://localhost:8080/openrdf-sesame/')
    c.use_repository('Course')
    
    res=c.query_one_para('Danh sách liên kết ngầm (MẢNG)')
    print(res)
    for i in res:
        print(i)
   
