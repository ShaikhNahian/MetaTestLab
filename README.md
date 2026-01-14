
## MetaTestLab

MetaTestLab is a hands-on project I am using to **learn and apply metamorphic testing (MT)** by building a small, extensible testing framework and applying it to realistic systems.

The focus of the project is not just implementing MT mechanically, but understanding **how different metamorphic relations behave in practice**, what kinds of faults they reveal, and where their limitations lie—particularly in systems that include machine learning components.

---

## Motivation

I started MetaTestLab to move beyond learning theoretical descriptions of metamorphic testing and explore how it works on real code. Many modern systems, especially ML-based ones, lack reliable test oracles, making traditional testing approaches insufficient or misleading.

Metamorphic testing offers an alternative: instead of checking whether an output is “correct,” it checks whether the system behaves **consistently and sensibly under controlled input transformations**.

I’m also interested in how MT works in combination with fuzzing. Random input generation is useful, but in practice it can be slow to reach the edge cases that matter. This is where **bug-directed fuzzing** becomes interesting: instead of exploring inputs blindly, the goal is to guide input generation toward regions where failures are more likely (for example, near an ML decision boundary).

This project reflects my attempt to:

- learn MT concepts through implementation rather than only reading
- understand which fault classes different MRs can detect
- explore oracle-free testing strategies for ML-heavy systems
- experiment with both broad fuzzing and bug-directed counterexample discovery

---

## What MetaTestLab Currently Does (Mid January - 2026)

MetaTestLab implements a lightweight metamorphic testing framework and applies it to both **algorithmic code** and **machine learning pipelines**.

Key features include:

- **Black-box testing** via simple callable interfaces (e.g., `predict(x)`)
- **Oracle-free testing**, without ground-truth labels
- Multiple classes of metamorphic relations:
  - invariance relations (noise robustness, feature scaling)
  - change-sensitive relations (feature perturbation sensitivity)
  - side-effect relations (input purity / no mutation)
- **Failure interpretation**, classifying detected issues as robustness, sensitivity, or purity failures

I’ve tried to keep the framework intentionally simple, so that the behavior of each MR is easy to reason about and extend.

---

## Fuzzing Support (Hypothesis + Bug-Directed)

To explore metamorphic relations at scale, MetaTestLab integrates fuzzing in two ways:

### 1) Hypothesis-based fuzzing (property-based testing)

- Automatically generates diverse source inputs for metamorphic tests
- Helps discover edge cases quickly
- Produces reproducible failing examples (counterexamples)

### 2) Bug-directed fuzzing (boundary-seeking)

- Implements a directed search approach for ML systems
- Uses prediction probabilities to push inputs toward the decision boundary
- Helps find robustness counterexamples faster than random input generation

---

## Machine Learning Focus

A major part of MetaTestLab focuses on **testing ML systems**.

The project includes:

- a black-box ML classifier accessed only through a prediction interface
- metamorphic relations that test robustness, sensitivity, and pipeline correctness
- fault-injection experiments such as **in-place preprocessing bugs**, which often go unnoticed by accuracy-based testing but are reliably detected using MT

The goal here is not model performance, but **behavioral correctness and pipeline reliability**.

---

## Counterexample Artifacts

When a counterexample is discovered (for example, an MR violation found via bug-directed fuzzing), MetaTestLab can save it as a JSON artifact under: artifacts/counterexamples/

These artifacts capture the source input, follow-up input, outputs, MR name, and failure type, making failures easier to reproduce and analyze.

---

## How to Run Tests

### 1) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2) Install dependencies

<pre class="overflow-visible! px-0!" data-start="4488" data-end="4531"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -r requirements.txt
</span></span></code></div></div></pre>

### 3) Run the full test suite

<pre class="overflow-visible! px-0!" data-start="4564" data-end="4598"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m pytest -v -s</span></span></code></div></div></pre>
