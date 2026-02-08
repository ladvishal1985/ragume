# Simple RAG Evaluation - Quick Reference

## 🚀 Quick Start

### 1. Run Evaluation (First Time)
```bash
python tests/evaluate_simple.py
```

This creates `tests/rag_evaluation_results.json` with your baseline answers.

### 2. Make Improvements
Implement changes to improve accuracy (e.g., better prompts, re-ranking, etc.)

### 3. Run Evaluation Again
```bash
python tests/evaluate_simple.py
```

### 4. Compare Results
```bash
python tests/compare_simple.py
```

This shows before/after comparison and generates a report.

---

## 📊 What You Get

### Before vs After Comparison
```
======================================================================
BEFORE vs AFTER COMPARISON
======================================================================

Before: 2026-02-08 16:25:00
After:  2026-02-08 17:30:00

----------------------------------------------------------------------
Question                                           Before    After
----------------------------------------------------------------------
What is your Python experience?...                    ✓        ✓  =
What databases do you know?...                        ?        ✓  ↑
Do you have React experience?...                      ✓        ✓  =
----------------------------------------------------------------------

Improvements: 1
Declines: 0
No change: 9

✓ Overall: IMPROVED! 🎉
```

### Full History View
```
======================================================================
EVALUATION HISTORY
======================================================================
Total runs: 5

#    Date                  Total  Matches      %
----------------------------------------------------------------------
1    2026-02-08 16:25:00      10        7   70.0%
2    2026-02-08 17:30:00      10        8   80.0%
3    2026-02-08 18:45:00      10        9   90.0%

----------------------------------------------------------------------
Total progress: +20.0% (70.0% → 90.0%)
```

### Markdown Report
Generates `tests/simple_comparison_report.md` with:
- Question-by-question comparison table
- Change indicators (✅ Improved, ⚠️ Declined)
- Detailed answers for changed questions
- Summary statistics

---

## 📈 Tracking Progress

### Files Created

1. **`tests/reports/rag_evaluation_results.json`** - Latest evaluation results
2. **`tests/reports/rag_evaluation_history.json`** - Historical results (last 20 runs)
3. **`tests/reports/simple_comparison_report.md`** - Markdown comparison report

### Workflow

```
Run evaluation → Results saved to tests/reports/rag_evaluation_results.json
                ↓
Run comparison → Results added to tests/reports/rag_evaluation_history.json
                ↓
                → Comparison shown in terminal
                ↓
                → Report generated (tests/reports/simple_comparison_report.md)
```

---

## 💡 Example Usage

### Scenario: Testing Prompt Improvements

```bash
# 1. Baseline
python tests/evaluate_simple.py
# Results: 7/10 matches (70%)

# 2. Improve prompt (add "use ONLY provided context")
# Edit app/graph/nodes.py

# 3. Re-evaluate
python tests/evaluate_simple.py
# Results: 9/10 matches (90%)

# 4. Compare
python tests/compare_simple.py
# Output: ✓ Overall: IMPROVED! 🎉
#         Improvements: 2
#         Total progress: +20.0%
```

---

## 🎯 Match Indicators

- **✓** - Answer contains key terms from ground truth
- **?** - Answer doesn't match ground truth well
- **✗** - Error occurred

---

## 📝 Tips

### 1. Run Baseline First
Always run evaluation before making changes to establish baseline.

### 2. One Change at a Time
Make one improvement at a time to isolate impact.

### 3. Track in Git
Commit after each evaluation to correlate code changes with results.

### 4. Review Reports
Check `simple_comparison_report.md` for detailed analysis.

### 5. Manual Review
The JSON files contain full answers - review them manually for quality.

---

## 🔧 Customizing

### Add More Sophisticated Matching

Edit `evaluate_simple.py` to improve the match logic:

```python
# Current (simple keyword matching)
"match": "✓" if any(word in answer.lower() for word in ground_truth.lower().split()[:5]) else "?"

# Better (semantic similarity)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
similarity = cosine_similarity(
    model.encode([answer]),
    model.encode([ground_truth])
)[0][0]
"match": "✓" if similarity > 0.7 else "?"
```

---

## 🆚 vs RAGAS

| Feature | Simple Evaluation | RAGAS |
|---------|------------------|-------|
| **Speed** | ✅ Fast (~1 min) | ⚠️ Slow (10+ min) |
| **Reliability** | ✅ Always works | ⚠️ Can hang |
| **API Calls** | ✅ Only for RAG | ⚠️ 100+ extra calls |
| **Metrics** | Basic matching | Advanced (faithfulness, relevancy, etc.) |
| **Setup** | ✅ Simple | Complex |
| **Cost** | ✅ Low | Higher |

**Use Simple Evaluation for**:
- Quick iteration
- Frequent testing
- Development phase
- When RAGAS has issues

**Use RAGAS for**:
- Production evaluation
- Detailed metrics
- Final validation
- When you have higher API limits

---

## Summary

**Two simple commands**:
1. `python tests/evaluate_simple.py` - Run evaluation
2. `python tests/compare_simple.py` - Compare results

Track your RAG improvements without complex dependencies! 🎯

**Note**: RAGAS files are still available in `tests/` for when you want to use them later.
