## MetaTestLab

MetaTestLab is a hands-on project I am using to **learn and apply metamorphic testing (MT)** by building a small, extensible testing framework and applying it to realistic systems.

The focus of the project is not just implementing MT mechanically, but understanding  **how different metamorphic relations behave in practice** , what kinds of faults they reveal, and where their limitations lie—particularly in systems that include machine learning components.

---

## Motivation

I started MetaTestLab to move beyond learning theoretical descriptions of metamorphic testing and explore how it works on real code. Many modern systems, especially ML-based ones, lack reliable test oracles, making traditional testing approaches insufficient or misleading.

Metamorphic testing offers an alternative: instead of checking whether an output is “correct,” it checks whether the system behaves  **consistently and sensibly under controlled input transformations** .

This project reflects my attempt to:

* learn MT concepts through implementation rather than only reading
* understand which fault classes different MRs can detect
* explore MT as a practical testing strategy for ML-heavy systems

---

## What MetaTestLab Currently Does (Mid January - 2026)

MetaTestLab implements a lightweight metamorphic testing framework and applies it to both **algorithmic code** and  **machine learning pipelines** .

Key features include:

* **Black-box testing** via simple callable interfaces (e.g., `predict(x)`)
* **Oracle-free testing** , without ground-truth labels
* Multiple classes of metamorphic relations:
  * invariance relations (noise robustness, feature scaling)
  * change-sensitive relations (feature perturbation sensitivity)
  * side-effect relations (input purity / no mutation)
* **Failure interpretation** , classifying detected issues as robustness, sensitivity, or purity failures

I've tried to keep The framework is intentionally simple, so that the behavior of each MR is easy to reason about and extend.

---

## Machine Learning Focus

A major part of MetaTestLab focuses **testing ML systems** .

The project includes:

* a black-box ML classifier accessed only through a prediction interface
* metamorphic relations that test robustness, sensitivity, and pipeline correctness
* fault-injection experiments such as  **in-place preprocessing bugs** , which often go unnoticed by accuracy-based testing but are reliably detected using MT

The goal here is not model performance, but  **behavioral correctness and pipeline reliability** .

---

## Immediate Next Goal

The next step for MetaTestLab is to apply the framework to a  **real, fully functioning sample web application** .

Planned work includes:

* selecting or deploying a web application that exposes:
  * REST APIs
  * ML or LLM-based components (e.g., search, recommendation, text processing)
* treating the application as the **System Under Test**
* using MetaTestLab to:
  * perform metamorphic testing on APIs (pagination, filtering, parameter sensitivity)
  * test ML/LLM modules using robustness, sensitivity, and purity relations

With this step I plan to learn how I can integrate MT in **practical testing workflow of modern, ML-enabled systems** .

---

**MetaTestLab is a learning-driven project rather than a finished tool. It reflects an ongoing effort to understand:**

* how metamorphic testing behaves on real systems
* how different MRs expose different fault classes
* how MT can complement traditional testing for ML and API-based systems

**The framework is designed to evolve as new systems and metamorphic relations are added.**
