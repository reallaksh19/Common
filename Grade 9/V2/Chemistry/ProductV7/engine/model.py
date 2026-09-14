from __future__ import annotations

def B(kind,text,asset_ids=(),frozen=False):
    return {'kind':kind,'text':text,'asset_ids':list(asset_ids),'frozen':frozen}

def page(page_id,title,badges,blocks,ttus=(),workspace=False):
    return {'page_id':page_id,'title':title,'badges':badges,'blocks':blocks,'ttu_ids':list(ttus),'workspace':workspace}

def build_page_models(AUTH):
    QUESTIONS={q['question_id']:q for q in AUTH['questions']}
    rule1=AUTH['canonical_rules'][0]['text']; rule2=AUTH['canonical_rules'][1]['text']; rule3=AUTH['canonical_rules'][2]['text']
    q15=QUESTIONS['CHEM-C2A-SRC-U2Q15C']; q35=QUESTIONS['CHEM-C2A-SRC-U2Q35']
    models={}
    models['CORE1A']=[
      page('C1A-P1','Separate the record from the claim',['Bucket','Concept','Medium','First study','Table'],[
        B('PROSE','The technical problem is not vocabulary; it is claim control. A record states what a learner could see, smell, hear, measure or obtain from a named test. An inference names what that record supports. Keep the two in separate fields before connecting them.'),
        B('CANONICAL',rule1,['C1A-RULE-PRIORITY'],True),
        B('TABLE','Observation/test: gas gives a pop | Inference: gas is hydrogen | Evidence link: the pop is the distinguishing test result',['C1A-OBS-INF-TABLE']),
        B('TABLE','Record only | Interpret next | Verify last ; gas evolves | a gas formed | identity still unresolved ; test gives characteristic result | candidate identity | link test to identity'),
        B('PROSE','Decision procedure: underline every phrase that can be recorded directly; box every phrase that names a substance or process; draw an arrow only when the underlined evidence is sufficient to support the boxed claim.'),
        B('PROSE','Use the table from left to right. The third column is not decoration: it must state why the observation licenses the inference. If that bridge cannot be written, the claim is premature.'),
        B('TTU','Complete: [recorded result] -> [what the result indicates] -> [bounded conclusion].',['C1A-EVIDENCE-CHAIN'])
      ],['C1A-EVIDENCE-CHAIN']),
      page('C1A-P2','Control the strength of a conclusion',['Concept','Medium','Linkage','Contrast','Check'],[
        B('PROSE','Evidence sets an upper bound on the conclusion. “A gas formed” supports existence of a gas; it does not by itself identify that gas. A distinguishing result can support identity. This creates a claim-strength ladder rather than a yes/no rule.'),
        B('CANONICAL',rule2,['C1A-CLAIM-STRENGTH'],True),
        B('TABLE','Evidence only: gas evolves -> allowed claim: gas formed -> not yet allowed: gas identity'),
        B('TABLE','Evidence plus distinguishing test -> allowed claim: identity tied to that test'),
        B('PROSE','Minimal contrast: “A colourless gas is seen” and “the gas gives a pop with a lighted splint” are not equivalent evidence statements. The second contains a discriminating test result.'),
        B('DIAGRAM','Claim strength -> gas exists -> property/test result -> gas identity -> wider causal explanation'),
        B('TABLE','Evidence available | strongest safe conclusion | overclaim to reject ; bubbles only | gas formed | hydrogen formed ; pop test | hydrogen supported | any unrelated gas identity ; smell only | characteristic property recorded | unsupported reaction mechanism'),
        B('TTU','Reconstruct which rung each conclusion belongs to, then reject any conclusion that jumps over a missing evidence rung.')
      ],['C1A-CLAIM-STRENGTH']),
      page('C1A-P3','Keep event order attached to evidence',['Concept','Medium','Event line','Causal link','Verify'],[
        B('PROSE','When two treatments differ, preserve event order before interpreting the observations. Mixing, heating, adding a reagent and testing a gas are different events; collapsing them can attach an observation to the wrong cause.'),
        B('DIAGRAM','Event line: initial material -> treatment -> reagent/test -> observation -> inference',['C1A-EVENT-LINE']),
        B('PROSE','The inference belongs after the observation on the event line. A test result can justify identity; the identity should not be written into the observation box.'),
        B('CANONICAL',rule3,[],True),
        B('TABLE','Event | direct record | interpretation allowed now? | what must wait ; treatment | heating/no heating | no gas identity yet | later test ; gas evolution | gas formed | yes: formation | identity ; distinguishing test | test result | yes: supported identity | broader cause'),
        B('VERIFY','Backward trace: start from a proposed gas name and move left until you reach the exact test or observation that supports it. If the trace stops at “gas evolved”, identity is not closed.'),
        B('TTU','Given two branches with different treatments, mark where the branches diverge and write a separate observation-to-inference chain for each branch.')
      ],['C1A-EVENT-LINE']),
      page('C1A-P4','Error clinic and independent verification',['Concept','Medium','Misconception','Repair','Verification'],[
        B('PROSE','Diagnose the sentence “I observed hydrogen gas.” The wording hides the evidence. Repair it by writing the actual test result first and placing “hydrogen” in the inference column.'),
        B('TABLE','Wrong model | Missing evidence | Repaired record | Supported inference',['C1A-ERROR-CLINIC']),
        B('PROSE','Second trap: gas evolution is sometimes treated as if it identifies the gas. The repair is to ask which observation distinguishes the proposed identity from alternatives.'),
        B('CANONICAL',AUTH['verification'][0]['check'],['C1A-VERIFY'],True),
        B('TABLE','Failure type | diagnostic question | repair ; observation contains a substance name | what was actually seen/tested? | move the name to inference ; inference has no arrow | which evidence supports it? | add or weaken claim ; two cases merged | where did histories diverge? | rebuild two event lines'),
        B('PROSE','Worked repair: replace “hydrogen was observed” with a test-result statement in the observation field, then place “hydrogen” in the inference field and connect the two with the named test.'),
        B('TTU','Independent check: cover the page, write the three-column ledger from memory, and use it to repair one overclaim without looking back.')
      ],['C1A-ERROR-CLINIC'])
    ]

    models['CORE1B']=[
      page('C1B-P1','Build the distinction before naming it',['Bucket','Concept','Medium','Reconstruct','Table'],[
        B('PROMPT','A gas is evolved. A later test gives a characteristic result. Make two columns before you explain anything: “what happened / what the test did” and “what I conclude”. Do not put a substance name in the first column.'),
        B('TTU','Incomplete ledger: OBSERVATION/TEST = ______ ; INFERENCE = ______ ; EVIDENCE LINK = because ______',['C1B-TTU-OBS-INF-TABLE','C1B-TTU-CLAIM-CHAIN']),
        B('PROMPT','Now write one sentence explaining why the first column is not already a chemical conclusion.'),
        B('HELP','Self-help 1: ask what another person could record without knowing the answer. Self-help 2: ask what statement requires interpretation.'),
        B('TTU','Second reconstruction: write one statement that is only an observation and a second statement that is only an inference. Swap them deliberately; explain why the swapped version fails.'),
        B('CANONICAL','Canonical check: record evidence first; place the chemical identity or conclusion in the inference field after the evidence link.',['C1B-VERIFY'],True)
      ],['C1B-TTU-OBS-INF-TABLE','C1B-TTU-CLAIM-CHAIN'],True),
      page('C1B-P2','Discover the evidence ceiling',['Concept','Medium','Compare','Diagnose','Verify'],[
        B('PROMPT','Rank these claims from weakest to strongest: “a gas formed”; “the gas has property X”; “the gas is substance Y”. What additional evidence would be needed before moving up each rung?'),
        B('TTU','Claim ladder: [formation] -> [property/test] -> [identity]. Fill the missing evidence under every arrow.',['C1B-TTU-CLAIM-STRENGTH']),
        B('PROMPT','A learner writes: “Bubbles prove hydrogen.” Identify the exact logical jump. Then rewrite the statement so that the conclusion cannot outrun the evidence.',['C1B-TTU-ERROR-DIAGNOSIS']),
        B('HELP','If stuck: separate evidence of existence from evidence of identity. A distinguishing test belongs between those two claims.'),
        B('TTU','Contrast case: a gas is visible but no identifying test is given. Write the strongest safe claim, then write one tempting but forbidden claim and cross it out.'),
        B('CANONICAL','Canonical principle: the strongest permitted claim is limited by the strongest recorded evidence.',['C1B-VERIFY'],True)
      ],['C1B-TTU-CLAIM-STRENGTH','C1B-TTU-ERROR-DIAGNOSIS'],True),
      page('C1B-P3','Reconstruct two evidence chains',['Concept','Medium','Event line','Branching','Explain'],[
        B('PROMPT','Two samples start alike but receive different treatments. After that, the same reagent is added. Draw two event lines. Your lines must show the exact event where the histories diverge.'),
        B('TTU','Branch A: start -> ______ -> reagent -> observation -> ______.  Branch B: start -> ______ -> reagent -> observation -> ______.',['C1B-TTU-EVENT-LINE']),
        B('PROMPT','Why is it unsafe to combine the two branches into a single explanation just because both produce a gas?'),
        B('HELP','Look for the earlier treatment. Same final surface feature does not imply the same chemical identity when the preceding state is different.'),
        B('TTU','Branch audit table: for A and B, fill treatment / observation / test result / inference. Circle any cell copied across branches without evidence.'),
        B('CANONICAL','Check your reconstruction by tracing each inference backward until it lands on a specific observation or test result.',['C1B-VERIFY'],True)
      ],['C1B-TTU-EVENT-LINE'],True),
      page('C1B-P4','Teach it back without the notes',['Concept','Medium','Retrieve','Teach-back','Repair'],[
        B('PROMPT','Without looking back, draw the evidence-to-claim chain and define “observation” and “inference” using your own chemical example.'),
        B('TTU','Blank chain: ______ -> ______ -> ______ ; boundary question: what would make the final claim too strong?'),
        B('PROMPT','Self-diagnose: if you named a substance before writing evidence, reopen the observation/inference table; if you mixed two histories, reopen the event line; if you cannot justify the identity, reopen the claim ladder.'),
        B('HELP','Final hint only: a valid inference can point backward to its evidence. A valid observation does not depend on already knowing the chemical identity.'),
        B('TTU','Counterexample challenge: invent a case where gas evolution occurs but hydrogen would be an unjustified identity. State what extra observation would be needed before naming hydrogen.'),
        B('CANONICAL','Master check: every conclusion on your page should have an explicit evidence arrow and no arrow may skip a required test.',['C1B-VERIFY'],True)
      ],['C1B-VERIFY'],True)
    ]

    src_badges=['Question','Task demand','Revision','Source','Guided']
    models['CORE2A']=[
      page('C2A-P1','Q15(c): expert setup and solution',src_badges,[
        B('SOURCE',q15['learner_visible_source'],['C2A-Q-U2Q15C'],True),
        B('QUESTION',q15['stem'],[],True),
        B('PROSE','Recognition: this question tests whether you can report the change without letting interpretation erase the observation. Start by separating the process/evidence from the chemical conclusion.'),
        B('TTU','Expert ledger: OBSERVED/PROCESS EVIDENCE | CHEMICAL INFERENCE. Complete the two cells before reading the answer.',['C2A-U2Q15C-LEDGER']),
        B('SOLUTION','Worked route: (1) retain the stated strong heating; (2) state the resulting evidence/process; (3) state the chemical conclusion separately; (4) make sure the conclusion is no stronger than the evidence.'),
        B('TABLE','Why each step exists | technical reason ; preserve strong heating | condition belongs to the evidence chain ; separate evidence/inference | prevents the product name from replacing the record ; bound the conclusion | avoids claiming more than the source supports'),
        B('TRAP','Common wrong route: jump directly from “heated strongly” to a named product without making the evidence/inference distinction explicit.'),
        B('CANONICAL','Quick answer: '+q15['quick_answer'],['C2A-ANS-U2Q15C'],True),
        B('VERIFY','Verification: can each conclusion be paired with the observation/process statement that supports it?',['C2A-VERIFY'])
      ],['C2A-U2Q15C-LEDGER']),
      page('C2A-P2','Q35: map the two histories before solving',src_badges,[
        B('SOURCE',q35['learner_visible_source'],['C2A-Q-U2Q35'],True),
        B('QUESTION',q35['stem'],[],True),
        B('PROSE','Recognition: the two parts have different histories. The safest setup is not a single gas-identification list; it is two parallel event lines so the later gas evidence remains attached to the correct treatment.'),
        B('DIAGRAM','Part A: mixture -> strong heating -> add dilute HCl -> gas evidence -> identity.  Part B: mixture -> no heating -> add dilute HCl -> gas evidence -> identity.',['C2A-U2Q35-EVENT-LINE']),
        B('TABLE','Part | prior treatment | evidence used for identification | inferred gas'),
        B('TRAP','Trap: “gas evolved in both” is shared evidence of formation, not proof that the gases have the same identity.',['C2A-U2Q35-TRAP']),
        B('TTU','Completion setup: fill only the treatment and evidence columns for A and B; leave gas identity blank until the evidence column is complete.')
      ],['C2A-U2Q35-EVENT-LINE']),
      page('C2A-P3','Q35: complete worked resolution',src_badges,[
        B('SOLUTION','Part A: keep the heating step attached to the sample before considering the acid step. Use the stated characteristic evidence to identify hydrogen sulphide. Part B: keep the unheated iron/sulphur mixture distinct; the hydrogen produced from the iron/acid route is identified by the pop test.'),
        B('TABLE','A | heated first | characteristic foul smell / lead acetate blackening | hydrogen sulphide.  B | not heated | pop test | hydrogen.',['C2A-U2Q35-EVIDENCE-CHECK']),
        B('CANONICAL','Quick answer: '+q35['quick_answer'],['C2A-ANS-U2Q35'],True),
        B('VERIFY','Independent check: swap the gas names mentally. The evidence then conflicts with the identification tests, so the swap fails.',['C2A-VERIFY']),
        B('TABLE','Evidence discrimination | Part A | Part B ; prior state | heated product present | unheated mixture ; identifying evidence | H2S characteristic evidence | H2 pop test ; safe inference | hydrogen sulphide | hydrogen'),
        B('TRAP','Counterfactual check: if you exchange the identification tests between A and B, the evidence-to-claim mapping breaks. This is why the two gas names cannot be justified by “gas evolved” alone.'),
        B('PROSE','What to retain: when two cases differ before the test, preserve their event histories. Never let a common surface feature erase the discriminating evidence.')
      ],['C2A-U2Q35-EVIDENCE-CHECK'])
    ]

    models['CORE2B']=[
      page('C2B-P1','Q15(c): attempt before the route is shown',src_badges,[
        B('SOURCE',q15['learner_visible_source'],['C2B-Q-U2Q15C'],True),
        B('QUESTION',q15['stem'],[],True),
        B('PROMPT','Commit first: what exactly is the question asking you to report - a visible/process record, a chemical identity, or both? Write the target in five words or fewer.'),
        B('TTU','Choose a representation: [ ] two-column observation/inference ledger  [ ] event line  [ ] other. Build it before opening the help.',['C2B-U2Q15C-PLAN']),
        B('PROMPT','First move: write the evidence/process statement only. Then decide whether an inference is justified.'),
        B('TTU','Commitment box: TARGET = ____ ; EVIDENCE I WILL USE = ____ ; CLAIM I WILL NOT MAKE YET = ____.'),
        B('HELP','H1 Notice: strong heating is part of the evidence chain. H2 Represent: separate the record from the conclusion. H3 Check: is any claim stronger than what the question supports?')
      ],['C2B-U2Q15C-PLAN'],True),
      page('C2B-P2','Q15(c): compare your reasoning with the authority',src_badges,[
        B('CANONICAL','Answer authority: '+q15['quick_answer'],['C2B-ANS-U2Q15C'],True),
        B('PROSE','Compare routes, not wording. A sound answer keeps the heating/event evidence visible and then states the formation of the new substance. If you wrote only a named product with no evidence chain, your reasoning is under-explained even if the final noun is correct.'),
        B('TTU','Repair box: MY EVIDENCE = ____ ; MY INFERENCE = ____ ; SUPPORT LINK = ____. Rebuild only the missing part.'),
        B('TTU','Compare: mark which part of your first attempt was recognition, which was evidence, and which was inference. Rewrite only the part that changed after the reveal.'),
        B('VERIFY','Falsifier: could someone read your evidence cell without already knowing the name of the product?',['C2B-VERIFY'])
      ],['C2B-VERIFY'],True),
      page('C2B-P3','Q35: build the problem model',src_badges,[
        B('SOURCE',q35['learner_visible_source'],['C2B-Q-U2Q35'],True),
        B('QUESTION',q35['stem'],[],True),
        B('PROMPT','Do not identify either gas yet. Mark the one event that makes Part A and Part B chemically different before acid is added.'),
        B('TTU','Construct two lines from scratch: A [start -> treatment -> acid -> evidence -> gas] ; B [start -> treatment -> acid -> evidence -> gas].',['C2B-U2Q35-TWO-CHAIN']),
        B('PROMPT','Now choose the discriminating evidence for each branch. Explain why “gas evolved” is not sufficient to name either gas.'),
        B('HELP','H1 Structure: histories diverge before acid. H2 Representation: two branches, not one list. H3 Principle: identity requires a distinguishing observation/test. H4 First move: fill the treatment column before the gas column.'),
        B('TTU','Commitment check: before reveal, write GAS A = ____ because evidence ____ ; GAS B = ____ because evidence ____.')
      ],['C2B-U2Q35-TWO-CHAIN'],True),
      page('C2B-P4','Q35: reveal, falsify, transfer',src_badges,[
        B('CANONICAL','Answer authority: '+q35['quick_answer'],['C2B-ANS-U2Q35'],True),
        B('PROSE','Audit your model: Part A must connect the heated history to hydrogen sulphide evidence; Part B must connect the unheated mixture to hydrogen evidence. A correct pair of gas names with the evidence chains crossed is not a correct solution model.'),
        B('TTU','Falsification matrix: proposed gas | observed/test evidence | consistent? yes/no | reason.',['C2B-U2Q35-CHECK']),
        B('VERIFY','Transfer check: if a new question changes the treatment but keeps “gas evolved,” start by rebuilding the event history rather than recycling the previous gas name.',['C2B-VERIFY']),
        B('TABLE','Error diagnosis | repair route ; gas names correct but tests crossed | rebuild evidence links ; both branches given same gas | re-check prior treatment ; identity based only on gas evolution | locate distinguishing test'),
        B('TTU','Fresh-sibling plan: write only a representation choice and first move for a new two-case gas question; do not reuse either gas name from Q35 unless new evidence supports it.'),
        B('PROMPT','One-sentence generalisation: “When two chemical cases share a surface observation but differ in prior treatment, I should first ______.”')
      ],['C2B-U2Q35-CHECK'],True)
    ]
    return models
