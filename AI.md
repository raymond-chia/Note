## Language

- https://www.youtube.com/watch?v=rURRYI66E54&t=240s
  - 最重要的是記得過去產生的文字 (連貫性)
  - 如果單純用機率, 對記憶體的消耗很大
- 先蒐集人類對文章的評價
  - 訓練能判斷文章好壞的 AI
  - 再訓練能產生文章的 AI
  - 不像 gan 同時訓練？
  - loop
- 訓練的是人類喜歡的答案, 不一定是正確的答案
- [限制 AI 用字, 以便偵測](https://www.youtube.com/watch?v=XZJc1p6RE78)
  - 降低某些用字的機率
    - 根據之前用字, 決定下一個要抑制哪些字的機率
    - 如果沒有其他適合的字, 還是可能用被抑制的字
  - Google synthid
    - 用於文字、圖片 (影片)、聲音
- https://beta.character.ai
- Distilling Step-by-Step https://www.ithome.com.tw/news/158902
  - 小型專用模型有兩種訓練方式, 分別是微調 ( Fine-tuning ) 和蒸餾 ( Distillation )
    - 微調使用人工註釋資料, 更新預先訓練的 BERT 或 T5 等規模較小的模型
    - 蒸餾的概念則是將一個大型模型, 或稱為教師模型的知識, 轉移至一個比較小的學生模型
      - 運用大型語言模型所生成的標籤, 訓練相同但規模較小的模型
      - 雖然蒸餾法可以讓學生模型的規模和複雜性都遠低於教師模型, 效能卻可以接近或是超越教師模型
  - 要達到良好的效能, 微調法需要人工生成標籤. 這個過程既昂貴又繁瑣
  - 蒸餾法則需要大量未標記的資料, 且收集資料本身就並非一件簡單的事
  - 逐步蒸餾法能夠讓研究人員以比標準微調或是蒸餾法少得多的訓練資料, 訓練一個更小且專用於特定任務的模型, 而且效能還可能可以優於 Few-Shot Prompted LLM
  - Few-Shot Prompted LLM: 大型語言模型使用少量的樣本, 並透過提示來完成任務的方法, 像是要求語言模型完成翻譯任務. 研究人員便可以提供少量的英翻中樣本, 再給予新的提示問題, 期望模型能夠依據範例正確翻譯新問題
  - 當大型語言模型被問到某些問題時, 能夠透過推理並給出最終答案. 這些中間的推理包含了可以完成任務需要的重要知識. 但是小型模型需要大量資料才能學到這些知識. 因此逐步蒸餾的核心想法, 便是從大型語言模型中擷取有用的自然語言解釋, 也就是中間的推理步驟, 然後使用這些解釋更有效地訓練小型模型
  - 因此逐步蒸餾的步驟
    1. 從大型語言模型中擷取解釋. 研究人員會提供少數範例. 這些範例包含問題, 中間的解釋和答案, 引導大型語言模型對新的問題產生相對應的解釋
    2. 利用第一階段取得的解釋訓練小型模型. 小型模型學習由大型語言模型生成的中間推理步驟, 便能夠更好地預測答案

#### Rank

- 使用量: https://openrouter.ai/rankings?view=month
- ai pk: https://www.youtube.com/watch?v=Ur8MbOj17Gs

#### [提示詞](https://tenten.co/learning/co-star-tidd-ec-prompt-framework)

- roles
  - https://github.com/f/awesome-chatgpt-prompts
  - https://github.com/cognitivecomputations/dolphin-system-messages/tree/main
- CO-STAR

| 縮寫 | 英文      | 中文     | 解釋                                                     |
| ---- | --------- | -------- | -------------------------------------------------------- |
| C    | Context   | 背景     | 為互動設置舞台，提供背景信息或請求所處的情境             |
| O    | Objective | 目標     | 定義提示旨在達成的內容，具體說明語言模型的目標或期望輸出 |
| S    | Style     | 風格     | 指定所需的寫作或回應風格，指導內容應如何呈現或表達       |
| T    | Tone      | 語調     | 表示回應的情感特徵或態度，塑造信息的情感傳達方式         |
| A    | Audience  | 觀眾     | 定義內容的目標觀眾或讀者，影響回應的語言、複雜性和方法   |
| R    | Response  | 回應格式 | 描述回應應該如何結構，決定內容的組織和呈現方式           |

- TIDD-EC

| 縮寫 | 中文     | 解釋                                                                                                                |
| ---- | -------- | ------------------------------------------------------------------------------------------------------------------- |
| T    | 任務類型 | 當前任務的類型，清楚地指示出 LLM 預期執行的活動類型                                                                 |
| I    | 指示     | 概述了 LLM 應遵循的具體步驟或指導方針，以完成任務。這個組件對於確保模型的輸出與用戶的期望緊密對齊至關重要           |
| D    | 做       | 指定 LLM 應該採取的行動，以成功完成提示。這包括使用某些語言、結構或應該包含在回應中的信息                           |
| D    | 不要     | 突出顯示 LLM 在回應中應避免的行動或元素。這對於防止常見錯誤或誤解至關重要，因為這些錯誤可能導致不準確或不相關的輸出 |
| E    | 範例     | 提供期望結果或回應的具體範例。這個組件對於指導 LLM 朝向預期的格式、風格或內容的回應是無價的                         |
| C    | 用戶內容 | 用戶提供的數據，LLM 應在其回應中使用或引用                                                                          |

#### Provider/Model

##### AWS Bedrock

> You don't have access to the model with the specified model ID.

- 申請使用權限: https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess
  - 申請的時候要注意地區  
    https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html
    - 基本上是 us-east-1
- 確認 boto3.client 的 region_name
- model id list
  - https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html
  - 如果在 modelaccess 顯示 Cross-region inference, 則要看 Inference profile ID: https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html

##### Google

###### Gemini

- key: https://aistudio.google.com/app/apikey
- model list
  - https://ai.google.dev/gemini-api/docs/models/gemini
  - https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models
- GeminiVoyager: 優化 Gemini 網頁版的 UX

###### Vertex

- 1. 到 Model Garden 搜尋 model
  1. enable model
  1. 在 pick one region 處取得可用的位置
  1. 給予 service account 權限: aiplatform.endpoints.predict. 例如 role `Vertex AI Platform Express User`

##### Claude

- 擅長寫程式

##### GPT

- [可 few shot](https://www.youtube.com/watch?v=_8yVOC4ciXc)
  - 數量越多效果越好
  - 模型越大, few shot 效果越好

##### Copilot

- Bing 的 copilot 不適合產生程式碼 [2023/2](https://www.youtube.com/watch?v=8BBzaiAbxp4)
  - 只適合搜尋
  - 改用 OpenAI 或 VS Code

##### Perplexity

- 免費
- 使用其他模型搜尋

##### Deepseek

- https://www.youtube.com/watch?v=gY4Z-9QlZ64
  - 一個大模型裡面有諸多小模型 (專家)
    - 每次呼叫只會使用專家模型, 降低消耗
    - 訓練的時候使用 distil 降低消耗
  - chain of thought
    - 不用通常的訓練方式: 問題, chain of thought, 答案
    - 只提供: 問題, 答案, 要 AI 自己訓練出 chain of thought
      - AI 學會自問自答

##### Grok

#### Vector / Embedding

- https://www.youtube.com/watch?v=gQddtTdmG_8
  - 如果直接訓練 LLM 學習語言, 會花很多功在學習單字
  - 改成讓 LLM 學習 embedded 之後的文字
    - vector 因為是數字, 比較好量化評分 LLM 回應, 比較好訓練
  - 訓練如何預測下個字的時候, 同時會訓練 vector 轉換器 ??
  - 可以加減 vector, 得到另外一個字: `king - man + woman = queen`
- 用 cosine similarity 比較 ??

##### Clip

- 調整 vectoring, 將 image 與字串對應到接近的 vector
  - https://www.youtube.com/watch?v=KcSXcpluDe4
  - 一次練一個 batch. 逼近相符圖文的 vectors, 遠離不符圖文的 vectors

##### DB

- S3 vector 比其他 AWS vector db 產品便宜

#### Retrieval Augmented Generation (RAG)

- 生成回應前參考指定知識庫
- 流程
  - https://python.langchain.com/v0.2/docs/how_to/chatbots_retrieval
  - https://python.langchain.com/v0.2/docs/concepts/#retrieval
- 事前先 Indexing, 要用的時候 Retrieval
  - Retrievers 可以是 Vector stores, 也可以是 search service (例如 Wikipedia search)
  - citation
- vector store
  - 要選適當的 dimension
  - 針對 keyword 表現可能不如普通搜尋 ??
    - dense embeddings
    - [sparse embeddings 適合 keyword searches](https://cloud.google.com/vertex-ai/docs/vector-search/overview#terminology)
    - Recall: The percentage of nearest neighbors returned by the index that are actually true nearest neighbors. For example, if a nearest neighbor query for 20 nearest neighbors returned 19 of the ground truth nearest neighbors, the recall is 19/20x100 = 95%.

##### GraphRAG

- 在 vector store 建立 embeddings 之間的關聯
- local search: 第一層關聯
- global search: 高層的關聯
  - 理解抽象
  - 容易幻覺
- drift search: local + global

#### Injection

##### Indirect prompt injection

- 把 injection 埋在 llm 會用來搜尋的資料庫

#### IDE

##### Cline

###### Step 1: Locate the Extension Folder

####### Windows

1. Open File Explorer and go to:

```
%USERPROFILE%\.vscode\extensions\
```

2. Look for a folder named similar to:

```
github.copilot-chat-<version>
```

####### macOS/Linux

1. Open your file manager or Terminal and navigate to:

```
~/.vscode/extensions/
```

2. Find the folder named like:

```
github.copilot-chat-<version>
```

###### Step 2: Open the extension.js File

1. Inside the github.copilot-chat-<version> folder, open the dist directory.
2. Locate the file named extension.js.
3. Open this file with your preferred text editor (e.g., VS Code).

###### Step 3: Find the Header Code

Search for the text: "x-onbehalf-extension-id"

###### Step 4: Remove or Comment Out the Code

###### Step 5: Restart Visual Studio Code

#### 整合

##### Dify

- 提供工作流

##### LangChain

- https://python.langchain.com/v0.2/docs/tutorials
- framework for developing applications powered by large language models
- LCEL: https://myapollo.com.tw/blog/langchain-expression-language
  - dict 會被轉成 RunnableParallel
  - function 會被轉成 RunnableLambda
    - 如果 function 會根據條件回不同的 Runnable, 就等於 RunnableBranch
  - `RunnablePassthrough.assign(新欄位名稱=目標LCEL)`
  - 參數 `LCEL.input_schema.schema()`
  - 回傳值 `LCEL.output_schema.schema()`
  - 圖 `LCEL.get_graph().print_ascii()`
- chat focused playground: https://python.langchain.com/v0.2/docs/langserve/#chat-playground
- 動態調整設定: https://python.langchain.com/v0.2/docs/how_to/configure
- 輪流用不同的 api key: https://clemenssiebler.com/posts/azure_openai_load_balancing_langchain_with_fallbacks

###### RAG

- 概念: https://python.langchain.com/docs/concepts/rag
- 歷史記錄: https://python.langchain.com/v0.1/docs/use_cases/chatbots/retrieval/#query-transformation
- 不使用 built-in function: https://python.langchain.com/v0.2/docs/tutorials/rag/#customizing-the-prompt

###### Image

- https://python.langchain.com/v0.2/docs/how_to/multimodal_prompts  
  在 chain 塞入以下可以讓 model 看到圖片

```python
def insert_image(x):
    import requests

    image = base64.b64encode(
        requests.get(
            "https://imageio.forbes.com/specials-images/imageserve/675ce0f75b64a53f072010c6/Ciri/960x0.jpg?format=jpg&width=960"
        ).content
    ).decode("utf-8")
    return [
        HumanMessage(
            content=[
                {"type": "text", "text": x["messages"][0].content},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                },
            ]
        )
    ]
    # 或下面
    return x["messages"] + [
        HumanMessage(
            content=[
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                },
            ]
        )
    ]
```

###### debug

- /docs 可以看 openapi
- ```py
  import langchain
  langchain.debug = True
  ```
- 在 fastapi 註冊 middleware 來印 request https://github.com/fastapi/fastapi/issues/3361

##### Gateway

- OpenRouter
- LiteLLM
  - 內建的各個供應商價目表: https://github.com/BerriAI/litellm/blob/v1.72.2-stable/model_prices_and_context_window.json

##### MCP

- 給 AI 的 API
- 範例: https://github.com/modelcontextprotocol/servers
- https://github.com/modelcontextprotocol/python-sdk 或 https://github.com/jlowin/fastmcp
  - https://github.com/jlowin/fastmcp 文件比較好
- 範例 server
  ```python
  from fastmcp import FastMCP
  from fastapi import FastAPI
  mcp = FastMCP("LLM-MCP")
  @mcp.tool
  def echo_tool(message: str) -> str:
      return f"something: {message}"
  mcp_app = mcp.http_app(path="/")
  app = FastAPI(lifespan=mcp_app.lifespan)
  app.mount("/", mcp_app)
  ```
  搭配 `roo code` client
  ```json
  {
    "mcpServers": {
      "doc": {
        "type": "streamable-http",
        "url": "http://localhost:8000",
        "alwaysAllow": ["echo_tool"],
        "disabled": false
      }
    }
  }
  ```
- claude code 不支援 nested object parameters 2025-10-02
  - 如果只有一個欄位 query, `query: str = Body(..., embed=True)` 可以避免 fastapi 當作 query string, 又能滿足 claude code mcp

###### Context7

- 提供 vibe coding 查詢程式碼 api

##### DeepWiki

- 預先分析程式碼

#### 雜項

- https://chatgpt.com/gpts
- [annotation reply](https://docs.dify.ai/guides/biao-zhu/annotation-reply): 人工修改某種問題的回答
- [NotebookLM](https://notebooklm.google.com): 整理上傳的檔案, 並提供問答 (rag ??)
- - temperature: 調整整個機率分佈的形狀. 0.0-2.0
    - 0.0 代表完全確定性（幾乎只會選擇機率最高的詞），
    - 1.0 為標準隨機性，
    - `>` 1.0 會讓生成內容更隨機、更有創意，但也可能更不穩定。
  - top_p: 根據累積機率直接截斷候選詞集合. 0.0-1.0
    - 1.0 代表不做截斷（等同於不啟用 top_p），
    - 越接近 0.0，生成內容越保守。

## GAN

- 一組產生, 一組判斷. 兩組對立訓練
- https://www.gwern.net/Faces

## Text to Image

- 看 prompt 對圖片的影響: https://huggingface.co/spaces/neggles/wd-tagger-heatmap
- [Dall-e2 vs Disco Diffustion](https://medium.com/@nin_artificial/dall-e-2-vs-disco-diffusion-c6de6bfbacf9)
- Stable Diffusion
  - https://github.com/invoke-ai/InvokeAI
  - https://github.com/AUTOMATIC1111/stable-diffusion-webui
    - api 文件在架設 stable diffusion server 的 `網址/docs`
    - command line arguments 加上 `--listen` 可以讓外界連
  - https://github.com/comfyanonymous/ComfyUI
    - https://github.com/ltdrdata/ComfyUI-Manager
    - 用於安裝 comfy ui 相關功能
    - 也是用 --listen 讓外界連
    - docker 版本 ??
      - https://replicate.com/fofr/any-comfyui-workflow
      - runpod 版本
  - https://ai.dawnmark.cn/
  - 直接用預設模型 + lora
- Stable Zero123
- Flux
- multi view diffusion
  - https://mv-dream.github.io
  - 3d
- Midjourney
  - [prompts](https://www.techbang.com/posts/105911-free-ultimate-chatgpt-tips-midjourney-treasure-god-map-1200?fbclid=IwAR0yMPvigCn8-llVd4Wrw-KSAJZaVuloEBnhkLr6YRrc_jaAKawDW0-B7r4_aem_th_AeOP0Rq4RuClf3tCCW6xeXcv1tHWUL_s0MRAAX48pVPG6Qku5f4J-9yQENyr_2PZPf0)
- visual chatgpt
  - https://github.com/microsoft/visual-chatgpt
- GFPGAN: face restoration
- ai models 集散地
  - https://civitai.com/

#### Blinkshot

- https://github.com/Nutlope/blinkshot
- 可以即時產生圖片

#### Stable Diffusion

- https://www.youtube.com/watch?v=1CIpzeNxIhU
  - 每步驟加上一點雜訊, 多個步驟後整張圖都是雜訊
  - 訓練 denoise 的能力
    - 給任意程度加雜訊的圖 (經過 x 步驟), 判斷加了哪些雜訊 (知道 x 或許比較好訓練？)
  - 從完全雜訊 denoise 之後, 圖片多半還是糊的
    - 再加上雜訊 (達到步驟 10 變成步驟 9)
    - 重複進行
  - classifier free guidance
    - 一次產生兩張圖, 一張有文字, 一張沒有文字
    - 判斷差異, 強化差異
- prompts:
  - 0.1 ~ 100
  - `(prompt)` 代表 x 1.1
  - `[prompt]` 代表 / 1.1
  - `prompt: 1.1`
  - `AND` 可以把 prompt 混到同一個目標上？
  - https://docs.google.com/spreadsheets/d/14Gg1kIGWdZGXyCC8AgYVT0lqI6IivLzZOdIT3QMWwVI/edit#gid=1760100829
  - https://docs.qq.com/doc/DWFdSTHJtQWRzYk9k
  - prompt demo: https://zele.st/NovelAI/
  - image to prompt: https://replicate.com/methexis-inc/img2prompt
  - 手姿勢: https://note.com/vivid_walrus6061/n/n161a3a02ece4
- sampler
  - ddim 很快定型
  - euler a 每一步變動頗大
  - `Euler/Euler_a` 快, `DPM++_2M` 中等, `DPM++SDE` 慢
- prompt matrix
  - 用 `|` 區隔. 比如 `forest, | style a | style b |`
- x/y plot
  - 可以排列 step & sampler 組合 (或其他組合)
  - x & y 內部各自用 `,` 分隔
- tilling
  - 可以產生連續的圖？
- inpaint
  - 截圖, inpaint, 合併回原本的圖片. 這樣效果或許比較好？
- 總共有 8 層, 最外面 2 層大, 中間 6 層小. 中間某幾層影響形狀, 某幾層影響風格/顏色

##### ControlNet

- 手動調整 openpose (不要設定 preprocessor)
  - https://hub.vroid.com/en/characters/6524757472248303508/models/3316848696231372685
  - https://github.com/fkunn1326/openpose-editor
- 可以用 control-net 構圖, img2img 決定顏色
  - https://www.youtube.com/watch?v=kf5uwP2mQAc
- seg 用的顏色要參考 ade20k
- 紙娃娃流程 https://vocus.cc/article/649803f4fd897800019abf84?fbclid=IwAR3Asd9exIJZ6qpTMoE-eQIKsW7jrHoChU3KBg2ucp8VLrunLnRLbWPRwQM

##### 其他

- models: https://rentry.org/sdmodels
  - [調整](https://www.youtube.com/watch?v=dVjMiJsuR5o)
    - Dreambooth: 直接訓練新 model. GB
      - 盡量只有一個 dreambooth
    - Textual Inversion: 訓練過程是去調整文字提詞對模型產圖的精準度. KB
    - LoRA: 在原有的大模型裡加入新的中間層, 訓練過程只調整那些新的中間層權重. 幾百 MB
    - Hypernetworks: 跟 LoRA 很像, 但是間接透過一個 Hypernetwork 模型去對原本的模型做改變. 幾百 MB
  - https://civitai.com/models/260267/animagine-xl-v3
- latent couple: 不同區塊可以用不同的 prompt
- cutoff: 避免元素互相影響 https://mnya.tw/cc/word/1973.html
- 修手: https://github.com/jexom/sd-webui-depth-lib
- 調整 openpose https://www.youtube.com/watch?v=n1LOPci7ICk
- Roop: 換臉
- GLIGen: 分區指定 prompt
  - https://github.com/mut-ex/gligen-gui
- Inpaint Anything: 協助產生 inpaint 的 mask
- 透明背景: https://github.com/layerdiffusion/sd-forge-layerdiffusion
- 兩張圖產生中間動畫 https://x.com/tds_95514874/status/1693603992092524662?s=46&t=y26bJt9O7xPNkMWJx-w1og
- LCM: 加速產圖
- Create Consistent, Editable AI Characters & Backgrounds (ComfyUI): https://www.youtube.com/watch?v=849xBkgpF3E
- 資料量太大, 難以讓 AI 知道前面有什麼圖片 -> 使用 encoder & decoder network 來壓縮圖片
  - 類似 embedding
  - [latent diffusion](https://www.youtube.com/watch?v=hJHfZKYUKMw)
- source
  - https://www.youtube.com/@Aitrepreneur
  - https://mnya.tw/cc/word/category/ai-drawing
  - https://www.kadokado.com.tw/book/22947

##### 範例

- 產生 3D 角色: https://talesofsyn.com/posts/creating-3d-character-models
- 產生 isometric 場地: https://talesofsyn.com/posts/creating-isometric-rpg-game-backgrounds
- 紙娃娃: https://vocus.cc/article/649803f4fd897800019abf84?fbclid=IwAR3Asd9exIJZ6qpTMoE-eQIKsW7jrHoChU3KBg2ucp8VLrunLnRLbWPRwQM
- 點光源: https://x.com/toyxyz3/status/1796226845517783264?s=46&t=y26bJt9O7xPNkMWJx-w1og
- 用 pseudo code 產生連貫的圖片
  - https://www.youtube.com/watch?v=3rb-54Q5fig
  - 雖然用於整理文字, 但是可以參考 https://baoyu.io/blog/prompt-engineering/advanced-prompting-using-pseudocode-to-control-llm-output#google_vignette
- 出圖 -> inpaint 要動的區域產生 A B 兩張圖 -> tooncrafter 製作短動畫用 AB / BA 組合 -> 頭尾相接後就成為 loop 動畫
- AI 演化: https://www.ptt.cc/bbs/C_Chat/M.1730732828.A.70C.html

#### 自回歸 ??

- 在 prompt 短的情況下, 比 stable diffusion 更嚴格遵守 prompt, 不容易擅自創造不在 prompt 裡的東西

## Text to 3D

- Tripo3D
  - https://x.com/toyxyz3/status/1806932777386098715?s=46&t=y26bJt9O7xPNkMWJx-w1og
  - 面數較下面低
- Rodin
- MetaHuman
  - 面數高
- meshy
  - 不能用扁平風格圖片
- 要求 claude 控制 blender: https://x.com/oran_ge/status/1899599891564999051?s=46&t=fj_x062sdFD-mXCkllQ04w
- nvidia: https://youtu.be/kB3J9EivZN0?si=L098tSqHPlDPdFnX

## Animation

- Unity Muse
  - 可以產生動作

## Image to Image

- ideogram
- Trellis

## Music

- https://github.com/GrandaddyShmax/audiocraft_plus ?
- https://www.stableaudio.com/ ?
- https://www.udio.com/blog/introducing-v1-5 ?
- Suno AI

## Platform

### AWS

- 花費警報: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html
- 用量: cloudwatch

### Azure

- 有多種 azure studio
  - azure ai studio
  - azure openai studio

#### 建立

- Resource Group: https://portal.azure.com/#create/Microsoft.ResourceGroup
- AI Foundry
  - OpenAI 的 models 選擇 Azure OpenAI
  - 其他選擇 Hubs + Project
  - https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/AIHubs
  - ai 能部署的區域: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
- 管理 key: OpenAI service > Resource Management > Keys and Endpoint

#### RAG

- rag 範例 https://github.com/langchain-ai/langchain/blob/d64bd32b20e359c1c4524a839b343302ed5a6f04/templates/rag-azure-search/rag_azure_search/chain.py
  - 搭配[RAG 的範例](<#Retrieval-Augmented-Generation-(RAG)>)
  - https://learn.microsoft.com/zh-tw/azure/ai-services/openai/concepts/use-your-data ??
  - https://learn.microsoft.com/zh-tw/azure/ai-services/openai/use-your-data-quickstart ??
  - web app 是設計面向一般使用者 ??
    - https://learn.microsoft.com/en-us/azure/ai-studio/tutorials/deploy-chat-web-app ??

#### 花費

- host fine tuned model 會按時收費
- 花費警報: Resource group (type) -> Cost Management -> Budgets
- 用量: Azure OpenAI (type) -> Monitoring -> Metrics

### Google

#### Agent Builder

- 如果要用來當作 vector store
  - 可能會花到 2 秒多 @ 2025/9
  - langchain VertexAISearchRetriever 在用 beta @ 2024/11
  - [範例](https://github.com/GoogleCloudPlatform/generative-ai/blob/d2d888ba3767af893c4fadc1446c32a1c3a59826/search/retrieval-augmented-generation/examples/question_answering.ipynb)

### Nvidia

- https://docs.api.nvidia.com/nim/docs/product#how-do-i-get-additional-api-credits
  - 只能透過網頁呼叫, 沒有提供付費雲端服務

## Video

- Runway 的 Gen-3
  - 範例: https://x.com/Ror_Fly/status/1899473065328656485
    - 先叫 claude 產生 three.js code
    - 播放並錄製
    - 傳送到 runway 產生影片
    - 到 Magnific 修圖
    - 回到 runway 修正影片
- 拖拉圖片 https://generative-dynamics.github.io
- 搭配 stable diffusion ? https://github.com/hotshotco/hotshot-xl
- [用 stable diffusion 訓練的時候, 給一組連續圖, 每次練一組](https://www.youtube.com/watch?v=hJHfZKYUKMw)
  - 訓練時, 每一張圖片的 noise 都要不一樣
  - latent diffusion 還是資料量太大 -> 把空間切小, 但是時間連續 patch (圖片不同地方的連續圖)
- 補幀數 (frame): Flowframes
- Luma AI
  - 參數下 live2d ??
  - e.g. live2d standing motion, hair swaying, 2d, looped
- https://github.com/jbilcke-hf/clapper

## Voice

- voice.ai ??
- ElevenLabs ??
- https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI ??
- https://www.youtube.com/watch?v=9lsSSPnF67Q ??
- 文字轉聲音 + 影片 https://www.heygen.com
- 分離人的聲音 https://vocalremover.org/

## Workflow

- https://github.com/langgenius/dify

## Collection

- https://www.futuretools.io/?tags=generative-art

## Misc

- [PPO](https://en.wikipedia.org/wiki/Proximal_Policy_Optimization), SAC
- Generative Adversarial Imitation Learning (GAIL)
- Long Short Term Memory (LSTM)
- text to image, 影片轉動畫 ?
  - https://domoai.app/
  - https://human3daigc.github.io/Textoon_webpage/
