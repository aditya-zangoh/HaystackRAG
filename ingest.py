from haystack.nodes import EmbeddingRetriever, PreProcessor
from haystack.document_stores import WeaviateDocumentStore
from haystack.nodes.file_converter import TextConverter
import os

print("Import Successfully")

path_txts = [f'data/{file}' for file in os.listdir('data')]

document_store = WeaviateDocumentStore(
    host="http://localhost", port=8080, embedding_dim=768
)

print("Document Store: ", document_store)
print("#####################")

converter = TextConverter()
print("Converter: ", converter)
print("#####################")

for path in path_txts:
    output = converter.convert(file_path=path, remove_numeric_tables=True)
    docs = output
    print("Docs: ", docs)
    print("#####################")

    final_doc = []
    for doc in docs:
        print(doc.text)
        new_doc = {"content": doc.text, "meta": doc.metadata}
        final_doc.append(new_doc)
        print("#####################")

    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=False,
        clean_header_footer=True,
        split_by="word",
        split_length=500,
        split_respect_sentence_boundary=True,
    )
    print("Preprocessor: ", preprocessor)
    print("#####################")

    preprocessed_docs = preprocessor.process(final_doc)
    print("Preprocessed Docs: ", preprocessed_docs)
    print("#####################")

    document_store.write_documents(preprocessed_docs)


    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    )

    print("Retriever: ", retriever)

    document_store.update_embeddings(retriever)

    print("Embeddings Done.")
