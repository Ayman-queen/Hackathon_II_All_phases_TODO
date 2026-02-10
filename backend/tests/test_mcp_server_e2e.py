import httpx
import json
import uuid

BASE_URL = "http://localhost:8001/mcp"
USER_ID = "w2PYO9wq2FGP2fR111aTZkbPWD5ZyJPC"
TASK_ID = "ca0ca8bb-7ffe-4071-baa2-848ed4937430"

def create_request(method, params=None, request_id=1):
    return {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": request_id,
    }

def get_headers():
    return {
        "X-User-ID": USER_ID,
        "X-Internal-Secret": "mcp-internal-secret-change-in-production",
    }

def print_test_result(test_name, success, response=None, error=None):
    status = "PASS" if success else "FAIL"
    print(f"Test: {test_name} - Status: {status}")
    if response:
        print(f"  Response: {json.dumps(response, indent=2)}")
    if error:
        print(f"  Error: {error}")
    print("-" * 20)

def run_tests():
    test_results = []

    with httpx.Client(timeout=30.0) as client:
        headers = get_headers()
        # Test 1: Initialize
        try:
            request = create_request("initialize")
            response = client.post(BASE_URL, json=request, headers=headers)
            response.raise_for_status()
            data = response.json()
            success = "result" in data and data["result"]["serverInfo"]["name"] == "Todo MCP Server"
            test_results.append(("Initialize", success, {"response": data}))
        except Exception as e:
            test_results.append(("Initialize", False, {"error": str(e)}))

        # Test 2: List Tools
        try:
            request = create_request("tools/list")
            response = client.post(BASE_URL, json=request, headers=headers)
            response.raise_for_status()
            data = response.json()
            success = "result" in data and "tools" in data["result"]
            test_results.append(("List Tools", success, {"response": data}))
            tools = [t["name"] for t in data["result"]["tools"]] if success else []
        except Exception as e:
            test_results.append(("List Tools", False, {"error": str(e)}))
            tools = []

        # Test 3: Add Task
        task_id = None
        try:
            task_title = f"Test Task E2E - {uuid.uuid4()}"
            params = {"name": "add_task", "arguments": {"user_id": USER_ID, "title": task_title}}
            request = create_request("tools/call", params)
            response = client.post(BASE_URL, json=request, headers=headers)
            response.raise_for_status()
            data = response.json()
            success = "result" in data
            if success:
                # Extract task_id from the response text
                text = data["result"]["content"][0]["text"]
                task_id_str = text.split("ID: ")[-1]
                task_id = str(uuid.UUID(task_id_str))
            test_results.append(("Add Task", success, {"response": data}))
        except Exception as e:
            test_results.append(("Add Task", False, {"error": str(e)}))

        # Test 4: List Tasks
        try:
            params = {"name": "list_tasks", "arguments": {"user_id": USER_ID}}
            request = create_request("tools/call", params)
            response = client.post(BASE_URL, json=request, headers=headers)
            response.raise_for_status()
            data = response.json()
            success = "result" in data and task_title in data["result"]["content"][0]["text"]
            test_results.append(("List Tasks", success, {"response": data}))
        except Exception as e:
            test_results.append(("List Tasks", False, {"error": str(e)}))

        # Test 5: Update Task
        if task_id:
            try:
                params = {"name": "update_task", "arguments": {"user_id": USER_ID, "task_id": task_id, "title": "Updated Task E2E"}}
                request = create_request("tools/call", params)
                response = client.post(BASE_URL, json=request, headers=headers)
                response.raise_for_status()
                data = response.json()
                success = "result" in data and "updated" in data["result"]["content"][0]["text"]
                test_results.append(("Update Task", success, {"response": data}))
            except Exception as e:
                test_results.append(("Update Task", False, {"error": str(e)}))

        # Test 6: Complete Task
        if task_id:
            try:
                params = {"name": "complete_task", "arguments": {"user_id": USER_ID, "task_id": task_id}}
                request = create_request("tools/call", params)
                response = client.post(BASE_URL, json=request, headers=headers)
                response.raise_for_status()
                data = response.json()
                success = "result" in data and "completed" in data["result"]["content"][0]["text"]
                test_results.append(("Complete Task", success, {"response": data}))
            except Exception as e:
                test_results.append(("Complete Task", False, {"error": str(e)}))

        # Test 7: Delete Task
        if task_id:
            try:
                params = {"name": "delete_task", "arguments": {"user_id": USER_ID, "task_id": task_id}}
                request = create_request("tools/call", params)
                response = client.post(BASE_URL, json=request, headers=headers)
                response.raise_for_status()
                data = response.json()
                success = "result" in data and "deleted" in data["result"]["content"][0]["text"]
                test_results.append(("Delete Task", success, {"response": data}))
            except Exception as e:
                test_results.append(("Delete Task", False, {"error": str(e)}))

    # Print results
    for test_name, success, details in test_results:
        response = details.get("response")
        error = details.get("error")
        print_test_result(test_name, success, response, error)

    # Create report
    with open("test_report.md", "w") as f:
        f.write("# MCP Server Test Report\n\n")
        for test_name, success, details in test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            f.write(f"## {test_name}\n")
            f.write(f"**Status:** {status}\n\n")
            if not success:
                error = details.get("error", "Unknown error")
                f.write(f"**Error:**\n```\n{error}\n```\n\n")
                if "429" in str(error):
                    f.write("**Solution:** The server is being rate-limited by the LLM API. This can be mitigated by optimizing the agent to make fewer API calls and to request shorter responses.\n\n")
                elif "500" in str(error):
                    f.write("**Solution:** The server encountered an internal error. Check the server logs for more details.\n\n")
                else:
                    f.write("**Solution:** Check the test implementation and the server logs for more details.\n\n")

if __name__ == "__main__":
    run_tests()
