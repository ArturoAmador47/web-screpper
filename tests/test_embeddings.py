"""Tests for embeddings service."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.embeddings.embeddings_service import EmbeddingsService


def test_cosine_similarity():
    """Test cosine similarity calculation."""
    service = EmbeddingsService()
    
    # Identical vectors
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [1.0, 0.0, 0.0]
    similarity = service.cosine_similarity(vec1, vec2)
    assert abs(similarity - 1.0) < 0.001
    
    # Orthogonal vectors
    vec3 = [1.0, 0.0, 0.0]
    vec4 = [0.0, 1.0, 0.0]
    similarity = service.cosine_similarity(vec3, vec4)
    assert abs(similarity - 0.0) < 0.001
    
    # Opposite vectors
    vec5 = [1.0, 0.0, 0.0]
    vec6 = [-1.0, 0.0, 0.0]
    similarity = service.cosine_similarity(vec5, vec6)
    assert abs(similarity - (-1.0)) < 0.001


def test_is_duplicate():
    """Test duplicate detection."""
    service = EmbeddingsService()
    
    # Very similar vectors (should be duplicate)
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [0.99, 0.01, 0.0]
    assert service.is_duplicate(vec1, vec2, threshold=0.9)
    
    # Different vectors (should not be duplicate)
    vec3 = [1.0, 0.0, 0.0]
    vec4 = [0.0, 1.0, 0.0]
    assert not service.is_duplicate(vec3, vec4, threshold=0.9)


def test_find_duplicates():
    """Test finding duplicate groups."""
    service = EmbeddingsService()
    
    embeddings = [
        [1.0, 0.0, 0.0],  # Group 1
        [0.99, 0.01, 0.0],  # Group 1
        [0.0, 1.0, 0.0],  # Group 2
        [0.0, 0.99, 0.01],  # Group 2
        [0.0, 0.0, 1.0],  # Unique
    ]
    
    duplicate_groups = service.find_duplicates(embeddings, threshold=0.9)
    
    # Should find 2 duplicate groups
    assert len(duplicate_groups) == 2
    assert len(duplicate_groups[0]) == 2
    assert len(duplicate_groups[1]) == 2
