# Initial Space Invaders assessment

## Improvements over the 14B first attempt

- The formation direction is stored separately in mutable `invaderDirection`, avoiding the 14B model's fatal attempt to reassign a `const` speed value.
- Formation bounds are calculated once per frame, so direction reversal and descent happen once for the group rather than once per invader.
- Player movement, shooting, bullet movement, and collision detection are present in the first version.
- JavaScript syntax validation passed.

## Remaining weaknesses visible before play testing

- The initial formation is wider than the 400-pixel canvas; the last invader begins outside the visible area and causes an immediate direction change and descent.
- There is no score, game-over condition, win state, lives, restart, enemy firing, or explanatory UI.
- Player movement depends on browser key-repeat events rather than tracked key state, so movement may feel uneven.
- Removing array elements from nested `forEach` loops can skip collisions when several objects overlap in one frame.
- Once every invader is removed, the animation continues on an empty screen with no completion state.

## Verification limitation

Automated in-app browser control could not be initialized because the Windows-side browser runtime failed during setup. The code was syntax-checked and statically inspected, but actual controls and animation continuity still require the human play test.
