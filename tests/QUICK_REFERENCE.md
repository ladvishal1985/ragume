# RAGAS Evaluation - Quick Reference

## 🚀 Quick Start

### 1. Run Evaluation (First Time)
```bash
python tests/evaluate_with_ragas.py
```

This creates `tests/ragas_results.json` with your baseline scores.

### 2. Make Improvements
Implement changes to improve accuracy (e.g., better prompts, re-ranking, etc.)

### 3. Run Evaluation Again
```bash
python tests/evaluate_with_ragas.py
```

### 4. Compare Results
```bash
python tests/compare_results.py
```

This shows before/after comparison and generates a report.

---

## 📊 Comparison Dashboard Features

### Before vs After Comparison
```
============================================================
BEFORE vs AFTER COMPARISON
============================================================

Before: 2026-02-08T15:25:00
After:  2026-02-08T16:30:00

------------------------------------------------------------
Metric                         Before      After     Change
------------------------------------------------------------
faithfulness                   0.8500     0.9200   +0.0700 ↑
answer_relevancy               0.8000     0.8500   +0.0500 ↑
context_precision              0.7500     0.8200   +0.0700 ↑
context_recall                 0.7000     0.7500   +0.0500 ↑
------------------------------------------------------------
OVERALL                        0.7875     0.8350   +0.0475

============================================================
SUMMARY
============================================================
✓ Overall improvement: +6.03%
  Great work! The changes improved accuracy.

Biggest improvement: faithfulness (+0.0700)
Biggest decline: context_recall (+0.0500)
```

### Full History View
```
============================================================
EVALUATION HISTORY
============================================================
Total runs: 5

#    Date                  Overall  Faithfulness  Relevancy
------------------------------------------------------------
1    2026-02-08 15:25:00    0.7875        0.8500     0.8000
2    2026-02-08 16:30:00    0.8350        0.9200     0.8500
3    2026-02-08 17:45:00    0.8600        0.9400     0.8700
4    2026-02-09 10:15:00    0.8800        0.9500     0.8900
5    2026-02-09 14:20:00    0.9100        0.9600     0.9200

------------------------------------------------------------
Total progress: +0.1225 (+15.6%)
```

### Markdown Report
Generates `tests/comparison_report.md` with:
- Metrics comparison table
- Change indicators (✅ Improved, ⚠️ Declined)
- Summary
- Recommendations for low scores

---

## 📈 Tracking Progress

### Files Created

1. **`ragas_results.json`** - Latest evaluation results
2. **`ragas_history.json`** - Historical results (last 20 runs)
3. **`comparison_report.md`** - Markdown comparison report

### Workflow

```
Run evaluation → Results saved to ragas_results.json
                ↓
Run comparison → Results added to ragas_history.json
                ↓
                → Comparison shown in terminal
                ↓
                → Report generated (comparison_report.md)
```

---

## 🎯 Interpreting Results

### Change Indicators

- **↑** - Metric improved
- **↓** - Metric declined  
- **=** - No change

### Status Indicators

- **✅ Improved** - Score increased
- **⚠️ Declined** - Score decreased
- **➖ No change** - Score stayed the same

---

## 💡 Example Usage

### Scenario: Testing Prompt Improvements

```bash
# 1. Baseline
python tests/evaluate_with_ragas.py
# Results: Overall 0.78

# 2. Improve prompt (add "use ONLY provided context")
# Edit app/graph/nodes.py

# 3. Re-evaluate
python tests/evaluate_with_ragas.py
# Results: Overall 0.85

# 4. Compare
python tests/compare_results.py
# Output: ✓ Overall improvement: +8.97%
#         Biggest improvement: faithfulness (+0.15)
```

### Scenario: Testing Re-Ranking

```bash
# 1. Baseline
python tests/evaluate_with_ragas.py
# Results: context_precision 0.75

# 2. Implement re-ranking
# Add re-ranking in app/graph/nodes.py

# 3. Re-evaluate
python tests/evaluate_with_ragas.py
# Results: context_precision 0.85

# 4. Compare
python tests/compare_results.py
# Output: Biggest improvement: context_precision (+0.10)
```

---

## 📝 Tips

### 1. Run Baseline First
Always run evaluation before making changes to establish baseline.

### 2. One Change at a Time
Make one improvement at a time to isolate impact.

### 3. Track in Git
Commit after each evaluation to correlate code changes with scores.

### 4. Review Reports
Check `comparison_report.md` for detailed analysis and recommendations.

### 5. Focus on Weak Areas
Prioritize improvements for metrics scoring < 0.75.

---

## 🔧 Troubleshooting

### "No results file found"
Run evaluation first: `python tests/evaluate_with_ragas.py`

### "Need at least 2 runs to compare"
Run evaluation twice (before and after changes).

### Results seem inconsistent
- LLM evaluation has some variance
- Run multiple times and average
- Focus on trends, not single runs

---

## 📚 Related Files

- [`ragas_test_data.py`](file:///d:/Users/vishal%20lad/workspace/first_python_project/tests/ragas_test_data.py) - Test dataset
- [`evaluate_with_ragas.py`](file:///d:/Users/vishal%20lad/workspace/first_python_project/tests/evaluate_with_ragas.py) - Evaluation script
- [`compare_results.py`](file:///d:/Users/vishal%20lad/workspace/first_python_project/tests/compare_results.py) - Comparison tool
- [`README.md`](file:///d:/Users/vishal%20lad/workspace/first_python_project/tests/README.md) - Full documentation

---

## Summary

**Two simple commands**:
1. `python tests/evaluate_with_ragas.py` - Run evaluation
2. `python tests/compare_results.py` - Compare results

That's it! Track your RAG improvements over time. 🎯
