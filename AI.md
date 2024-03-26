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

#### GPT

- [可 few shot](https://www.youtube.com/watch?v=_8yVOC4ciXc)
  - 數量越多效果越好
  - 模型越大, few shot 效果越好

##### GPT Roles

- https://github.com/f/awesome-chatgpt-prompts

## GAN

- 一組產生, 一組判斷. 兩組對立訓練
- https://www.gwern.net/Faces

## Text to Image

- [Dall-e2 vs Disco Diffustion](https://medium.com/@nin_artificial/dall-e-2-vs-disco-diffusion-c6de6bfbacf9)
- Stable Diffusion
  - https://github.com/invoke-ai/InvokeAI
  - https://github.com/AUTOMATIC1111/stable-diffusion-webui
    - api 文件在架設 stable diffusion server 的 `網址/docs`
    - command line arguments 加上 `--listen` 可以讓外界連
  - https://github.com/DominikDoom/a1111-sd-webui-tagcomplete/blob/main/README_ZH.md
  - https://ai.dawnmark.cn/
- Stable Zero123
- multi view diffusion
  - https://mv-dream.github.io
  - 3d
- tripo
  - 3d
- Midjourney
  - [prompts](https://www.techbang.com/posts/105911-free-ultimate-chatgpt-tips-midjourney-treasure-god-map-1200?fbclid=IwAR0yMPvigCn8-llVd4Wrw-KSAJZaVuloEBnhkLr6YRrc_jaAKawDW0-B7r4_aem_th_AeOP0Rq4RuClf3tCCW6xeXcv1tHWUL_s0MRAAX48pVPG6Qku5f4J-9yQENyr_2PZPf0)
- visual chatgpt
  - https://github.com/microsoft/visual-chatgpt
- GFPGAN: face restoration
- ai models 集散地
  - https://civitai.com/

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
- sampler
  - euler a 每一步變動頗大
  - ddim 很快定型
- prompt matrix
  - 用 `|` 區隔. 比如 `forest, | style a | style b |`
- x/y plot
  - 可以排列 step & sampler 組合 (或其他組合)
  - x & y 內部各自用 `,` 分隔
- tilling
  - 可以產生連續的圖？
- inpaint
  - 截圖, inpaint, 合併回原本的圖片. 這樣效果或許比較好？

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
- source
  - https://www.youtube.com/@Aitrepreneur
  - https://mnya.tw/cc/word/category/ai-drawing
  - https://www.kadokado.com.tw/book/22947

##### 範例

- 產生 3D 角色: https://talesofsyn.com/posts/creating-3d-character-models
- 產生 isometric 場地: https://talesofsyn.com/posts/creating-isometric-rpg-game-backgrounds
- 紙娃娃: https://vocus.cc/article/649803f4fd897800019abf84?fbclid=IwAR3Asd9exIJZ6qpTMoE-eQIKsW7jrHoChU3KBg2ucp8VLrunLnRLbWPRwQM

## Music

- https://github.com/GrandaddyShmax/audiocraft_plus ?
- https://www.stableaudio.com/ ?

## Video

- 拖拉圖片 https://generative-dynamics.github.io
- 搭配 stable diffusion ? https://github.com/hotshotco/hotshot-xl
- 補幀數 (frame): Flowframes

## Voice

- voice.ai ?
- https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI ?
- https://www.youtube.com/watch?v=9lsSSPnF67Q ?
- 文字轉聲音 + 影片 https://www.heygen.com
- 分離人的聲音 https://vocalremover.org/

## Collection

- https://www.futuretools.io/?tags=generative-art

## Misc

- [PPO](https://en.wikipedia.org/wiki/Proximal_Policy_Optimization), SAC
- Generative Adversarial Imitation Learning (GAIL)
- Long Short Term Memory (LSTM)
- text to image, 影片轉動畫 ? https://domoai.app/
