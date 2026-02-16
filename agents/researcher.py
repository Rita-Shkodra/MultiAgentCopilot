def research_task(vectorstore, plan, k=4, max_total=6, score_threshold=0.6):

    all_results = []

    research_queries = plan.get("research_queries", [])

    for query in research_queries:

        try:
            results = vectorstore.similarity_search_with_score(query, k=k)
        except Exception:
            continue  

        for doc, score in results:

          
            if score is None:
                continue

            if score > score_threshold:
                continue  

            citation = doc.metadata.get("citation_id", "unknown")

            all_results.append({
                "fact": doc.page_content.strip(),
                "citation": citation
            })

    
    unique = {}
    for item in all_results:
        unique[item["fact"]] = item

    final_notes = list(unique.values())[:max_total]

    return final_notes
