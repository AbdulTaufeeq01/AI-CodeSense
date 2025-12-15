# AI CodeSense 🤖

**AI CodeSense** is a retrieval-grounded code review system that analyzes GitHub repositories for bugs, security risks, code smells, and refactoring opportunities using AI-powered code analysis.

## Features

✨ **Smart Code Analysis**
- Analyzes Python files from any GitHub repository
- Identifies bugs, security vulnerabilities, and code smells
- Provides suggested refactoring improvements
- Uses AI to deliver concise, actionable insights

⚡ **Efficient Processing**
- Chunks code into manageable pieces for better analysis
- Retrieves relevant code sections based on your query
- Compares efficiency between naive and chunked approaches
- Measures token usage and processing time

🔐 **Secure**
- GitHub token support for higher API rate limits
- Environment-based configuration
- No credentials stored in version control

## Installation

### Prerequisites
- Python 3.8+
- Ollama (for local LLM inference)

### Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Ollama**
   ```bash
   ollama pull llama3
   ollama serve
   ```

3. **Configure GitHub Token** (optional for higher rate limits)
   ```powershell
   $env:GITHUB_TOKEN = 'your_github_token'
   ```
   Get a token at: https://github.com/settings/tokens (select `public_repo` scope)

## Usage

### Basic Command
```bash
python main.py --owner <username> --repo <repository> --query "<what-to-look-for>"
```

### Examples
```bash
# Analyze Flask for security vulnerabilities
python main.py --owner pallets --repo flask --query "security vulnerabilities"

# Analyze a personal project for code smells
python main.py --owner AbdulTaufeeq01 --repo PharmaMap --query "code smells"

# Use defaults (PSF's requests library)
python main.py
```

### Arguments
- `--owner`: GitHub username/organization (default: `psf`)
- `--repo`: Repository name (default: `requests`)
- `--query`: Type of issues to find (default: `security vulnerabilities`)

## How It Works

1. **Fetch** - Download Python files from GitHub
2. **Chunk** - Split code into manageable pieces
3. **Embed** - Generate embeddings using sentence-transformers
4. **Retrieve** - Find relevant chunks matching your query
5. **Analyze** - Send context to Ollama for AI review
6. **Compare** - Show efficiency gains vs. full-repo approach

## Output

The tool provides a comprehensive analysis with:

```
========== Efficiency Comparison ==========
Naive input tokens:     5,432
Chunked input tokens:   1,246
Token reduction:        77.07%

Naive processing time:  12.34 sec
Chunked processing time: 3.21 sec
Time reduction:         73.97%

========== Chunked Review Output ==========
- Bug identified: Missing null check in line 45
- Security Risk: Hardcoded credentials detected
- Code Smell: Function too long (250+ lines)
- Suggested Refactoring: Extract helper method for validation logic
```

## Project Structure

```
ai_codesense/
├── main.py              # Entry point
├── github_fetch.py      # GitHub API integration
├── chunker.py           # Code chunking
├── embedder.py          # Embedding generation
├── vector_store.py      # FAISS vector search
├── reviewer.py          # AI code review
├── naive_reviewer.py    # Full-repo baseline
├── metrics.py           # Performance tracking
├── requirements.txt
└── README.md
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Ollama connection error** | Run `ollama serve` in another terminal |
| **Model not found** | Run `ollama pull llama3` |
| **GitHub rate limit** | Set `$env:GITHUB_TOKEN = 'your_token'` |
| **Missing module** | Run `pip install -r requirements.txt` |

## Performance Tips

1. **Use GitHub Token** - Allows more API requests
2. **Start with small repos** - Fewer files = faster analysis
3. **Be specific with queries** - Better retrieval results
4. **Run locally** - Ollama inference is faster than cloud APIs

## Future Enhancements

- [ ] Support for multiple programming languages
- [ ] Integration with different LLM providers (OpenAI, Claude)
- [ ] Web UI for interactive analysis
- [ ] Batch repository analysis
- [ ] Custom chunk size configuration
- [ ] Export results to JSON/HTML

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for better code quality**
