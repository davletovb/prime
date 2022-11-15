from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import DensePassageRetriever
from haystack.nodes import Seq2SeqGenerator
from haystack.nodes import RAGenerator
from haystack.nodes import PreProcessor
from haystack.pipelines import GenerativeQAPipeline
from haystack.utils import clean_wiki_text, convert_files_to_docs, print_answers, launch_es

import pandas as pd
import glob
import time
import datetime as dt


def prepare_document_store():
    # try to launch elasticsearch server if not already running
    try:
        launch_es()
    except:
        print("Elasticsearch already running")

    # Connect to Elasticsearch
    document_store = ElasticsearchDocumentStore(
        host="localhost", username="", password="", index="document")
    # document_store.delete_documents()
    # Download sample data
    doc_dir = "data/article_txt_got"

    # check if there are new files in the directory
    # get the list of files in the directory
    files = glob.glob(doc_dir+'/*.txt')

    # get the list of files in the document store
    docs = document_store.get_all_documents()
    docs = pd.DataFrame(docs)

    # check if there are new files
    if len(files) > len(docs.index):
        # convert files to documents
        docs = convert_files_to_docs(
            dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)

        # preprocess documents
        processor = PreProcessor(
            split_by="word", split_length=500, split_respect_sentence_boundary=True)
        docs = processor.process(docs)

        # write documents to document store
        document_store.write_documents(docs)

    # clean and convert files to Haystack Documents
    #docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)

    # Write documents to DB
    # document_store.write_documents(docs)
    return document_store


def answer(question):

    start_time = time.time()
    print("Starting to get answer from model... : {}".format(
        dt.datetime.fromtimestamp(start_time)))
    print()

    document_store = prepare_document_store()

    # Initialize Retriever
    retriever = BM25Retriever(document_store=document_store)

    # Using Facebook's DPR model together with Facebook's RAG model
    #retriever = DensePassageRetriever(document_store=document_store, query_embedding_model="facebook/dpr-question_encoder-single-nq-base", passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base", use_gpu=True, embed_title=True)

    # Using HuggingFace's DPR retriever model for LFQA
    #retriever = DensePassageRetriever(document_store=document_store, query_embedding_model="vblagoje/dpr-question_encoder-single-lfqa-wiki", passage_embedding_model="vblagoje/dpr-ctx_encoder-single-lfqa-wiki", use_gpu=True)
    # document_store.update_embeddings(retriever)

    # use Haystack generator to generate answers from the pipeline, use Seq2SeqGenerator for abstractive QA
    generator = Seq2SeqGenerator(
        model_name_or_path="vblagoje/bart_lfqa", use_gpu=True)

    # Using Facebook's RAG model
    #generator = RAGenerator(model_name_or_path="facebook/rag-token-nq", use_gpu=True)

    pipe = GenerativeQAPipeline(generator, retriever)

    prediction = pipe.run(
        query=question,
        params={
            "Retriever": {"top_k": 10},
            "Generator": {"top_k": 1},
        })

    # return the answer from the json
    print_answers(prediction, details="minimum")

    end_time = time.time()
    # print the time it took to get the answer and leave a blank line
    print("End of process, time: ", dt.datetime.fromtimestamp(end_time))
    print("Time to get answer: ", end_time - start_time, " seconds")
    print()

    try:
        answer = prediction['answers'][0].answer
    except:
        answer = "No answer found"

    return answer
