# ◈ Smart Attendance System
## RFID × Facial Recognition — Linear Algebra Pipeline

> **Course:** UE24MA241B – Linear Algebra and Its Applications

---

## ◈ Team Details

| Name | SRN |
|:---|:---|
| D Harikrishnan | PES1UG24CS136 |
| Dhawal Pathak | PES1UG24CS151 |
| Vivian Sobers E | PES1UG24CS901 |
| Aryan Upadhyay | PES1UG25CS806 |
---
 
## ◈ Problem Statement

Manual attendance is slow and prone to proxy marking. This project solves that by pairing **RFID card identification** with **real-time face verification**. When a student taps their card, the system reads their identity and immediately captures a live photo. A linear algebra pipeline then compares the live face against a stored reference image. The outcome — **Present** or **Rejected** — is logged to a database and displayed on the Arduino's OLED screen.

> The mathematical core is built entirely on **vector and matrix operations**: image data enters as a matrix, gets transformed and normalised into a unit vector, and identity is confirmed through orthogonal projection.

---

## ◈ System Architecture Overview

```mermaid
flowchart TD
    A([🪪 Student Taps RFID Card]) --> B[Arduino UNO\nReads Card ID]
    B --> C[Serial → Python Backend]
    C --> D[Webcam Captures\nLive Frame]
    D --> E{Face Detected?}
    E -- No --> F([❌ Rejected — No Face])
    E -- Yes --> G[Linear Algebra\nPipeline]
    G --> H[DeepFace FaceNet512\nCosine Distance Check]
    H --> I{Distance < 0.40?}
    I -- Yes --> J([✅ Present — Logged to DB])
    I -- No --> K([❌ Rejected — Mismatch])
    J --> L[OLED Display\nGreen LED + Buzzer]
    K --> L

    style A fill:#1a1a2e,stroke:#00d4ff,color:#00d4ff
    style B fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style C fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style D fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style E fill:#0f3460,stroke:#00d4ff,color:#00d4ff
    style F fill:#2d0a0a,stroke:#ff4d4d,color:#ff4d4d
    style G fill:#0d1b2a,stroke:#00d4ff,color:#00d4ff
    style H fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style I fill:#0f3460,stroke:#00d4ff,color:#00d4ff
    style J fill:#0a2d1a,stroke:#00ff88,color:#00ff88
    style K fill:#2d0a0a,stroke:#ff4d4d,color:#ff4d4d
    style L fill:#1a1a2e,stroke:#7b2ff7,color:#e0e0e0
```

---

## ◈ Linear Algebra Pipeline

---

### Step 1 — Real-World Data → Matrix Representation

A face image loaded in grayscale maps each pixel to an intensity value between 0 (black) and 255 (white). Both the stored reference photo and the live webcam capture are resized to **64×64 pixels**:

$$A \in \mathbb{R}^{64 \times 64}$$

Each row of $A$ is a horizontal scan line; each entry is a brightness value. This is a direct application of matrices as linear transformations — the image is mapped from pixel space into a structured numerical form that algebraic operations can act on.

```mermaid
graph LR
    subgraph INPUT["📷 Image Input"]
        A[Raw Webcam Frame\n1920×1080 px]
    end
    subgraph PROC["⚙️ Processing"]
        B[Grayscale\nConversion]
        C[Resize to\n64×64 px]
    end
    subgraph OUT["🔢 Matrix"]
        D["A ∈ ℝ^(64×64)\n4096 values\n[0 ... 255]"]
    end
    A --> B --> C --> D

    style INPUT fill:#0d1b2a,stroke:#00d4ff,color:#00d4ff
    style PROC fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style OUT fill:#0a2d1a,stroke:#00ff88,color:#00ff88
    style A fill:#1a1a2e,stroke:#00d4ff,color:#e0e0e0
    style B fill:#1a1a2e,stroke:#7b2ff7,color:#e0e0e0
    style C fill:#1a1a2e,stroke:#7b2ff7,color:#e0e0e0
    style D fill:#0a2d1a,stroke:#00ff88,color:#00ff88
```

> **Topics Used:** Matrices · Linear Transformations · Matrix Representation of Data

---

### Step 2 — Matrix Simplification → Vectorisation

The 64×64 matrix is **flattened** into a single column vector of length 4096:

$$\mathbf{v} = \text{reshape}(A) \in \mathbb{R}^{4096}$$

This is a structure-preserving linear map — no pixel information is lost. The 2D layout is simply unrolled into 1D form, bringing the image into a space where dot products, norms, and projections apply directly.

```mermaid
graph LR
    A["Matrix A\n64×64\n(2D grid)"] -->|"reshape()"| B["Vector v\n4096×1\n(1D column)"]
    B --> C["✓ Dot products\n✓ Norms\n✓ Projections\n   now defined"]

    style A fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style B fill:#0f3460,stroke:#00d4ff,color:#00d4ff
    style C fill:#0a2d1a,stroke:#00ff88,color:#00ff88
```

> **Topics Used:** Linear Transformations · Matrix Reshaping

---

### Step 3 — Structure of the Space

Each face image, once flattened, is a **point in ℝ⁴⁰⁹⁶**. The reference image and the live capture are two vectors in this same high-dimensional space, and the goal is to determine how close they are in **direction**.

- The **column space** of the image matrix captures which intensity patterns are expressible by that face.
- The **rank** of the matrix indicates variation across the face — a plain image has low rank; a detailed face has higher rank.

```mermaid
graph TD
    subgraph SPACE["🌐 ℝ⁴⁰⁹⁶ — High-Dimensional Face Space"]
        A["📌 v_ref\nReference Vector\n(stored photo)"]
        B["📍 v_live\nLive Vector\n(webcam capture)"]
        C{{"θ = angle\nbetween vectors"}}
        A --- C
        B --- C
    end

    style SPACE fill:#0d1b2a,stroke:#00d4ff,color:#00d4ff
    style A fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style B fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style C fill:#0f3460,stroke:#00d4ff,color:#00d4ff
```

> **Topics Used:** Vector Spaces and Subspaces · Column Space · Rank

---

### Step 4 — Remove Redundancy → Normalisation

Two photos of the same person under different lighting produce vectors of very different **magnitudes**. Normalisation removes this redundancy:

$$\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|}$$

This projects both vectors onto the **unit hypersphere** in ℝ⁴⁰⁹⁶. After normalisation, only the **direction** matters — which corresponds to the geometric structure of the face, not the brightness.

```mermaid
graph LR
    subgraph BEFORE["Before Normalisation"]
        A["v_bright\n‖v‖ = 8200\n(well-lit photo)"]
        B["v_dark\n‖v‖ = 1400\n(dim photo)"]
    end
    subgraph AFTER["After Normalisation"]
        C["v̂_bright\n‖v̂‖ = 1.0"]
        D["v̂_dark\n‖v̂‖ = 1.0"]
    end
    A -->|"÷ ‖v‖"| C
    B -->|"÷ ‖v‖"| D
    C --> E(["✓ Same person\n   same direction"])
    D --> E

    style BEFORE fill:#2d1a0a,stroke:#ff9900,color:#ff9900
    style AFTER fill:#0a2d1a,stroke:#00ff88,color:#00ff88
    style A fill:#1a1a2e,stroke:#ff9900,color:#e0e0e0
    style B fill:#1a1a2e,stroke:#ff9900,color:#e0e0e0
    style C fill:#1a1a2e,stroke:#00ff88,color:#e0e0e0
    style D fill:#1a1a2e,stroke:#00ff88,color:#e0e0e0
    style E fill:#0a2d1a,stroke:#00ff88,color:#00ff88
```

> **Topics Used:** Norm and Unit Vectors · Basis Selection · Linear Independence

---

### Step 5 — Projection → Similarity Measurement

With both vectors normalised, similarity is computed via **orthogonal projection**. The live vector is projected onto the reference vector:

$$\text{projection} = \hat{\mathbf{v}}_{\text{ref}}^{\top} \times \hat{\mathbf{v}}_{\text{live}}$$

$$\text{confidence} = |\text{projection}| \times 100\%$$

This scalar measures how much of the live face vector aligns with the reference. When the two vectors point in nearly the same direction (same person), the projection is close to **1**. When they diverge (different person), the value drops toward **0**.

```mermaid
graph TD
    A["v̂_ref\n(Unit Reference Vector)"]
    B["v̂_live\n(Unit Live Vector)"]
    C["Dot Product\nv̂_ref · v̂_live"]
    D["Scalar Score\n∈ [0, 1]"]
    E["Confidence %\n= score × 100"]

    A --> C
    B --> C
    C --> D --> E

    style A fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style B fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style C fill:#0f3460,stroke:#00d4ff,color:#00d4ff
    style D fill:#0f3460,stroke:#00d4ff,color:#00d4ff
    style E fill:#0a2d1a,stroke:#00ff88,color:#00ff88
```

> **Topics Used:** Orthogonal Projections · Projection onto Subspaces · Dot Product as a Projection Operator

---

### Step 6 — Final Output → Attendance Decision

The projection score provides an interpretable similarity metric. The final decision uses a **DeepFace (FaceNet512) cosine distance check**:

$$\text{if distance} < 0.40 \Rightarrow \texttt{Status = Present}$$
$$\text{else} \Rightarrow \texttt{Status = Rejected}$$

Both scores are saved to a **SQLite database** alongside the student's SRN, name, timestamp, and captured photo path. The result is sent back to the Arduino over serial to update the OLED display and activate the green or red LED with a buzzer tone.

```mermaid
flowchart LR
    A["Cosine Distance\nComputed"] --> B{distance < 0.40?}
    B -- Yes --> C["🟢 PRESENT\nWrite to SQLite DB\nGreen LED + Buzzer"]
    B -- No --> D["🔴 REJECTED\nWrite to SQLite DB\nRed LED + Buzzer"]
    C --> E["OLED Display\nUpdated"]
    D --> E

    style A fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style B fill:#0f3460,stroke:#00d4ff,color:#00d4ff
    style C fill:#0a2d1a,stroke:#00ff88,color:#00ff88
    style D fill:#2d0a0a,stroke:#ff4d4d,color:#ff4d4d
    style E fill:#1a1a2e,stroke:#7b2ff7,color:#e0e0e0
```

> **Topics Used:** Projection-based Similarity Scoring · Threshold Classification · Pattern Detection

---

## ◈ Full Pipeline Summary

```mermaid
flowchart LR
    S1["Step 1\nMatrix\nRepresentation\nA ∈ ℝ^(64×64)"]
    S2["Step 2\nVectorisation\nv ∈ ℝ^4096"]
    S3["Step 3\nVector Space\nℝ^4096"]
    S4["Step 4\nNormalisation\n‖v̂‖ = 1"]
    S5["Step 5\nProjection\nv̂_ref · v̂_live"]
    S6["Step 6\nDecision\nPresent / Rejected"]

    S1 --> S2 --> S3 --> S4 --> S5 --> S6

    style S1 fill:#1a1a2e,stroke:#7b2ff7,color:#e0e0e0
    style S2 fill:#16213e,stroke:#7b2ff7,color:#e0e0e0
    style S3 fill:#0f3460,stroke:#00d4ff,color:#00d4ff
    style S4 fill:#0f3460,stroke:#00d4ff,color:#00d4ff
    style S5 fill:#0a2d1a,stroke:#00ff88,color:#00ff88
    style S6 fill:#0a2d1a,stroke:#00ff88,color:#00ff88
```

| Stage | Concept | What It Does |
|:---|:---|:---|
| Real-World Data | Matrix Representation | Face image loaded as a 64×64 pixel matrix |
| Matrix Simplification | Linear Transformation | Matrix flattened to a 4096-length vector |
| Structure of the Space | Vector Spaces, Column Space, Rank | Face vectors placed in ℝ⁴⁰⁹⁶ |
| Remove Redundancy | Normalisation, Basis Selection | Unit vectors isolate facial geometry from brightness |
| Projection | Orthogonal Projection, Dot Product | Measures directional similarity between two face vectors |
| Final Output | Pattern Detection, Classification | Present or Rejected decision logged and displayed |

---

*Report generated for UE24MA241B — Linear Algebra and Its Applications*
