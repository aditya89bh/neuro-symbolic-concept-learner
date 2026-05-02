# 🧠 Neuro-Symbolic Concept Learner (NSCL)

### Toward interpretable reasoning systems for AGI

Most modern AI systems are powerful but opaque.  
They generate answers, but cannot explain *how* they arrived at them.

This project explores a different direction:

> Building systems that **reason, explain, and operate over structured concepts**

---

# 🚀 What this project does

This is a minimal neuro-symbolic reasoning system that:

- Represents a scene as structured objects  
- Converts natural language questions into symbolic programs  
- Executes reasoning over those programs  
- Produces answers with **step-by-step reasoning traces**

---

# ⚙️ System Pipeline

Language → Parser → Symbolic Program → Executor → Answer + Trace

### Components:

- **Scene Graph** → structured world representation  
- **Parser** → converts language into logic  
- **Executor** → runs symbolic reasoning  
- **Trace Engine** → explains every step  

---

# 🧩 Example

### Question
What is left of the blue sphere?

### Parsed Program
filter(color=blue) → filter(shape=sphere) → relate(left_of) → query(color)

### Answer
red

### Reasoning Trace
- Filtered objects where color=blue
- Filtered objects where shape=sphere
- Applied relation left_of on obj_2
- Queried attribute color

---

# 🏗️ Scene Representation

The system operates on structured scenes:

- Objects are defined with:
  - shape
  - color
  - size
  - position (x, y)

This enables **deterministic, interpretable reasoning**, unlike purely neural approaches.

---

# 🧠 Reasoning Capabilities

The system currently supports:

- Attribute filtering (color, shape, size)  
- Spatial relations (left, right, above, below)  
- Attribute queries  
- Counting  
- Existence checks  

---

# 🔍 Why this matters

Most AI systems today are:

- Black-box
- Hard to debug
- Difficult to trust

This project explores a hybrid approach:

> **Structured representations + symbolic reasoning**

This direction is important for:

- Compositional reasoning  
- Explainability  
- Robust generalization  
- Foundations of AGI  

---

# 🎯 Design Philosophy

> Every answer must be explainable

- No hidden reasoning  
- No opaque outputs  
- Every step is traceable  

The goal is not just intelligence, but **understandable intelligence**.

---

# ⚠️ Current Limitations

- Uses structured scenes (no real visual perception yet)  
- Rule-based language parser  
- Limited reasoning depth  
- No learning or memory across tasks  

---

# 🔮 Future Directions

- Replace structured scenes with visual perception  
- Learn concepts instead of predefined attributes  
- Add memory for temporal reasoning  
- Extend to embodied systems (robotics)  
- Move toward **interpretable, general intelligence systems**

---

# 🧪 Running the Demo

```bash
python src/demo.py
```

---

# 🧭 Positioning

This is not a production system.

This is an **early-stage AGI reasoning prototype** exploring:

- Neuro-symbolic architectures  
- Interpretable reasoning  
- Structured intelligence systems  

---

# ⚡ Summary

Language → Logic → Reasoning → Answer → Explanation

A small but meaningful step toward **systems that think, not just predict**.
