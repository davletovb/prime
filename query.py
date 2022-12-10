
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import DensePassageRetriever
from haystack.nodes import Seq2SeqGenerator
from haystack.nodes import RAGenerator
from haystack.nodes import PreProcessor
from haystack.pipelines import GenerativeQAPipeline
from haystack.utils import clean_wiki_text, convert_files_to_docs, launch_es

import pandas as pd
import glob


class QAPipeline:
    """
    A class that defines a question-answering (QA) pipeline using the Haystack library.
    """

    def __init__(self, retriever=BM25Retriever, generator=Seq2SeqGenerator, pipeline=GenerativeQAPipeline, document_store=ElasticsearchDocumentStore, model_name="vblagoje/bart_lfqa"):
        """
        Initializes the QA pipeline by creating and configuring its components.
        """
        # if the document store is elasticsearch, launch it
        if document_store == ElasticsearchDocumentStore:
            try:
                launch_es()
            except:
                print("Elasticsearch already running")

        # Create the document store
        self.document_store = document_store(
            host="localhost", username="", password="", index="document")

        self.documents_path = "data/documents"

        # Create the retriever
        self.retriever = retriever(document_store=self.document_store)

        # Using Facebook's DPR model together with Facebook's RAG model
        # retriever = DensePassageRetriever(document_store=document_store, query_embedding_model="facebook/dpr-question_encoder-single-nq-base", passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base", use_gpu=True, embed_title=True)

        # Using HuggingFace's DPR retriever model for LFQA
        # retriever = DensePassageRetriever(document_store=document_store, query_embedding_model="vblagoje/dpr-question_encoder-single-lfqa-wiki", passage_embedding_model="vblagoje/dpr-ctx_encoder-single-lfqa-wiki", use_gpu=True)
        # document_store.update_embeddings(retriever)

        # Create the generator
        self.generator = generator(model_name_or_path=model_name, use_gpu=True)

        # Using Facebook's RAG model
        # generator = RAGenerator(model_name_or_path="facebook/rag-token-nq", use_gpu=True)

        # Create the pipeline
        self.pipeline = pipeline(
            generator=self.generator, retriever=self.retriever)

    def retrieve(self, query, top_k=10):
        """
        Retrieves the top-k documents that are most relevant to the given query.
        """
        return self.retriever.retrieve(query, top_k=top_k)

    def answer(self, question, top_k_retriever=10, top_k_generator=1):
        """
        Answers the given question by retrieving the most relevant documents and generating an answer from them.
        """
        # Run the pipeline to retrieve relevant documents and generate an answer
        prediction = self.pipeline.run(
            query=question,
            params={
                "Retriever": {"top_k": top_k_retriever},
                "Generator": {"top_k": top_k_generator},
            })

        try:
            answer = prediction['answers'][0].answer
        except:
            answer = "No answer found"

        return answer

    def write_documents(self, docs):
        """
        Writes the given documents to the document store.
        """

        # check if there are new files in the directory
        # get the list of files in the directory
        files = glob.glob(self.documents_path+'/*.txt')

        # get the list of files in the document store
        docs = self.document_store.get_all_documents()
        docs = pd.DataFrame(docs)

        # check if there are new files
        if len(files) > len(docs.index):
            # clean and convert files to Haystack Documents
            docs = convert_files_to_docs(
                dir_path=self.documents_path, clean_func=clean_wiki_text, split_paragraphs=True)

            # preprocess documents
            processor = PreProcessor(
                split_by="word", split_length=500, split_respect_sentence_boundary=True)
            docs = processor.process(docs)

            # write documents to document store
            self.document_store.write_documents(docs)
