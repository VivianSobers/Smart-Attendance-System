# Smart Attendance System Using RFID and Facial Recognition


## **Course:** UE24MA241B – Linear Algebra and Its Applications


## Team

| Name | SRN |
|---|---|
| D Harikrishnan | PES1UG24CS136 |
| Dhawal Pathak | PES1UG24CS151 |
| Vivian Sobers E | PES1UG24CS901 |
| Aryan Upadhyay | PES1UG25CS806 |


## Problem Statement

Manual attendance is slow and prone to proxy marking. This project solves that by pairing RFID card identification with real-time face verification. When a student taps their card, the system reads their identity from the card and immediately captures a live photo. A linear algebra pipeline then compares the live face against a stored reference image. The outcome either Present or Rejected is logged to a database and displayed on the Arduino's OLED screen.

The mathematical core of the system is built entirely on vector and matrix operations: image data enters as a matrix, gets transformed and normalized into a unit vector, and identity is confirmed through orthogonal projection.

___

## Linear Algebra Flow


### Step 1: Real-World Data to Matrix Representation

A face image is a grid of pixel intensity values. When loaded in grayscale, each pixel holds a value between 0 (black) and 255 (white). Both the stored reference photo and the live webcam capture are resized to 64x64 pixels, giving a matrix:

```
A ∈ ℝ^(64×64)
```

Each row of A is a horizontal scan line of the face. Each entry is a brightness value. Representing the image this way is a direct application of matrices as linear transformations — the image is mapped from pixel space into a structured numerical form that algebraic operations can act on.

**Topics Used:**
- Matrices
- Linear Transformations
- Matrix Representation of Data

___

### Step 2: Matrix Simplification — Vectorisation

The 64x64 matrix is flattened into a single column vector of length 4096:

```
v = reshape(A) ∈ ℝ^4096
```

This is a structure-preserving linear map. No pixel information is lost — the 2D layout is simply unrolled into a 1D form. The reason for this step is practical: dot products, norms, and projections are defined on vectors, not on 2D matrices. Flattening brings the image into a space where these operations apply directly.

**Topics Used:**
- Linear Transformations
- Matrix Reshaping

___

### Step 3: Structure of the Space

Each face image, once flattened, is a point in ℝ^4096. The entire set of possible face images forms a subspace within this high-dimensional space. The reference image and the live capture are two vectors in the same space, and the goal is to determine how close together they are in direction.

The column space of the original image matrix captures which intensity patterns are expressible by that face. The rank of the matrix indicates how much variation exists across the face — a plain, featureless image has low rank; a detailed face has higher rank.

**Topics Used:**
- Vector Spaces and Subspaces
- Column Space
- Rank

___

### Step 4: Remove Redundancy — Normalisation

Two photos of the same person taken under different lighting will produce vectors of very different magnitudes. If compared directly, a brighter photo would dominate simply because its values are larger, not because the face is different. This is redundant information that must be removed before comparison.

Each vector is normalised to unit length:

```
v̂ = v / ||v||
```

This projects both vectors onto the unit hypersphere in ℝ^4096. After normalisation, only the direction of the vector matters — which corresponds to the geometric structure of the face, not the brightness. Normalisation is equivalent to selecting a representative basis vector for the direction the image points in.

**Topics Used:**
- Norm and Unit Vectors
- Basis Selection
- Linear Independence

___

### Step 5: Projection — Similarity Measurement

With both the reference vector v̂_ref and the live vector v̂_live normalised, the similarity between them is computed using orthogonal projection. The live vector is projected onto the reference vector:

```
projection = v̂_ref^T × v̂_live
```

This scalar measures how much of the live face vector aligns with the reference. When the two vectors point in nearly the same direction (same person, similar lighting), the projection is close to 1. When they diverge (different person), the value drops. The similarity score reported by the system is:

```
confidence = |projection| × 100
```

This gives a percentage that is logged alongside every attendance record.

**Topics Used:**
- Orthogonal Projections
- Projection onto Subspaces
- Dot Product as a Projection Operator

___

### Step 6: Final Application Output — Attendance Decision

The projection score provides an interpretable similarity metric. The final attendance decision uses a DeepFace (FaceNet512) cosine distance check alongside it:

```
if distance < 0.40  →  Status = Present
else                →  Status = Rejected
```

Both scores are saved to a SQLite database along with the student's SRN, name, timestamp, and the path to the captured photo. The result is sent back to the Arduino over serial, which updates the OLED display and activates the green or red LED with a buzzer tone.

**Topics Used:**
- Projection-based Similarity Scoring
- Threshold Classification
- Pattern Detection


___

## Pipeline Summary

| Stage | Concept | What It Does |
|---|---|---|
| Real-World Data | Matrix Representation | Face image loaded as a 64x64 pixel matrix |
| Matrix Simplification | Linear Transformation | Matrix flattened to a 4096-length vector |
| Structure of the Space | Vector Spaces, Column Space, Rank | Face vectors placed in ℝ^4096 |
| Remove Redundancy | Normalisation, Basis Selection | Unit vectors isolate facial geometry from brightness |
| Projection | Orthogonal Projection, Dot Product | Measures directional similarity between two face vectors |
| Final Output | Pattern Detection, Classification | Present or Rejected decision logged and displayed |

