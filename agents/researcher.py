def research_task(vectorstore, query, k=10):
    results = vectorstore.similarity_search(query, k=k)

    grounded_facts = []

    for r in results:
        grounded_facts.append({
            "fact": r.page_content.strip(),
            "citation": r.metadata.get("citation_id", "unknown")
        })

    return grounded_facts
