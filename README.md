# LeetCodeNotionRecoder

# Before start
1. Get your notion key: https://developers.notion.com/docs/create-a-notion-integration
2. Create a Notion database template: https://sable-juice-2a9.notion.site/LeetCode-431ad60000374f368b1003812a780d06 <br>
   (credit to https://vocus.cc/article/63b195e6fd89780001da4619)
3. Get the database id: https://developers.notion.com/reference/retrieve-a-database
4. Fill the `NOTION_KEY` and the `DATABASE_ID` in `config.yml` 
### Check the connection
```
python main.py --debug
```
It will create a page call "Test title" on the current day

# Start
```
python main.py --url LeetCode-Problem-URL
```

* You can set an alias in Linux for easier command usage.
* Alias in **windows** <br>
  (https://learn.microsoft.com/zh-tw/powershell/module/microsoft.powershell.utility/set-alias?view=powershell-7.5) <br>
  (https://blog.poychang.net/make-your-powershell-handy/) <br>
  you can use the following example
  ```
  function lr{
	param($URL)
	python .\path\to\LeetCodeNotionRecoder\main.py --url $URL
   }
  ```
