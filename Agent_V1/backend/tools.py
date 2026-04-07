
import os
import json
from langchain_core.tools import tool
from serpapi import GoogleSearch


@tool
def reverse_image_search(image_url: str) -> str:
    """
    Performs a reverse image search using Google Lens via SerpApi.
    Use this tool whenever the user provides an image URL to check its provenance.
    
    Args:
        image_url (str): The public URL of the image to analyze.
        
    Returns:
        str: A structured summary of the image's history and visual matches.
    """
    params = {
        "engine": "google_lens",
        "url": image_url,
        "api_key": os.environ.get("SERPAPI_API_KEY"),
        "hl": "en",  # Force English results
        "gl": "us"   # Force US geolocation for consistency
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # 1. Check for Knowledge Graph (Exact identification)
        # If Google knows exactly what the image is (e.g., "Eiffel Tower"), it puts it here.
        knowledge_graph = results.get("knowledge_graph",{})
        summary_parts =[]
        
        if knowledge_graph:
            entity = knowledge_graph
            title = entity.get("title", "Unknown Entity")
            subtitle = entity.get("subtitle", "")
            summary_parts.append(f"identified_entity: {title} ({subtitle})")
            
        # 2. Parse Visual Matches
        # These are other pages containing the same or similar images.
        matches = results.get("visual_matches",)
        summary_parts.append(f"visual_matches_count: {len(matches)}")
        
        if matches:
            summary_parts.append("top_matches:")
            for i, match in enumerate(matches[:5]): # Limit to top 5 to save tokens
                title = match.get("title", "No Title")
                source = match.get("source", "Unknown Source")
                date = match.get("date", "No Date") # Google sometimes provides date snippets
                link = match.get("link", "")
                
                entry = f"  {i+1}. Title: {title} | Source: {source} | Link: {link}"
                summary_parts.append(entry)
                
        # 3. Construct Final Output
        return "\n".join(summary_parts)

    except Exception as e:
        return f"Error executing reverse image search: {str(e)}"