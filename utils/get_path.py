import os

def get_group_file_path(group_id: str) -> str:
    data_dir = os.getenv("GROUP_TEXT_DIR", "/home/aiserver/Desktop/IBComm_RAG/group_texts")
    return os.path.join(data_dir, f"{group_id}.txt")
