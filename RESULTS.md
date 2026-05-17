# Results

## Demo Results

### Question
What color is the cube?

### Parsed Program
filter(shape=cube) → query(color)

### Answer
red

### Trace
- Filtered objects where shape=cube
- Queried attribute color

---

### Question
What is left of the blue sphere?

### Parsed Program
filter(color=blue) → filter(shape=sphere) → relate(left_of) → query(color)

### Answer
red

### Trace
- Filtered objects where color=blue
- Filtered objects where shape=sphere
- Applied relation left_of on obj_2
- Queried attribute color

---

## Evaluation Results

### Evaluation Summary

```text
Total questions: 6
Correct answers: 6
Accuracy: 100%
Failed parses: 0
Trace coverage: 100%
```

### Supported Query Types

- Attribute queries
- Spatial relation queries
- Count queries
- Existence queries

### Current Limitations

- Structured scenes only
- Rule-based parser
- No neural perception
- No learned concepts
- No memory across tasks

### Future Work

- Add neural perception layer
- Learn concepts dynamically
- Add persistent memory
- Expand reasoning depth
- Connect symbolic reasoning to embodied systems
