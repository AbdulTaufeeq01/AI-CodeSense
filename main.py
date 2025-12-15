import argparse
import traceback
from github_fetch import fetch_python_files
from chunker import chunk_code
from embedder import embed
from vector_store import VectorStore
from reviewer import review_code
from naive_reviewer import review_full_repo
from metrics import estimate_tokens, measure_execution

# Parse command-line arguments
parser = argparse.ArgumentParser(description="AI CodeSense – Retrieval-grounded code review system")
parser.add_argument("--owner", default="psf", help="GitHub username or organization (default: psf)")
parser.add_argument("--repo", default="requests", help="GitHub repository name (default: requests)")
parser.add_argument("--query", default="security vulnerabilities", help="Type of issues to look for (default: security vulnerabilities)")

args = parser.parse_args()
OWNER = args.owner
REPO = args.repo
QUERY = args.query

print(f"\nAnalyzing {OWNER}/{REPO} for: {QUERY}\n")

try:
    # ----------------------------
    # Fetch repository
    # ----------------------------
    files = fetch_python_files(OWNER, REPO)

    # ============================
    # 1️⃣ NAIVE FULL-FILE APPROACH
    # ============================
    (naive_review, full_context), naive_time = measure_execution(
        review_full_repo, files
    )

    naive_tokens = estimate_tokens(full_context)

    # ============================
    # 2️⃣ CHUNK + RETRIEVAL APPROACH
    # ============================
    chunks = []
    for file in files:
        chunks.extend(chunk_code(file))

    embeddings = embed(chunks)
    store = VectorStore(len(embeddings[0]))
    store.add(embeddings, chunks)

    query_embedding = embed([QUERY])[0]
    retrieved_chunks = store.search(query_embedding)

    retrieval_context = "\n".join(retrieved_chunks)

    (chunk_review, chunk_time) = measure_execution(
        review_code, retrieval_context
    )

    chunk_tokens = estimate_tokens(retrieval_context)

    # ============================
    # 📊 EFFICIENCY COMPARISON
    # ============================
    token_reduction = 100 * (1 - chunk_tokens / naive_tokens)
    time_reduction = 100 * (1 - chunk_time / naive_time)

    print("\n========== Efficiency Comparison ==========")
    print(f"Naive input tokens:     {naive_tokens}")
    print(f"Chunked input tokens:   {chunk_tokens}")
    print(f"Token reduction:        {token_reduction:.2f}%")

    print(f"\nNaive processing time:  {naive_time:.2f} sec")
    print(f"Chunked processing time:{chunk_time:.2f} sec")
    print(f"Time reduction:         {time_reduction:.2f}%")

    print("\n========== Chunked Review Output ==========")
    print(chunk_review)
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
    exit(1)