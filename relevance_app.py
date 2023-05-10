import json
import itertools
import boto3
import re
#import stopwords
stopwords = ["a", "as", "able", "about", "above", "according", "accordingly",
	     "across", "actually", "after", "afterwards", "again", "against", "aint", "all", "allow",
	     "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among",
	     "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway",
	     "anyways", "anywhere", "apart", "appear","appreciate", "appropriate", "are", "arent", "around",
	     "as", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "be", "became",
	     "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind",
	     "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond",
	     "both", "brief", "but", "by", "cmon", "cs", "came", "can", "cant", "cannot", "cant",
	     "cause", "causes", "certain", "certainly", "changes", "clearly", "co", "com", "come",
	     "comes", "concerning", "consequently", "consider", "considering", "contain", "containing",
	     "contains", "corresponding", "could", "couldnt", "course", "currently", "definitely",
	     "described", "despite", "did", "didnt", "different", "do", "does", "doesnt", "doing",
	     "dont", "done", "down", "downwards", "during", "each", "edu", "eg", "eight", "either",
	     "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "ever",
	     "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example",
	     "except", "far", "few", "ff", "fifth", "first", "five", "followed", "following", "follows",
	     "for", "former", "formerly", "forth", "four", "from", "further", "furthermore", "get",
	     "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten",
	     "greetings", "had", "hadnt", "happens", "hardly", "has", "hasnt", "have", "havent",
	     "having", "he", "hes", "hello", "help", "hence", "her", "here", "heres", "hereafter",
	     "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself",
	     "his", "hither", "hopefully", "how", "howbeit", "however", "i", "id", "ill", "im", "ive",
	     "ie", "if", "ignored", "immediate", "in", "inasmuch", "inc", "indeed", "indicate",
	     "indicated", "indicates", "inner", "insofar", "instead", "into", "inward", "is",
	     "isnt", "it", "itd", "itll", "its", "its", "itself", "just", "keep", "keeps", "kept",
	     "know", "knows", "known", "last", "lately", "later", "latter", "latterly", "least",
	     "less", "lest", "let", "lets", "like", "liked", "likely", "little", "look", "looking",
	     "looks", "ltd", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely",
	     "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself",
	     "name", "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither",
	     "never", "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", "noone",
	     "nor", "normally", "not", "nothing", "novel", "now", "nowhere", "obviously", "of",
	     "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only",
	     "onto", "or", "other", "others", "otherwise", "ought", "our", "ours", "ourselves",
	     "out", "outside", "over", "overall", "own", "particular", "particularly",
	     "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably",
	     "provides", "que", "quite", "qv", "rather", "rd", "re", "really", "reasonably",
	     "regarding", "regardless", "regards", "relatively", "respectively", "right", "said",
	     "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing",
	     "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent",
	     "serious", "seriously", "seven", "several", "shall", "she", "should", "shouldnt",
	     "since", "six", "so", "some", "somebody", "somehow", "someone", "something",
	     "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify",
	     "specifying", "still", "sub", "such", "sup", "sure", "ts", "take", "taken", "tell", "tends",
	     "th", "than", "thank", "thanks", "thanx", "that", "thats", "thats", "the", "their", "theirs",
	     "them", "themselves", "then", "thence", "there", "theres", "thereafter", "thereby",
	     "therefore", "therein", "theres", "thereupon", "these", "they", "theyd",
	     "theyll", "theyre", "theyve", "think", "third", "this", "thorough",
	     "thoroughly", "those", "though", "three", "through", "throughout", "thru",
	     "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries",
	     "truly", "try", "trying", "twice", "two", "un", "under", "unfortunately",
	     "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used",
	     "useful", "uses", "using", "usually", "value", "various", "very", "via", "viz",
	     "vs", "want", "wants", "was", "wasnt", "way", "we", "wed", "well", "were", "weve",
	     "welcome", "well", "went", "were", "werent", "what", "whats", "whatever", "when",
	     "whence", "whenever", "where", "wheres", "whereafter", "whereas", "whereby",
	     "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who",
	     "whos", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish",
	     "with", "within", "without", "wont", "wonder", "would", "would", "wouldnt", "yes",
	     "yet", "you", "youd", "youll", "youre", "youve", "your", "yours", "yourself",
	     "yourselves", "zero"]
		 

#geeting the document ids for the terms
def get_docids_for_terms(terms):
    table=boto3.resource("dynamodb").Table("tfidf-5330")
    docids = []
    if terms is not None:
        for term in terms:
            query_params={ 
                'KeyConditionExpression':':term = term', 
                'ExpressionAttributeValues':{':term':term},  
                'ProjectionExpression':'docid' }
            response =table.query(**query_params)
            res=response['Items']
            docids.append(res)
    # dictiopnary is return, we need only document ids 
    d=list(itertools.chain.from_iterable(docids))
    dids=d1=[d[i]['docid'] for i in range(len(d))]
   
    return dids
#computing the relevant for given document id and terms    
def compute_doc_relevance(docid, terms):
    table=boto3.resource("dynamodb").Table("tfidf-5330")
    total = 0.0
    compute_rel=0.0
    if docid is not None and terms is not None:
        for term in terms:
            query_params={ 
                'KeyConditionExpression':':term = term and :docid = docid', 
                'ExpressionAttributeValues':{':term':term, ':docid':docid},  
                'ProjectionExpression':'tfidf' }
            response= table.query(**query_params)
            res= response['Items']
            # extracting only the terms from list of dictioonaries
            if len(res)>0:
                res1=float(res[0]['tfidf'])
            else:
                res1=0.0

            total = total+res1
        compute_rel = total/len(terms) 
    
    return compute_rel
# extractin gthe documenmt title for given documemnt id    
def doc_title(docid):
    table=boto3.resource("dynamodb").Table("doctitle-lab6")
    title=None
    query_params={ 
                'KeyConditionExpression':':docid = docid', 
                'ExpressionAttributeValues':{':docid':docid},  
                'ProjectionExpression':'title' }
    response= table.query(**query_params)
    res=response['Items']
    if len(res)>0:
        res1=res[0]['title']
    else:
        res1=""
    return res1
# extrqcting the relevant terms.    
def termify(line):
    terms = []
    words = re.findall(r'[^\W_]+', line)
    for word in words:
        lowered = word.lower()
        if (len(lowered) > 1) and (lowered not in stopwords) and (not re.search(r'^\d*$', lowered)):
            terms.append(lowered)
    return terms
#returning only the top five higfhest relevant document
def sort_and_limit(docid_relevance):
    docid_relevance=set(docid_relevance)
    sorted_docid=sorted(docid_relevance,key=lambda x: x[2], reverse=True)[:5]
   
    return sorted_docid
#main fucntion called by lambda fuction
def search(line):
    terms=termify(line)
    docids=get_docids_for_terms(terms)
    result=(sort_and_limit([(docid,doc_title(docid), compute_doc_relevance(docid, terms)) for docid in docids]))
    return result
#formattin gthe result
def formatResult(line,items):
    html="<html><body>"
    html+= f"<h3>Relevant documents for: {line}:</h3> \n"
    html += "<ol>"
    for item in items:
        html+= f"<li> {item[1]} -- {item[2]}</li>"
    html+= "</ol></body></html>"
    return {'statusCode':200,'headers':{'Content-Type':'text/html'},'body':html}
#lambda handler   
def lambda_handler(event, context):
    line=event['queryStringParameters']['line']
    items=search(line)
    return formatResult(line,items)  # Echo back the first key value
