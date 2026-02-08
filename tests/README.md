# RAG Evaluation Tests

This directory contains test infrastructure for evaluating the RAG chatbot's accuracy using RAGAS.

## Files

- **`ragas_test_data.py`**: Test dataset with 10 questions and ground truth answers
- **`evaluate_with_ragas.py`**: Main evaluation script using RAGAS metrics
- **`ragas_results.json`**: Evaluation results (generated after running tests)

## RAGAS Metrics

The evaluation measures:

1. **Faithfulness** (target: >0.90): No hallucination - answer grounded in context
2. **Answer Relevancy** (target: >0.85): Answer addresses the question
3. **Context Precision** (target: >0.80): Retrieved documents are relevant
4. **Context Recall** (target: >0.75): All needed information was retrieved

## Usage

### Run Full Evaluation

```bash
python tests/evaluate_with_ragas.py
```

### Expected Output

```
============================================================
RAGAS EVALUATION RESULTS
============================================================
faithfulness................................ 0.9500
answer_relevancy............................ 0.8800
context_precision........................... 0.8200
context_recall.............................. 0.7900
Overall Score............................... 0.8600

INTERPRETATION
faithfulness: Excellent ✓
answer_relevancy: Good
context_precision: Good
context_recall: Fair
```

## Test Dataset

The test dataset includes:
- **3 simple questions**: Basic information retrieval
- **2 complex questions**: Multiple pieces of information
- **3 technical questions**: Specific implementations
- **2 edge cases**: Testing boundaries

## Interpreting Results

| Score Range | Quality | Action |
|-------------|---------|--------|
| 0.90-1.00 | Excellent | Maintain quality |
| 0.80-0.89 | Good | Minor improvements |
| 0.70-0.79 | Fair | Needs improvement |
| < 0.70 | Poor | Major issues |

### Diagnostic Guide

**Low Faithfulness (<0.80)**:
- Problem: Hallucination
- Fix: Improve prompt, add confidence scoring

**Low Answer Relevancy (<0.80)**:
- Problem: Answer doesn't address question
- Fix: Better prompt engineering

**Low Context Precision (<0.75)**:
- Problem: Retrieving irrelevant documents
- Fix: Improve retrieval (re-ranking, better embeddings)

**Low Context Recall (<0.70)**:
- Problem: Missing relevant information
- Fix: Retrieve more documents, improve chunking

## Cost

RAGAS uses LLM calls for evaluation:
- ~5-10 LLM calls per test case
- For 10 test cases: ~50-100 LLM calls
- With gpt-4o-mini: ~$0.01-0.02 per run

## Adding New Test Cases

Edit `ragas_test_data.py`:

```python
test_data = {
    "question": [
        "Your new question here",
        # ... existing questions
    ],
    "ground_truth": [
        "Expected answer here",
        # ... existing answers
    ]
}
```

## Continuous Testing

Recommended schedule:
- After major changes
- Weekly for monitoring
- Before deployment
