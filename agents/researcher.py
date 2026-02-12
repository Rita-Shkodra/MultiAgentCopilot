def research_task(vectorstore, query, k=6):
    """
    Performs similarity search on the vectorstore
    and returns grounded structured notes with citations.
    """

    results = vectorstore.similarity_search(query, k=k)

    grounded_notes = []

    for r in results:
        note = {
            "summary": r.page_content[:500], 
            "citation": r.metadata.get("citation_id", "unknown")
        }
        grounded_notes.append(note)

    return grounded_notes
