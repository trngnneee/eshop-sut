import os
import urllib.request
import urllib.error
import json
import sys

# Repo information from git remote origin
REPO = "trngnneee/eshop-sut"
API_URL = f"https://api.github.com/repos/{REPO}/issues"

bug_dir = r"tests/bug/dashboard"
bug_files = [f"BUG-FR13-C-0{i}.md" for i in range(1, 6)]

def create_issue(token, title, body):
    req_data = json.dumps({
        "title": title,
        "body": body,
        "labels": ["bug", "FR-13", "dashboard"]
    }).encode("utf-8")
    
    req = urllib.request.Request(
        API_URL,
        data=req_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "Antigravity-Assistant"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            return response.status, json.loads(res_body)
    except urllib.error.HTTPError as e:
        res_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(res_body)
        except Exception:
            return e.code, {"error": res_body}
    except Exception as e:
        return 0, {"error": str(e)}

def main():
    print("=" * 80)
    print("AI GITHUB ISSUES CREATOR FOR FR-13 DASHBOARD BUGS")
    print("=" * 80)
    
    # Get token from env or user input
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        token = input("Nhập vào GitHub Personal Access Token (PAT) của bạn: ").strip()
        if not token:
            print("Lỗi: GitHub Token không được để trống.")
            sys.exit(1)
            
    created_issues = []
    
    for filename in bug_files:
        filepath = os.path.join(bug_dir, filename)
        if not os.path.exists(filepath):
            print(f"Bỏ qua: Không tìm thấy file {filename}")
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse title from first line
        lines = content.split("\n")
        title = lines[0].replace("#", "").strip() if lines else filename
        
        print(f"Đang đẩy lỗi: {title}...")
        status, res = create_issue(token, title, content)
        
        if status == 201:
            issue_url = res.get("html_url")
            issue_number = res.get("number")
            print(f"-> Đẩy thành công! Issue #{issue_number}: {issue_url}")
            created_issues.append((filename, issue_number, issue_url))
        else:
            print(f"-> Đẩy thất bại (HTTP {status}): {res.get('message') or res.get('error')}")
            
    if created_issues:
        print("\nTỔNG HỢP ISSUES ĐÃ TẠO THÀNH CÔNG:")
        print("-" * 80)
        for fn, num, url in created_issues:
            print(f"- {fn} -> Issue #{num} ({url})")
            
        print("\nBạn có thể copy các link Issue trên để cập nhật vào `main-report.md` và `traceability-matrix.md`.")
    else:
        print("\nKhông có issue nào được tạo thành công.")

if __name__ == "__main__":
    main()
