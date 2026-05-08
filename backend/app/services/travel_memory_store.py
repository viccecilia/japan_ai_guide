from copy import deepcopy

from app.schemas.travel_memory import MemorySnapshot, TravelMemory


_MEMORY_STORE: dict[str, TravelMemory] = {}


def load_memory(session_id: str) -> TravelMemory:
    if session_id not in _MEMORY_STORE:
        _MEMORY_STORE[session_id] = TravelMemory(session_id=session_id)
    return deepcopy(_MEMORY_STORE[session_id])


def save_memory(memory: TravelMemory) -> TravelMemory:
    _MEMORY_STORE[memory.session_id] = deepcopy(memory)
    return deepcopy(memory)


def update_memory(session_id: str, memory: TravelMemory) -> TravelMemory:
    memory.session_id = session_id
    memory.memory_updates += 1
    return save_memory(memory)


def get_memory_snapshot(session_id: str) -> MemorySnapshot:
    memory = load_memory(session_id)
    return MemorySnapshot(
        session_id=session_id,
        preference=memory.preference,
        summary=_summary(memory),
        evolution=memory.evolution[-5:],
    )


def clear_memory(session_id: str) -> None:
    _MEMORY_STORE.pop(session_id, None)


def _summary(memory: TravelMemory) -> str:
    pace = {
        "slow": "慢节奏",
        "normal": "均衡节奏",
        "dense": "充实节奏",
    }.get(memory.preference.preferred_pace, "均衡节奏")
    persona = {
        "culture": "文化体验",
        "foodie": "美食探索",
        "elder": "少步行路线",
        "family": "亲子轻松路线",
        "couple": "情侣散步路线",
        "first_time": "第一次来日本路线",
    }.get(memory.preference.preferred_persona, "日本旅行路线")
    return f"AI 已记住你更偏好{pace}和{persona}。"
