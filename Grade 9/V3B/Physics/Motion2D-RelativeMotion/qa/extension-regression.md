# EXT-001 impacted-check rerun — SELF_REVIEW

The extension request “Add equal-velocity, different-initial-position relative motion” is implemented only under `changes/`; the 159-atom baseline source inventory, six baseline learner books and baseline question/coverage registers remain historical artifacts.

## Dependency/model check

`B05E` reuses baseline `EQ05` relative velocity and `EQ06` relative position. It adds no new frame transform or mathematical prerequisite. The new invariant follows directly: if `v_A/G=v_B/G`, then `v_A/B=0`, hence `r_A/B(t)=r_A/B(0)`. The initial relative position may be nonzero, and equal nonzero ground velocities do not make either object ground-stationary.

## Staleness / successor closure

The change record correctly marks Core1/Core1A/Core1B B05 teaching, Core2A `2A-Q10`, Core2B `2B-Q04`, G2/G4/G6/G7 and the B04–B06 packet as stale **for extension-aware use only**. The separate extension artifacts supply a Core1 note, Core1A worked example, Core1B reconstruction checkpoint, Core2A question/solution and Core2B transfer closure. The successor question register has 70 rows; successor coverage has 164 atom rows representing 984 atom×Core dispositions (954 baseline + 30 extension dispositions), with all 25 extension-required Core realizations present and Core2 explicitly not required because its frozen source corpus is unchanged.

`EXT-Q-001` demand is 3/10 (entry): inference 1, representation translation 1, interacting constraints 1, algebra 0, novelty 0. Its high support does not lower that demand score.

## Reuse/transfer review

The same canonical invariant necessarily appears across the extension products, but the learner action changes: Core1 states the rule, Core1A derives it with a worked position example, Core1B asks for a prediction and repair, Core2A apprentices a complete solution, and Core2B asks for a no-final-position transfer argument. This is justified canonical/model reuse, not numeric relabeling presented as fresh external source.

Cold fresh-agent verification and independent review remain `NOT_RUN`.
