# 🧠 Reasoning Examples

This document showcases how the system converts natural language questions into symbolic programs and executes them with full reasoning traces.

---

## Example 1: Attribute Query

**Question**  
What color is the cube?

**Program**  
filter(shape=cube) → query(color)

**Answer**  
red

**Trace**  
- Filtered objects where shape=cube  
- Queried attribute color  

---

## Example 2: Relation Query

**Question**  
What is left of the blue sphere?

**Program**  
filter(color=blue) → filter(shape=sphere) → relate(left_of) → query(color)

**Answer**  
red

**Trace**  
- Filtered objects where color=blue  
- Filtered objects where shape=sphere  
- Applied relation left_of on obj_2  
- Queried attribute color  

---

## Example 3: Count Query

**Question**  
How many small objects are there?

**Program**  
filter(size=small) → count

**Answer**  
2

**Trace**  
- Filtered objects where size=small  
- Counted objects  

---

## Example 4: Existence Query

**Question**  
Is there a green cylinder?

**Program**  
filter(color=green) → filter(shape=cylinder) → exist

**Answer**  
True

**Trace**  
- Filtered objects where color=green  
- Filtered objects where shape=cylinder  
- Checked existence  

---

## Example 5: Multi-step Reasoning

**Question**  
What color is the object right of the red cube?

**Program**  
filter(color=red) → filter(shape=cube) → relate(right_of) → query(color)

**Answer**  
blue

**Trace**  
- Filtered objects where color=red  
- Filtered objects where shape=cube  
- Applied relation right_of on obj_1  
- Queried attribute color  

---

## Summary

These examples demonstrate the core loop:

Language → Symbolic Program → Reasoning → Answer → Explanation

The system prioritizes interpretability, ensuring every output is traceable and understandable.
