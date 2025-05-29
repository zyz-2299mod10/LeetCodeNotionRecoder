from datetime import datetime, timezone
from crawler import extract_slug, get_leetcode_info_via_api
import yaml
import os

def get_test_data():
    title = "Test Title"
    description = "This is a test"
    published_date = datetime.now().astimezone(timezone.utc).date().isoformat()

    test_data = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "Tags": {
            "multi_select": [
                {"name": "Medium"},
                {"name": "Array"},
                {"name": "DP"},
                {"name": "Matrix"},
            ]
        },
        "Time": {
            "date": {
                "start": published_date
            }
        },
        "備註": {
            "rich_text": [
                {
                    "text": {
                        "content": description
                    }
                }
            ]
        },
        "網址": {
            "url": "https://leetcode.com/problems/minimum-path-sum/description/"
        }
    }

    context = [
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Code"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "In-place Dynamic Programming, 記得留意邊界"}
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "language": "c++",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": """class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        for(int i = m - 1; i >= 0; i--) {
            for(int j = n - 1; j >= 0; j--) {
                if (i == m - 1 && j == n - 1) continue;
                else if (i == m - 1) grid[i][j] += grid[i][j + 1];
                else if (j == n - 1) grid[i][j] += grid[i + 1][j];
                else grid[i][j] += min(grid[i + 1][j], grid[i][j + 1]);
            }
        }
        return grid[0][0];
    }
};"""
                        }
                    }
                ]
            }
        }
    ]

    return test_data, context

def get_LeetCode_data(url:str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.yml")

    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)    
    topic = config["Topic"]

    slug = extract_slug(url)
    info = get_leetcode_info_via_api(slug)

    title = f"{info['id']}. {info['title']}"
    difficulty = info["difficulty"]
    published_date = datetime.now().astimezone(timezone.utc).date().isoformat()
    
    Tags = {
        "multi_select":
            [
                {"name": difficulty}
            ]
    }

    out_of_topic = {}
    for t in info["topics"]: 
        if t not in topic:
            out_of_topic[str(t)] = str(t)
            tag = t
            print(f"New topic added \"{t}\"")
        else: 
            tag = topic[t]
        select = {"name": tag}
        Tags["multi_select"].append(select)
    
    if out_of_topic: # this Problem have new topic
        print("Update config topic.... ", end="")
        config["Topic"].update(out_of_topic)
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        print("Done")

    LeetCode_data = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "Time": {
            "date": {
                "start": published_date
            }
        },
        "網址": {
            "url": url
        }
    }
    LeetCode_data["Tags"] = Tags

    context = [
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Code"}}]
            }
        }
    ]

    return LeetCode_data, context