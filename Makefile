.PHONY: day-1-silver

day-1-silver: day_1/day_1.py
	uv run day_1/day_1.py silver

day-1-gold: day_1/day_1.py
	uv run day_1/day_1.py gold

