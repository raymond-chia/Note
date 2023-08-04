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
    - https://colab.research.google.com/github/acheong08/Diffusion-ColabUI/blob/main/Diffusion_WebUI.ipynb#scrollTo=Y4qjIc1XXKWw
    - https://github.com/camenduru/stable-diffusion-webui-colab/tree/v2.0
  - https://github.com/DominikDoom/a1111-sd-webui-tagcomplete/blob/main/README_ZH.md
  - https://ai.dawnmark.cn/
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

##### 其他配件

- models: https://rentry.org/sdmodels
  - [調整](https://www.youtube.com/watch?v=dVjMiJsuR5o)
    - Dreambooth: 直接訓練新 model. GB
      - 盡量只有一個 dreambooth
    - Textual Inversion: 訓練過程是去調整文字提詞對模型產圖的精準度. KB
    - LoRA: 在原有的大模型裡加入新的中間層, 訓練過程只調整那些新的中間層權重. 幾百 MB
    - Hypernetworks: 跟 LoRA 很像, 但是間接透過一個 Hypernetwork 模型去對原本的模型做改變. 幾百 MB
- latent couple: 不同區塊可以用不同的 prompt
- cutoff: 避免元素互相影響 https://mnya.tw/cc/word/1973.html
- 修手: https://github.com/jexom/sd-webui-depth-lib
- posex: 調整 openpose
- Roop: 換臉
- GLIGen: 分區指定 prompt
- Inpaint Anything: 協助產生 inpaint 的 mask
- OneButtonPrompt, Tag Autocomplete: 幫忙產生 prompt
- source
  - https://www.youtube.com/@Aitrepreneur
  - https://mnya.tw/cc/word/category/ai-drawing

##### 範例

- 產生 3D 角色: https://talesofsyn.com/posts/creating-3d-character-models
- 產生 isometric 場地: https://talesofsyn.com/posts/creating-isometric-rpg-game-backgrounds
- 紙娃娃: https://vocus.cc/article/649803f4fd897800019abf84?fbclid=IwAR3Asd9exIJZ6qpTMoE-eQIKsW7jrHoChU3KBg2ucp8VLrunLnRLbWPRwQM

## Voice

- voice.ai
- https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI

## Collection

- https://www.futuretools.io/?tags=generative-art

## Misc

- [PPO](https://en.wikipedia.org/wiki/Proximal_Policy_Optimization), SAC
- Generative Adversarial Imitation Learning (GAIL)
- Long Short Term Memory (LSTM)
