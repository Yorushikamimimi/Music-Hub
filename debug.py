import traceback
import sys

try:
    import app
except Exception as e:
    with open('debug.log', 'w', encoding='utf-8') as f:
        traceback.print_exc(file=f)
