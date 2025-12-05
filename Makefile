.PHONY: day-1-1 day-1-2 day-2-1 day-2-2 day-3-1 day-3-2 day-4-1 day-4-2 day-5-1 day-5-2

day-5-2: day_5/day_5.py
	uv run day_5/day_5.py 2

day-5-1: day_5/day_5.py
	uv run day_5/day_5.py 1

day-4-2: day_4/day_4.py
	uv run day_4/day_4.py 2

day-4-1: day_4/day_4.py
	uv run day_4/day_4.py 1

day-3-2: day_3/day_3.py
	uv run day_3/day_3.py 2

day-3-1: day_3/day_3.py
	uv run day_3/day_3.py 1

day-2-2: day_2/day_2.py
	uv run day_2/day_2.py 2

day-2-1: day_2/day_2.py
	uv run day_2/day_2.py 1

day-1-2: day_1/day_1.py
	uv run day_1/day_1.py 2

day-1-1: day_1/day_1.py
	uv run day_1/day_1.py 1


