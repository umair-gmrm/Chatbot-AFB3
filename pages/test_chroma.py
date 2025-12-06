import chromadb

client = chromadb.Client()


def main():
    collection = client.create_collection("test")
    collection.add(
        documents=["Hello, World!"],
        metadatas=[{"source": "test"}],    
        ids=["1"]
    )
    collection.add(
        documents=["Hello"],
        metadatas=[{"source": "test"}],    
        ids=["2"]
    )

    collection.add(
        documents=["My name is John"],
        metadatas=[{"source": "test"}],    
        ids=["3"]
    )
    results = collection.query(
        query_texts=["name"],
        n_results=1)
    
    print(results)

    client.delete_collection("test")
    print("Collection deleted")

if __name__ == "__main__":
    main()