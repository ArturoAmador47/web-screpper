#!/usr/bin/env python3
"""
Setup script for Supabase database schema.
This script prints the SQL needed to set up the articles table with pgvector.
"""

from src.storage.supabase_storage import SupabaseStorage


def main():
    """Print the setup SQL for Supabase."""
    print("=" * 80)
    print("SUPABASE DATABASE SETUP")
    print("=" * 80)
    print("\nCopy and run the following SQL in your Supabase SQL Editor:\n")
    print("-" * 80)
    
    storage = SupabaseStorage()
    print(storage.create_schema_sql())
    
    print("-" * 80)
    print("\nAfter running the SQL, your database will be ready to store articles.")
    print("\nNext steps:")
    print("1. Run the SQL above in Supabase SQL Editor")
    print("2. Update your .env file with Supabase credentials")
    print("3. Start the API server: python -m src.api.main")
    print("=" * 80)


if __name__ == "__main__":
    main()
