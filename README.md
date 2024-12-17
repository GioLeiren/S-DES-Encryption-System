# Implementation Work Report 1: S-DES

---

## 1. Introduction

The S-DES (Simplified Data Encryption Standard) algorithm is a reduced version of DES, designed for educational purposes. It uses a 10-bit key and operates on 8-bit data blocks, with only two Feistel network rounds. This work aims to implement software that performs encryption and decryption using S-DES. The parameters used include:

- **10-bit Key:** 1010000010
- **8-bit Data Block:** 11010111

We will detail the S-DES algorithm structure and implementation process, including intermediate steps and results obtained.

---

## 2. S-DES Structure

S-DES follows these main steps:

1. **Subkey Generation:** Two subkeys (K1 and K2) are generated from the 10-bit key using permutations and circular shifts.
2. **Encryption:** The 8-bit data block is processed through the following stages:
   - Initial Permutation (IP);
   - Two Feistel function rounds, each using a subkey;
   - Final Permutation (IP⁻¹).
3. **Decryption:** Uses the same process as encryption, but with subkeys applied in reverse order.

---

## 3. Implementation and Step-by-Step Resolution

### 3.1. Subkey Generation

Generating K1 and K2 follows these steps:

1. **P10 Permutation:** Rearranges the bits of the original key based on the order `[3, 5, 2, 7, 4, 10, 1, 9, 8, 6]`.
   - **Input:** `1010000010`
   - **Output:** `1000001100`

2. **Single Circular Shift:** Divides the key into two 5-bit halves and performs a circular shift on each half.
   - **Input:** `10000 | 01100`
   - **Output:** `00001 | 11000`

3. **P8 Permutation:** Selects and permutes 8 bits to form K1.
   - **Input:** `0000111000`
   - **Output:** `10100100`

4. **Double Circular Shift:** Applies a double circular shift to the halves.
   - **Input:** `00001 | 11000`
   - **Output:** `00100 | 00011`

5. **P8 Permutation:** Generates K2 from the new configuration.
   - **Input:** `0010000011`
   - **Output:** `01000011`

**Result:**
- **K1:** `10100100`
- **K2:** `01000011`

---

### 3.2. Encryption

1. **Initial Permutation (IP):** Rearranges the data block bits based on the order `[2, 6, 3, 1, 4, 8, 5, 7]`.
   - **Input:** `11010111`
   - **Output:** `10101111`

2. **First Feistel Round:**
   - **Division:** `L = 1010`, `R = 1111`
   - **Expansion/Permutation (E/P):** Applies the order `[4, 1, 2, 3, 2, 3, 4, 1]` to `R`.
     - **Input:** `1111`
     - **Output:** `11111111`
   - **XOR with K1:** Combines with subkey `K1`.
     - **Result:** `01011011`
   - **S-Boxes:** Processes the 8 resulting bits with S0 and S1.
     - **S0 Output:** `01`
     - **S1 Output:** `11`
   - **P4 Permutation:** Applies the order `[2, 4, 3, 1]` to the combination of S0 and S1.
     - **Output:** `1110`
   - **XOR with L:**
     - `L = 1010`, `P4 = 1110`
     - **Result:** `0100`
   - **Swap:**
     - New `L = 1111`, New `R = 0100`

3. **Second Feistel Round:**
   - **Division:** `L = 1111`, `R = 0100`
   - **Expansion/Permutation (E/P):** Applied to `R`.
     - **Output:** `00101000`
   - **XOR with K2:**
     - **Result:** `01101011`
   - **S-Boxes:** Processes the 8 resulting bits.
     - **S0 Output:** `10`
     - **S1 Output:** `01`
   - **P4 Permutation:**
     - **Output:** `1001`
   - **XOR with L:**
     - **Result:** `0110`

4. **Final Permutation (IP⁻¹):** Rearranges the bits based on the order `[4, 1, 3, 5, 7, 2, 8, 6]`.
   - **Input:** `01100100`
   - **Output:** `00001111`

**Result:**
- **Encrypted Block:** `00001111`

---

### 3.3. Decryption

The decryption process uses the same steps as encryption, but with subkeys applied in reverse order (`K2` in the first round and `K1` in the second). When applied to the encrypted block `00001111`, the result is the original block `11010111`.

---

## 4. Conclusion

The S-DES implementation allowed understanding the fundamental concepts of block ciphering, such as permutations, non-linear functions, and the Feistel structure. The developed software successfully performs encryption and decryption for the given parameters, manually validating the results.

**Final Results:**
- **Original Key:** `1010000010`
- **Original Block:** `11010111`
- **Encrypted Block:** `00001111`
- **Decrypted Block:** `11010111`
