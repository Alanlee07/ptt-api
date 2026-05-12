import requests
from bs4 import BeautifulSoup
import time

def get_ptt_real_trends(board, pages=3, min_push=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'cookie': 'over18=1'
    }
    
    current_url = f"https://www.ptt.cc/bbs/{board}/index.html"
    results = []
    
    # 定義要排除的關鍵字 (公告、版規等)
    exclude_keywords = ['公告', '協尋', '版規', '置底']

    for i in range(pages):
        print(f">>> 正在掃描第 {i+1} 頁: {current_url}")
        try:
            res = requests.get(current_url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            posts = soup.find_all('div', class_='r-ent')
            
            for post in posts:
                # 1. 處理推文數
                raw_push = post.find('div', class_='nrec').text.strip()
                push_num = 0
                if raw_push:
                    if raw_push == '爆': push_num = 100
                    elif raw_push.startswith('X'): push_num = -10
                    elif raw_push.isdigit(): push_num = int(raw_push)
                
                # 2. 處理標題
                title_element = post.find('div', class_='title').find('a')
                if not title_element: continue
                
                title = title_element.text
                link = "https://www.ptt.cc" + title_element['href']
                
                # 3. 排除邏輯：如果標題包含排除關鍵字，就跳過
                # 使用 any() 函數快速檢查標題是否包含任一排除字眼
                if any(k in title for k in exclude_keywords):
                    continue
                
                # 4. 符合推文門檻才加入
                if push_num >= min_push:
                    results.append({
                        'page': i + 1,
                        'push': raw_push if raw_push else '0',
                        'title': title,
                        'link': link
                    })

            # 找上一頁
            prev_btn = soup.find('a', string='‹ 上頁')
            if prev_btn:
                current_url = "https://www.ptt.cc" + prev_btn['href']
            else:
                break
                
            time.sleep(0.5)

        except Exception as e:
            print(f"錯誤: {e}")
            break

    return results

# 執行
all_posts = get_ptt_real_trends("Gossiping", pages=3, min_push=10)

if all_posts:
    print(f"\n✅ 成功抓取！已排除公告，共找到 {len(all_posts)} 篇真實風向文章：")
    print("-" * 70)
    for p in all_posts:
        # 使用 f-string 格式化輸出，讓推文數對齊
        print(f"[{p['push']:^3}] {p['title']}")
        #print(f"      {p['link']}")
else:
    print("\n❌ 未發現符合條件的文章。")