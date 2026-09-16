# Core (1A) <-> Core (2) learner linking

Core (2) v2 is the fixed practice surface for this chapter. Core (1A) must teach the idea first, then point the learner to the exact Core (2) challenges that use it.

## Learner wording

Do not expose internal production language such as `repair`, `custody`, `falsifier`, `remediation`, `semantic drift`, or `source-grounded` on learner pages.

Use these labels instead:

- `Where you will use this` - forward concept-to-question link
- `Try Core (2)` - action from Core (1A)
- `Need a quick refresher?` - return path from Core (2)
- `Go back to this idea` - return action
- `Ready to practise?` - end-of-concept gateway
- `Easy mistake to make` - misconception callout
- `Does the answer make sense?` - physical verification

## Bidirectional contract

```text
CORE (1A)
learn the idea
   |
   +--> Quick check
   +--> Try it with help
   +--> Try Core (2): Qxx, Qyy, ...
                         |
                         v
                    CORE (2)
                  attempt first
                         |
             +-----------+-----------+
             |                       |
          confident              need help
             |                       |
             v                       v
       next challenge       Need a quick refresher?
                                     |
                                     v
                           Go back to this idea
                           in Core (1A)
```

The return target is a **concept/stage**, not an arbitrary page. Example: Q03 `Horizontal launch` returns to the stage that shows vertical fall setting the shared time; Q15 `Moving launch source` returns to the velocity-addition stage; Q53 `Accelerating reference frame` returns to the accelerating-observer stage.

## Linkage authority

`registry/physics-core1a-core2-linkage.json` is the single machine-readable map. It contains all 59 Core (2) questions exactly once and records the Core (1A) concept that should teach each question's decisive idea.

The registry is derived from the explicit `Review: Core (1A) ...` routes already present in Revised Core (2) v2. Core (1A) must follow those routes rather than invent a second question taxonomy.

## Concept groups used by Core (2)

| Core (1A) concept | Learner-facing title | Core (2) challenges |
|---|---|---|
| 2.3-2.7 | Follow the velocity through the flight | Q01, Q11, Q13, Q14, Q17, Q27, Q40 |
| 2.4-2.5 | Time, range, height and matching-angle shortcuts | Q02, Q06, Q07, Q12, Q16, Q18, Q19, Q20, Q22, Q24, Q25, Q44, Q52 |
| 2.7 | Horizontal launch: one sideways speed, one falling motion | Q03, Q04, Q08, Q29, Q34, Q42 |
| 2.3 + 6.2 | Use one shared clock at special moments | Q05, Q26 |
| 2.7 + 6.2 | Launch from a height: choose a vertical direction and keep it | Q09, Q30, Q36 |
| 2.3 | One clock, two directions | Q10, Q43 |
| 2.6 | Describe the path without using time | Q38, Q47 |
| 6.1 | Projectile motion with a sloping landing surface | Q54, Q55, Q56 |
| 6.2 | Moving launchers: add the platform motion | Q15 |
| 6.2 | Track change: momentum and average velocity | Q21, Q39, Q58, Q59 |
| 6.2 | Meet at the same place, at the same time | Q23, Q28, Q35, Q37 |
| 6.2 | Spot the pattern before calculating | Q31, Q32, Q33 |
| 6.2 | Work backwards: design the launch | Q41, Q49, Q51 |
| 6.2 | How the projectile turns about a chosen point | Q45, Q46 |
| 6.2 | When the projectile also accelerates sideways | Q48 |
| 6.2 | Bounce from a sloping surface | Q50, Q57 |
| 6.2 | What changes when the observer is accelerating | Q53 |

## Rendering rule

A Core (1A) concept footer should never say `repair link`. It should render:

```text
WHERE YOU WILL USE THIS
Core (2): Q03 Horizontal launch | Q04 Horizontal launch to a target

READY TO PRACTISE?
[Quick check] -> [Try it with help] -> [Try Core (2)]
```

A Core (2) return link should render:

```text
NEED A QUICK REFRESHER?
Go back to: Horizontal launch - one sideways speed, one falling motion
```

Internally, stable IDs may remain technical. Learner-visible labels must come from `physics-core1a-learner-language.json`.
