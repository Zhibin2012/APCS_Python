import json
import sys
from jsonschema import validate, ValidationError

def run_validation():
    try:
        with open("data/knowledge_apcs_python.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        with open("data/schema.json", "r", encoding="utf-8") as f:
            schema = json.load(f)

        validate(instance=data, schema=schema)
        print("✅ 驗證通過：資料符合 Schema 規範。")
    except ValidationError as e:
        print(f"❌ 驗證失敗：{e.message}")
        print(f"路徑：{list(e.path)}")
        sys.exit(1)
    except Exception as e:
        print(f"💥 發生非預期錯誤：{e}")
        sys.exit(1)

if __name__ == "__main__":
    run_validation()
