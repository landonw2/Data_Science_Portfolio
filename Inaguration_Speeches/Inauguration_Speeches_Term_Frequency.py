import gensim
import re
import pandas as pd
import nltk
import string
nltk.download( 'averaged_perceptron_tagger' )
nltk.download('punkt')
nltk.download('stopwords')

speeches = pd.read_csv(r'presidential_speeches_all.csv')

##########################################################################
#                                                                        #                                        
#                            Text Posturing                              #
#                                                                        #
##########################################################################

# Remove punctuation, then tokenize documents
punc = re.compile( '[%s]' % re.escape( string.punctuation ) )

term_vec = []

for text in speeches['Speech']:
    text = text.lower()
    text = punc.sub( '', text )
    term_vec.append( nltk.word_tokenize( text ) )
    

# Remove stop words from term vectors
stop_words = nltk.corpus.stopwords.words( 'english' )

for i in range( 0, len( term_vec ) ):
    term_list = [ ]

    for term in term_vec[ i ]:
        if term not in stop_words:
            term_list.append( term )

    term_vec[ i ] = term_list


# Porter stem remaining terms
porter = nltk.stem.porter.PorterStemmer()

for i in range( 0, len(term_vec)):
    for j in range( 0, len(term_vec[ i ])):
        term_vec[i][j] = porter.stem(term_vec[i][j])


#  Convert term vectors into gensim dictionary

dict = gensim.corpora.Dictionary( term_vec )

corp = [ ]
for i in range( 0, len( term_vec ) ):
    corp.append( dict.doc2bow( term_vec[ i ] ) )


##########################################################################
#                                                                        #                                        
#                                 TFIDF                                  #
#                                                                        #
##########################################################################

#  Create TFIDF vectors based on term vectors bag-of-word corpora
tfidf_model = gensim.models.TfidfModel( corp )

tfidf = [ ]
for i in range( 0, len( corp ) ):
    tfidf.append( tfidf_model[ corp[ i ] ] )

#  Create pairwise document similarity index
n = len( dict )
index = gensim.similarities.SparseMatrixSimilarity( tfidf_model[ corp ], num_features = n )

#  Create pairwise similarity per document
for i in range( 0, len( tfidf ) ):
    s = 'Doc ' + str( i + 1 ) + ' TFIDF:'

    for j in range( 0, len( tfidf[ i ] ) ):
        s = s + ' (' + dict.get( tfidf[ i ][ j ][ 0 ] ) + ','
        s = s + ( '%.3f' % tfidf[ i ][ j ][ 1 ] ) + ')'
    
    #print(s)  

# Storing similarity scores
sim_list = []
for i in range( 0, len( corp ) ):
    #print( 'Doc', ( i + 1 ), 'sim: [ ',)

    sim = index[ tfidf_model[ corp[ i ] ] ]
    #for j in range( 0, len( sim ) ):
        #print( '%.3f ' % sim[ j ],)

    #print(']')
    sim = sim.tolist()
    sim_list.append(sim)
    