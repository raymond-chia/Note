## Language

- https://www.youtube.com/watch?v=rURRYI66E54
  - 最重要的是記得過去產生的文字（連貫性）
  - 如果單純用機率, 對記憶體的消耗很大
    - https://www.youtube.com/watch?v=rURRYI66E54&t=240s
- https://beta.character.ai

#### GPT

- [可 few shot](https://www.youtube.com/watch?v=_8yVOC4ciXc)
  - 數量越多效果越好
  - 模型越大, few shot 效果越好

## GAN

- 一組產生, 一組判斷. 兩組對立訓練
- https://www.gwern.net/Faces

## Text to Image

- [Dall-e2 vs Disco Diffustion](https://medium.com/@nin_artificial/dall-e-2-vs-disco-diffusion-c6de6bfbacf9)
- Stable Diffusion
  - https://github.com/invoke-ai/InvokeAI
  - https://github.com/AUTOMATIC1111/stable-diffusion-webui
    - https://colab.research.google.com/github/acheong08/Diffusion-ColabUI/blob/main/Diffusion_WebUI.ipynb#scrollTo=Y4qjIc1XXKWw
  - https://github.com/DominikDoom/a1111-sd-webui-tagcomplete/blob/main/README_ZH.md
  - https://ai.dawnmark.cn/
- Midjourney
- GFPGAN: face restoration
- ai models 集散地
  - https://civitai.com/

#### Stable Diffusion

- https://www.youtube.com/watch?v=1CIpzeNxIhU
  - 每步驟加上一點雜訊, 多個步驟後整張圖都是雜訊
  - 訓練 denoise 的能力
    - 給任意程度加雜訊的圖（經過 x 步驟）, 判斷加了哪些雜訊（知道 x 或許比較好訓練？）
  - 從完全雜訊 denoise 之後, 圖片多半還是糊的
    - 再加上雜訊（達到步驟 10 變成步驟 9）
    - 重複進行
  - classifier free guidance
    - 一次產生兩張圖, 一張有文字, 一張沒有文字
    - 判斷差異, 強化差異
- models: https://rentry.org/sdmodels
  - DreamBooth
    - 修改 model
    - 適用於主題, 而非風格？
  - Textual Inversion
    - 訓練後可以掛載（像是 mod）
    - 可用於主題 & 風格？
    - https://www.youtube.com/watch?v=4E459tlwquU
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
  - 可以排列 step & sampler 組合（或其他組合）
  - x & y 內部各自用 `,` 分隔
- tilling
  - 可以產生連續的圖？
- inpaint
  - 截圖, inpaint, 合併回原本的圖片. 這樣效果或許比較好？

## Voice
- voice.ai

## Misc

- [PPO](https://en.wikipedia.org/wiki/Proximal_Policy_Optimization), SAC
- Generative Adversarial Imitation Learning (GAIL)
- Long Short Term Memory (LSTM)
- https://mp.weixin.qq.com/s/0kNrI3VyuCXMz5yNKmACyA
- https://www.futuretools.io/?tags=generative-art
