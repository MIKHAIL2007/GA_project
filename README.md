# Exam Timetabling – Genetic Algorithm

## Problem
- Exam timetabling (Carter benchmark)
- Assign exams to time slots
- No student with two exams in one slot (hard)
- Spread conflicting exams apart in time (soft)

## Data
- Toronto exam timetabling benchmark
- Instance: EAR-F-83-2 (`.crs`, `.stu`)

## Encoding (Chromosome)
- Vector of length = number of exams
- Index = exam id
- Value = time slot (0 … T−1)

## Fitness Function
- Infeasible (clash for any student) → very large penalty
- Otherwise Carter proximity cost:
  - distance 1–5 slots → weights 16, 8, 4, 2, 1
- GA maximises `fitness = - penalty`
