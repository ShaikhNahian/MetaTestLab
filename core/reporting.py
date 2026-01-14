import json
import os
from datetime import datetime


def _to_json_safe(obj):
    """
    Convert numpy types and other non-serializable objects into JSON-safe values.
    """
    try:
        # numpy scalars have .item()
        return obj.item()
    except Exception:
        pass

    if isinstance(obj, (list, tuple)):
        return [_to_json_safe(x) for x in obj]

    if isinstance(obj, dict):
        return {k: _to_json_safe(v) for k, v in obj.items()}

    return obj


def save_counterexample(result, failure_type, sut_name="sut", out_dir="artifacts/counterexamples"):
    """
    Save a counterexample (MR failure) as a JSON artifact.
    """
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mr_name = result.get("mr", "UnknownMR")

    filename = f"{timestamp}__{sut_name}__{mr_name}__{failure_type}.json"
    path = os.path.join(out_dir, filename)

    payload = {
        "timestamp": timestamp,
        "sut": sut_name,
        "mr": mr_name,
        "failure_type": failure_type,
        "source_input": result.get("source_input"),
        "follow_up_input": result.get("follow_up_input"),
        "source_output": result.get("source_output"),
        "follow_up_output": result.get("follow_up_output"),
        "passed": result.get("passed"),
        "input_mutated": result.get("input_mutated"),
    }

    payload = _to_json_safe(payload)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    return path
