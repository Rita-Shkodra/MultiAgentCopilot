def research_task(vectorstore, plan, k=3, max_total=10):

    all_results = []

    for query in plan.get("research_queries", []):
        results = vectorstore.similarity_search(query, k=k)

        for r in results:
            all_results.append({
                "fact": r.page_content.strip(),
                "citation": r.metadata.get("citation_id", "unknown")
            })

    unique = {item["citation"]: item for item in all_results}

    return list(unique.values())[:max_total]
