# Single Agent Pipeline

A rule-based agent that routes a query to the right tool based on intent, with structured JSON-style output and error handling.

## Demo

| Query | Type | Result |
|---|---|---|
| `Calculate 20 + 5` | `calculation` | `25` |
| `Compute 8 * 4` | `calculation` | `32` |
| `Solve 100 / 5` | `calculation` | `20.0` |
| `Calculate 2^3` | `calculation` | `8` |
| `Extract keywords from Artificial Intelligence is transforming industries across every sector` | `keywords` | `['extract', 'keywords', 'artificial', 'intelligence', 'transforming']` |
| `What is the keyword in this text` | `keywords` | `['keyword']` |
| `Count the words in this message` | `count` | `{'words': 6, 'characters': 31}` |
| `What is machine learning?` | `general` | `No specific tool matched - treating as a general query: ...` |
| `Calculate 10 / 0` | `error` | `Error in calculation` |
| `Calculate 9**9**9**9` | `error` | `Error in calculation (expression too complex)` |

The last row is worth calling out: that query used to hang the kernel indefinitely with a plain `eval()`. The calculator tool now runs each expression in a separate process with a 2-second timeout, so it fails safely instead of freezing.

## Tools

- **Calculator** - evaluates math expressions, timeout-guarded against runaway computations
- **Keyword Extractor** - pulls out meaningful keywords, filtering stopwords, with deterministic output across runs
- **Word Counter** - word and character counts (bonus tool)

## Run

Open `week8_Parth_Moholkar.ipynb` and run all cells. The last cell is interactive - type a query, or `exit` to stop.
