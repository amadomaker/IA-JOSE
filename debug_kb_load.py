from src.kb.loader import load_kb
from src.core.config import KnowledgeBaseConfig
import sys

print(f"Trying to load KB from: {KnowledgeBaseConfig.KB_PATH}")
try:
    kb = load_kb(KnowledgeBaseConfig.KB_PATH)
    print(f"SUCCESS! Loaded {len(kb)} entries")
except Exception as e:
    print(f"FAILURE! Error: {e}")
    sys.exit(1)
