"""Author-created engineering fixtures; no claim of complete learner books."""

import hashlib
import json
from pathlib import Path

from v3b.contracts import digest


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def make_fixture(root: Path):
    equation = '<math display="block"><mrow><mi>v</mi><mo>=</mo><msqrt><mrow><msubsup><mi>v</mi><mi>x</mi><mn>2</mn></msubsup><mo>+</mo><msubsup><mi>v</mi><mi>y</mi><mn>2</mn></msubsup></mrow></msqrt></mrow></math>'
    atoms = [dict(id=k, value=v, unit=u, kind='DATUM', locator='Author-created fixture datum ' + k)
             for k, v, u in [('vx', -3, 'm/s'), ('vy', 4, 'm/s'), ('fx', 6, 'N'), ('fy', -8, 'N'),
                              ('u', 4, 'm/s'), ('a', -2, 'm/s^2'), ('t', 1, 's'),
                              ('t0', 0, 's'), ('t1', 2, 's'), ('t2', 4, 's'),
                              ('T0', 320, 'K'), ('T1', 310, 'K'), ('T2', 310, 'K'), ('Tmin', 300, 'K')]]
    atoms.append(dict(id='speed_eq', value=equation, kind='EQUATION', locator='Pythagoras relationship for perpendicular velocity components'))
    questions = [
        dict(id='qv', original_number='G01', stem='A velocity has components −3 m/s along x and +4 m/s along y. Find its speed and explain its direction.',
             verification=dict(validator_id='SPEED_FROM_COMPONENTS', bindings=dict(vx='vx', vy='vy'))),
        dict(id='qf', original_number='G02', stem='A force has components +6 N horizontally and −8 N vertically. Which quadrant contains its arrow? Draw the vector before checking the model.'),
        dict(id='qa', original_number='G03', stem='A body starts at +4 m/s and accelerates constantly at −2 m/s² for 1 s. Find its final velocity.',
             verification=dict(validator_id='CONSTANT_ACCELERATION_VELOCITY', bindings=dict(u='u', a='a', t='t'), model='CONSTANT_ACCELERATION', axis_convention='+x is right')),
        dict(id='qg', original_number='G04', stem='A temperature–time graph joins (0 s, 320 K), (2 s, 310 K) and (4 s, 310 K). Describe what changes and what stays unchanged. Does the horizontal segment prove that no energy is transferred?')]
    source = dict(id='AUTHOR', origin='AUTHOR_CREATED', citation='V3B publication integration specimen; original generated questions, not CBSE examination items', atoms=atoms, questions=questions)
    write_json(root / 'sources/source.json', source)
    groups = [['vx', 'vy', 'speed_eq'], ['fx', 'fy'], ['u', 'a', 't'], ['t0', 't1', 't2', 'T0', 'T1', 'T2', 'Tmin']]
    cores = ['CORE1A', 'CORE1B', 'CORE2A', 'CORE2B']
    baseline = dict(schema_version='1.0.0', topic_id='PUBLICATION-INTEGRATION', baseline_id='BASE-1', selected_cores=cores,
                    sources=[dict(id='AUTHOR', path='source.json', sha256=hashlib.sha256((root / 'sources/source.json').read_bytes()).hexdigest())],
                    buckets=[dict(id='B' + str(i), badge='MEDIUM', prerequisites=[]) for i in range(4)],
                    obligations=[dict(id='O' + str(i), bucket_id='B' + str(i), source_atom_ids=group,
                                      required_cores=[core], required_kinds=['TEXT', 'QUESTION'])
                                 for i, (group, core) in enumerate(zip(groups, cores))],
                    required_questions=[dict(core=core, source_id='AUTHOR', question_id=q['id']) for core, q in zip(cores, questions)])
    introductions = [
        'Read the signs before calculating. The negative x component points left; the positive y component points upward. These are two descriptions of one velocity, not two journeys made one after the other. A right triangle connects the components to the speed: squaring removes the signs for the length calculation, but the signs still determine the direction.',
        'First decide which sign controls each direction. Predict where the endpoint belongs and draw it yourself. If you drew it above the origin, check what the minus sign on the vertical component tells you. After the model drawing, explain why rotating the axes would change the components but would not physically change the force.',
        'Separate the initial velocity, change in velocity and final velocity. A negative acceleration means that the change points toward negative x; it does not automatically mean the body is already moving left. Keep units beside the substitution so that acceleration multiplied by time becomes a velocity change.',
        'Describe the graph before selecting a physical explanation. A line sloping down indicates a decreasing measured temperature. A horizontal line indicates an unchanged measured temperature. Decide whether that measurement alone can tell you the heat transfer or the physical process. Use the answer to check the limits of your inference.']
    solutions = [
        ('The speed is 5 m/s. The velocity points into the upper-left quadrant.', ['Draw the two perpendicular components from the same physical origin.', 'Apply the right-triangle relationship: speed squared = (−3)² + 4² = 25 (m/s)².', 'Take the nonnegative square root for speed; retain the original component signs for direction.'], 'The speed exceeds either component magnitude. Reversing both components would preserve the speed but reverse the direction.'),
        ('The vector lies below and to the right of the origin.', ['A positive horizontal component points right.', 'A negative vertical component points down.', 'Connect the origin to the endpoint reached by those component changes; the model drawing appears below.'], 'A drawing above the horizontal axis would contradict the negative vertical component.'),
        ('The final velocity is +2 m/s.', ['Identify u = +4 m/s, a = −2 m/s² and elapsed time = 1 s.', 'Calculate the velocity change: a × t = −2 m/s.', 'Add this change to the initial velocity: +4 + (−2) = +2 m/s.'], 'The body is still moving right, more slowly. A negative acceleration did not by itself reverse the velocity.'),
        ('Temperature decreases in the first interval and stays constant in the second. The graph alone does not prove zero energy transfer.', ['Compare the two endpoint temperatures in the first interval: the measured temperature falls.', 'Compare the temperatures at 2 s and 4 s: the measured value is unchanged.', 'State the evidence limit: interpreting heat transfer also requires a model of the system and process.'], 'Do not confuse an unchanged measured temperature with proof that every energy transfer is zero.')]
    products = []
    for i, (core, q, group, intro, solution) in enumerate(zip(cores, questions, groups, introductions, solutions)):
        base = dict(obligation_ids=['O' + str(i)], source_atom_ids=group)
        answer = dict(summary=solution[0], steps=solution[1], check=solution[2])
        if i in (0, 2):
            answer['numeric'] = dict(value=5 if i == 0 else 2, unit='m/s')
        question = dict(base, id=core + '-Q', kind='QUESTION', source_id='AUTHOR', source_question_id=q['id'],
                        original_number=q['original_number'], stem=q['stem'], answer=answer,
                        hints=['Identify the quantities or observations supplied.', 'Connect their signs or changes to the representation.', 'Check each reasoning step, then compare with the full answer.'],
                        family='components' if i < 2 else ('constant_acceleration' if i == 2 else 'graph_inference'),
                        learner_action=['worked_explanation', 'reconstruct', 'solve', 'judge_model_limits'][i],
                        exposure_role=['WORKED_EXAMPLE', 'RECONSTRUCTION_ANCHOR', 'PRACTICE', 'NEW_TRANSFER'][i])
        blocks = [dict(base, id=core + '-T', kind='TEXT', text=intro), question]
        if i == 0:
            blocks.insert(1, dict(base, id=core + '-E', kind='EQUATION', mathml=equation,
                                 meaning='Speed is the nonnegative magnitude of a velocity with perpendicular components.',
                                 symbols=['v: speed, in m/s.', 'vx and vy: signed perpendicular components, in m/s.'],
                                 conditions=['Both components use the same physical frame and time.', 'The coordinate axes are perpendicular.']))
        if i in (0, 1):
            blocks.append(dict(base, id=core + '-F', kind='FIGURE', placement='ANSWER', question_id=core + '-Q',
                               scene=dict(kind='VECTOR', x_atom=group[0], y_atom=group[1], unit='m/s' if i == 0 else 'N',
                                          symbol='v' if i == 0 else 'F', frame='horizontal x right; vertical y up',
                                          x_label='x component (' + ('m/s' if i == 0 else 'N') + ')',
                                          y_label='y component (' + ('m/s' if i == 0 else 'N') + ')',
                                          caption='Component signs determine the vector direction.')))
        if i == 3:
            blocks.append(dict(base, id=core + '-F', kind='FIGURE', scene=dict(kind='GRAPH', points=[['t0','T0'],['t1','T1'],['t2','T2']],
                              x_unit='s', y_unit='K', y_min_atom='Tmin', frame='elapsed time and measured temperature', x_label='Time (s)', y_label='Temperature (K)',
                              caption='The temperature falls, then stays constant. Read the labelled vertical-axis minimum.')))
        products.append(dict(core=core, units=[dict(id='U' + str(i), bucket_id='B' + str(i), title=['Explained components', 'Reconstruct a vector', 'Resolve a velocity change', 'Interpret a different physical graph'][i], blocks=blocks)]))
    plan = dict(schema_version='1.0.0', subject='Physics', topic_id=baseline['topic_id'], title='Physics publication integration specimen', baseline_digest=digest(baseline),
                practice_control=dict(mode='DESIGN_PREVIEW', purpose='PRACTICE'), products=products)
    write_json(root / 'baseline.json', baseline)
    write_json(root / 'plan.json', plan)
    # Tests mutate independent authority inputs; never share list aliases across them.
    return json.loads(json.dumps(plan)), json.loads(json.dumps(baseline))
