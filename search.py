import gzip
import numpy as np


class SemanticSearch:
    def __init__(self, documents):
        self.documents = documents
        self.compressed_docs = self.compress_documents()

    def compress_documents(self):
        compressed_docs = []
        for doc in self.documents:
            compressed_doc = gzip.compress(doc.encode())  # Compress document using gzip
            compressed_docs.append(compressed_doc)
        return compressed_docs

    def calculate_similarity(self, query_doc):
        query_compressed = gzip.compress(query_doc.encode())  # Compress query document
        distances = []
        for doc in self.documents:
            compressed_doc = gzip.compress(doc.encode())
            querydoc_compressed = gzip.compress(" ".join([query_doc, doc]).encode())
            dist = self.ncd_distance(query_compressed, compressed_doc,
                                     querydoc_compressed)  # Calculate NCD distance between compressed representations
            distances.append(dist)
        return distances

    def ncd_distance(self, x, y, xy):
        length_x = len(x)
        length_y = len(y)
        length_xy = len(xy)

        dist = (length_xy - min(length_x, length_y)) / max(length_x, length_y)
        return dist

    def search(self, query_doc, k=1):
        distances = self.calculate_similarity(query_doc)
        sorted_indices = np.argsort(distances)
        top_k_indices = sorted_indices[:k]
        results = [self.documents[idx] for idx in top_k_indices]
        return results


# Example usage
if __name__ == "__main__":
    # Create a list of documents
    documents = [
        "Санкт-Петербург был основан в 1703 году по инициативе императора Петра I. На Заячьем острове был заложен первый камень, именно отсюда стал расти новый город.",
        "Своё название Санкт-Петербург получил от Петропавловской крепости, первого сооружения города, которое появилось на реке Неве в ходе Северной войны.",
        "Новая столица (Санкт-Петербург был столицей России на протяжении двух столетий, начиная с 1710 года) строилась силами крепостных, которых насильно сгоняли на постройку города. Говорят, что Петербург стоит на костях усопших.",
        "Во время строительства от недоедания и изнурительного труда умерло несколько тысяч рабочих-крестьян. В 1710 году Петр приказал переселить в Петербург около 15 тысяч разных мастеровых людей из всех областей России.",
        "Во времена царствования Павла I было построено самое мистическое здание Петербурга - Михайловский замок, легенды о котором ходят и по сей день."
    ]

    # Create an instance of SemanticSearch
    search_engine = SemanticSearch(documents)

    # Query document
    query = "В каком году переселили мастеровых?"

    # Perform semantic search
    search_results = search_engine.search(query, k=3)

    # Print search results
    print("Search Results:")
    for result in search_results:
        print(result)