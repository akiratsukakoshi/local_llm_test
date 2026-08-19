# Human observations — direct use

## Chat

- Response latency remained fast.
- The user did not feel a meaningful improvement in conversational quality over the 7B model.
- The model initially admitted that it did not know `原っぱ大学`, which was appropriate.
- After the user said it was a play-oriented school in Zushi, Kanagawa, the model claimed that it had researched the subject even though this chat harness had no browsing tool.
- It then presented specific unsupported claims about a supposed `逗子市遊戯学校`, a 1947 founding date, its educational mission, and an attached kindergarten.
- The user identified this as an obvious hallucination.
- Overall judgment: chat quality remained below a level the user would choose to use.

## Coding

- Generation felt somewhat slower than with the 7B model.
- The initial interpretation of Space Invaders was better than the 7B attempt: enemies moved horizontally and descended rather than simply falling vertically.
- Shooting did not work initially and required one correction.
- Horizontal player movement was reported not to work reliably.
- The animation stopped after roughly three to five seconds.
- Multiple correction attempts did not resolve the stopping behavior.
- Overall judgment: the improvement over 7B was visible but still far below the user's practical usability threshold.

## Adoption judgment

The controlled `slugify` result improved from the 7B baseline, but that improvement did not translate into a clearly better conversational experience or a dependable small product-building experience. The user would not use this configuration for real work.
