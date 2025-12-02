.PHONY: day-1-silver day-1-gold day-2-silver-day-2-gold

day-2-gold: day_2/day_2.py
	uv run day_2/day_2.py gold

day-2-silver: day_2/day_2.py
	uv run day_2/day_2.py silver

day-1-gold: day_1/day_1.py
	uv run day_1/day_1.py gold

day-1-silver: day_1/day_1.py
	uv run day_1/day_1.py silver


