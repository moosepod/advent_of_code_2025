.PHONY: day-1-silver day-1-gold day-2-silver-day-2-gold

day-5-gold: day_5/day_5.py
	uv run day_5/day_5.py gold

day-5-silver: day_5/day_5.py
	uv run day_5/day_5.py silver

day-4-gold: day_4/day_4.py
	uv run day_4/day_4.py gold

day-4-silver: day_4/day_4.py
	uv run day_4/day_4.py silver

day-3-gold: day_3/day_3.py
	uv run day_3/day_3.py gold

day-3-silver: day_3/day_3.py
	uv run day_3/day_3.py silver

day-2-gold: day_2/day_2.py
	uv run day_2/day_2.py gold

day-2-silver: day_2/day_2.py
	uv run day_2/day_2.py silver

day-1-gold: day_1/day_1.py
	uv run day_1/day_1.py gold

day-1-silver: day_1/day_1.py
	uv run day_1/day_1.py silver


