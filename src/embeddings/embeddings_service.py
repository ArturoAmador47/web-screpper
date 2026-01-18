"""Embeddings module for generating and comparing article embeddings."""

import logging
from typing import List, Optional
import numpy as np
from openai import AsyncOpenAI

from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingsService:
    """Service for generating and comparing text embeddings using OpenAI."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
    
    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding vector for text."""
        try:
            # Truncate text if too long (OpenAI has token limits)
            text = text[:8000]  # Roughly 8000 chars ~ 2000 tokens
            
            response = await self.client.embeddings.create(
                model=self.model,
                input=text
            )
            
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding with {len(embedding)} dimensions")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Generate embeddings for multiple texts."""
        embeddings = []
        
        # Process in batches to avoid rate limits
        batch_size = 10
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            try:
                # Truncate texts
                batch = [text[:8000] for text in batch]
                
                response = await self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                
            except Exception as e:
                logger.error(f"Error generating batch embeddings: {e}")
                embeddings.extend([None] * len(batch))
        
        logger.info(f"Generated {len(embeddings)} embeddings")
        return embeddings
    
    def cosine_similarity(
        self, 
        embedding1: List[float], 
        embedding2: List[float]
    ) -> float:
        """Calculate cosine similarity between two embeddings."""
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    
    def is_duplicate(
        self, 
        embedding1: List[float], 
        embedding2: List[float],
        threshold: Optional[float] = None
    ) -> bool:
        """Check if two embeddings represent duplicate content."""
        if threshold is None:
            threshold = settings.similarity_threshold
        
        similarity = self.cosine_similarity(embedding1, embedding2)
        return similarity >= threshold
    
    def find_duplicates(
        self,
        embeddings: List[List[float]],
        threshold: Optional[float] = None
    ) -> List[List[int]]:
        """Find duplicate articles based on embeddings.
        
        Returns:
            List of duplicate groups, where each group is a list of indices.
        """
        if threshold is None:
            threshold = settings.similarity_threshold
        
        n = len(embeddings)
        visited = set()
        duplicate_groups = []
        
        for i in range(n):
            if i in visited:
                continue
            
            group = [i]
            visited.add(i)
            
            for j in range(i + 1, n):
                if j in visited:
                    continue
                
                similarity = self.cosine_similarity(embeddings[i], embeddings[j])
                if similarity >= threshold:
                    group.append(j)
                    visited.add(j)
            
            if len(group) > 1:
                duplicate_groups.append(group)
        
        logger.info(f"Found {len(duplicate_groups)} duplicate groups")
        return duplicate_groups


async def main():
    """Test embeddings service."""
    service = EmbeddingsService()
    
    texts = [
        "OpenAI releases GPT-5 with improved capabilities",
        "OpenAI announces GPT-5 with enhanced features",
        "Google unveils new AI model competing with GPT",
    ]
    
    embeddings = await service.generate_embeddings_batch(texts)
    
    print("\nSimilarity matrix:")
    for i, emb1 in enumerate(embeddings):
        for j, emb2 in enumerate(embeddings):
            if i < j and emb1 and emb2:
                sim = service.cosine_similarity(emb1, emb2)
                print(f"Text {i} vs Text {j}: {sim:.4f}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
