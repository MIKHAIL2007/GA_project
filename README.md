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
- Otherwise Carter proximity cost:
  - distance 1–5 slots → weights 16, 8, 4, 2, 1
- minimise the average penalty per student, no clash students.
- In the GA treating lower penalty as better fitness.

## Algorithm
A simple GA with a “feasible-first” approach:
- building the conflict graph from `.stu`.
- generating the initial population using greedy graph colouring, so starts from schedules with zero (or near zero) clashes.
- After crossover/mutation we apply a light graph-based repair to keep the hard constraint satisfied.
- Operators:
  - tournament selection
  - uniform crossover
  - neighbour-aware mutation (tries not to put an exam into a slot used by its conflicting neighbours)

## Run
- Put `ear-f-83-2.crs` and `ear-f-83-2.stu` into `data/`
- Run:
  - `python main.py`

## Results
The hard constraint was satisfied throughout the main optimisation phase:
- `clash_students` quickly reached 0 and stayed 0.
- The GA then focused on improving the soft objective.
- instead of spending most of the search trying to fix collisions, the GA spends its budget improving student comfort.

## Conclusions
I built a simple GA that reliably maintains feasibility and improves the Carter penalty; the main benefit comes from starting with a greedy feasible population and using lightweight repair to keep hard constraints satisfied.

