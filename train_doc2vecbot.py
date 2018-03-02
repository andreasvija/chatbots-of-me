import time
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from random import randint

def train_doc2vecbot(corpus, inputs):

    text_corpus = corpus
    doc_corpus = []
    for i in range(len(corpus)):
        code = 'corpus' + str(i)
        doc_corpus.append(TaggedDocument(corpus[i].split(), [code]))
        
    training_inputs = []
    for i in range(len(inputs)):
        code = 'input' + str(i)
        doc_corpus.append(TaggedDocument(inputs[i].split(), [code]))
        
    start = time.clock()
    
    model = Doc2Vec(window=5, min_count=2, iter=5)
    model.build_vocab(doc_corpus)
    model.train(doc_corpus, total_examples=model.corpus_count, epochs=model.iter)

    end = time.clock()
    print('Training doc2vec completed in ' +
          str(int((end-start)) // 60) + 'm ' +
          str(int((end-start)) % 60) + 's')
    
    model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    model.save('doc2vecmodel')
    
