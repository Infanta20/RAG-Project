from collections import defaultdict


def normalize_score(raw_score):
    try:
        return round(1 / (1 + float(raw_score)), 4)
    except Exception:
        return 0.0


def rank_candidates(results, top_n=5):
    grouped = defaultdict(list)

    for doc, raw_score in results:
        candidate_id = doc.metadata.get("candidate_id", "unknown")

        grouped[candidate_id].append({
            "candidate_name": doc.metadata.get("candidate_name", "Unknown"),
            "file_name": doc.metadata.get("file_name", "Unknown.pdf"),
            "page": doc.metadata.get("page", 0),
            "raw_score": float(raw_score),
            "score": normalize_score(raw_score),
            "snippet": doc.page_content[:350]
        })

    final_results = []

    for candidate_id, matches in grouped.items():
        matches = sorted(matches, key=lambda x: x["raw_score"])
        top_matches = matches[:3]

        avg_score = sum(item["score"] for item in top_matches) / len(top_matches)
        best_match = top_matches[0]

        final_results.append({
            "candidate_id": candidate_id,
            "candidate_name": best_match["candidate_name"],
            "file_name": best_match["file_name"],
            "match_score": round(avg_score * 100, 2),
            "best_page": best_match["page"] + 1,
            "best_snippet": best_match["snippet"],
            "matched_chunks": len(matches)
        })

    final_results = sorted(final_results, key=lambda x: x["match_score"], reverse=True)
    return final_results[:top_n]