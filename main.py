from ga_timetable import run
best, fit, info = run(
    "data/ear-f-83-2.crs",
    "data/ear-f-83-2.stu",
    t=24,
    ps=140,
    g=100,
    cx=0.8,
    mu=0.02,
    k=3,
    v=True,
    seed=2,
    pr=10
)

print(info)