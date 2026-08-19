# Human observations — direct use

## Chat

- The user did not consider the 32B model practically useful compared with current hosted frontier models.
- Four of seven submitted prompts in the observed session returned `HTTP 400 Bad Request`.
- The chat client displayed every HTTP failure as `connection error`, making the experience feel like repeated connection loss.
- Successful answers still felt substantially below the conversational quality of current high-end hosted models.
- One answer responded to `聞こえる？` with an irrelevant description of Kanagawa and incorrectly listed Waseda University among examples of universities in Kanagawa.
- The repeated failures were a major source of frustration independent of model intelligence.

## Coding

- The initial JavaScript version appeared to run relatively well.
- The first requested correction did not affect the version being played.
- When asked how to launch it, the model switched the HTML to a newly created JavaScript file and claimed the files would work together.
- The replacement displayed blocks but did not behave as a game.
- The user did not feel a major practical improvement over the smaller model configurations.

## Adoption judgment

The 32B model clearly improved the deterministic benchmark, but that success did not translate into a reliable chat or iterative vibe-coding experience. The configuration remained below the user's practical adoption threshold.
