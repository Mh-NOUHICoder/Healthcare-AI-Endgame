from typing import Any, Dict, Optional, List
import uuid

def build_a2a_response(
    request_id: Any,
    task_id: str,
    state: str,
    text: str,
    metadata: Optional[Dict[str, Any]] = None,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Builds a JSON-RPC 2.0 compliant A2A response.
    """
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "id": task_id,
            "status": {
                "state": state,
                "result": {
                    "text": text
                }
            },
            "metadata": metadata or {},
            "sessionId": session_id
        }
    }

def build_a2a_error_response(
    request_id: Any,
    code: int,
    message: str,
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Builds a JSON-RPC 2.0 compliant A2A error response.
    """
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message,
            "data": data
        }
    }

def extract_a2a_text(params: Dict[str, Any]) -> str:
    """
    Extracts plain text from A2A message parts.
    Handles 'input.text', 'message.text', and 'message.parts' formats.
    """
    if not params:
        return ""
        
    # 1. Try 'input.text' (Common in some A2A implementations)
    input_data = params.get("input", {})
    if isinstance(input_data, dict) and input_data.get("text"):
        return str(input_data.get("text"))
        
    # 2. Try 'message' field
    message = params.get("message")
    if not message:
        # Fallback to any 'text' or 'content' at top level of params
        return str(params.get("text", params.get("content", "")))
        
    if isinstance(message, str):
        return message
        
    # 3. Try 'message.parts'
    parts = message.get("parts", [])
    if not parts:
        return str(message.get("text", message.get("content", "")))
        
    text_parts = []
    for part in parts:
        if not part: continue
        if part.get("type") == "text" or part.get("kind") == "text":
            text_parts.append(str(part.get("text", part.get("content", ""))))
            
    return "\n".join(text_parts)
