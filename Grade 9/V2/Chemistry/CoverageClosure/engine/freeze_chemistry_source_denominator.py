#!/usr/bin/env python3
"""Generic Chemistry source-ingestion / denominator-freezing stage.

PR #346 proved the discipline by hand: for each of its four NCERT topic
baselines it scanned the supplied corpus, decided in-scope / out-of-scope,
and only then started authoring. That audit was manual and per-topic, so the
next chapter would have had to repeat it from scratch — and nothing stopped an
agent from authoring first and reconciling afterwards.

This module makes it a real pipeline stage. A frozen denominator is a record
whose counters are **re-derived from declared evidence** at validation time and
compared with what was frozen; a counter that cannot be derived is recorded as
``unresolved`` rather than guessed. Authoring is gated on the freeze:
``assert_authoring_allowed`` raises ``AUTHORING_BEFORE_DENOMINATOR_FREEZE``
unless the instance is frozen to the level the profile demands.

Counters (from the profile, and from #346's WORKFLOW.md Phase 1):

    TOTAL_SCANNED  ELIGIBLE_IN_SCOPE  PLACED_UNIQUE
    EXCLUDED_WITH_REASON  UNRESOLVED_WITH_REASON  MISSING  DUPLICATE_PRIMARY

Closure:

    ELIGIBLE_IN_SCOPE == PLACED_UNIQUE
    MISSING == 0
    DUPLICATE_PRIMARY == 0
    TOTAL_SCANNED == ELIGIBLE_IN_SCOPE + EXCLUDED_WITH_REASON + UNRESOLVED_WITH_REASON
"""
import argparse, ast, copy, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve()
CHEM = HERE.parents[2]
REPO = HERE.parents[5]
PROFILE_PATH = CHEM / 'CoverageClosure' / 'registry' / 'chemistry-source-ingestion-profile.json'

ELIGIBLE = 'ELIGIBLE_IN_SCOPE'
UNRESOLVED_STATUSES = {'SOURCE_UNRESOLVED', 'UNRESOLVED'}


def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field: x.pop(field, None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fail(code, detail=''): raise ValueError(f'{code}: {detail}' if detail else code)


# ---------------------------------------------------------------------------
# counter derivation from an item ledger (the generic replacement for the
# per-topic manual audit)
# ---------------------------------------------------------------------------

def counters_from_items(items):
    """Derive the frozen counters from scanned item rows.

    ``items`` is a list of ``{'item_id', 'status', 'reason', 'placements'}``.
    ``placements`` is the number of canonical primary placements the item
    received; it is optional and defaults to 1 for eligible items so the
    *freeze* can run before placement exists (which is the whole point of
    freezing first).
    """
    seen = set()
    eligible = excluded = unresolved = missing = duplicate = 0
    for row in items:
        item_id = row.get('item_id')
        if not item_id: fail('SOURCE_ITEM_LEDGER_UNAVAILABLE', 'row without item_id')
        if item_id in seen: fail('DUPLICATE_PRIMARY_PLACEMENT', item_id + ':duplicate ledger row')
        seen.add(item_id)
        status = str(row.get('status') or '')
        if status == ELIGIBLE:
            eligible += 1
            placements = row.get('placements', 1)
            if placements == 0: missing += 1
            elif placements > 1: duplicate += 1
        elif status in UNRESOLVED_STATUSES:
            unresolved += 1
            if not str(row.get('reason') or '').strip(): fail('EXCLUSION_WITHOUT_REASON', item_id)
        else:
            excluded += 1
            if not str(row.get('reason') or '').strip(): fail('EXCLUSION_WITHOUT_REASON', item_id)
    return {'TOTAL_SCANNED': len(seen), 'ELIGIBLE_IN_SCOPE': eligible,
            'PLACED_UNIQUE': eligible - missing - duplicate,
            'EXCLUDED_WITH_REASON': excluded, 'UNRESOLVED_WITH_REASON': unresolved,
            'MISSING': missing, 'DUPLICATE_PRIMARY': duplicate}


# ---------------------------------------------------------------------------
# evidence readers
# ---------------------------------------------------------------------------

def _read_scope_status_ledger(evidence, repo_root):
    data = load(Path(repo_root) / evidence['path'])
    rows = data[evidence['records_key']]
    # A scanned item is identified by the declared key tuple, because a single
    # source question can legitimately contribute several scanned parts.
    keys = evidence.get('item_id_keys') or [evidence['item_id_key']]
    out = []
    for r in rows:
        item_id = '|'.join(str(r.get(k)) for k in keys)
        out.append({'item_id': item_id,
                    'status': r[evidence['status_key']],
                    'reason': r.get(evidence.get('reason_key', ''), '')})
    return out


def _read_handoff_manifest(evidence, repo_root):
    data = load(Path(repo_root) / evidence['path'])
    topics = {t['id']: t for t in data['topics']}
    topic = topics.get(evidence['topic_id'])
    if topic is None: fail('SOURCE_ITEM_LEDGER_UNAVAILABLE', evidence['topic_id'])
    return int(topic['retained_questions'])


def _read_handoff_validator(evidence, repo_root):
    """Read PR #346's independent per-topic expected counts out of its validator.

    This is a second, independently authored #346 artifact. Agreement between it
    and HANDOFF_MANIFEST.json is what makes the retained denominator evidence
    rather than a restated assertion.
    """
    text = (Path(repo_root) / evidence['path']).read_text(encoding='utf-8')
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == evidence.get('symbol', 'TOPICS') for t in node.targets):
            table = ast.literal_eval(node.value)
            if evidence['topic_id'] not in table:
                fail('SOURCE_ITEM_LEDGER_UNAVAILABLE', evidence['topic_id'] + ':validator')
            return int(table[evidence['topic_id']])
    fail('SOURCE_ITEM_LEDGER_UNAVAILABLE', evidence['path'] + ':symbol')


def derive_counters(instance, repo_root=REPO):
    """Re-derive an instance's counters from its declared evidence."""
    evidence = instance['evidence']
    path = Path(repo_root) / evidence['path']
    if not path.exists(): fail('INGESTION_EVIDENCE_DIGEST_MISMATCH', evidence['path'] + ':missing')
    if sha_file(path) != evidence['sha256']:
        fail('INGESTION_EVIDENCE_DIGEST_MISMATCH', evidence['path'])
    kind = evidence['kind']
    if kind == 'SCOPE_STATUS_LEDGER':
        return counters_from_items(_read_scope_status_ledger(evidence, repo_root)), []
    if kind == 'AUTHORING_HANDOFF_MANIFEST':
        retained = _read_handoff_manifest(evidence, repo_root)
        corroborating = instance.get('corroborating_evidence')
        if corroborating:
            cpath = Path(repo_root) / corroborating['path']
            if not cpath.exists() or sha_file(cpath) != corroborating['sha256']:
                fail('INGESTION_EVIDENCE_DIGEST_MISMATCH', corroborating['path'])
            if _read_handoff_validator(corroborating, repo_root) != retained:
                fail('SCANNED_TOTAL_RECONCILIATION_FAILURE', instance['instance_id'] + ':corroborating evidence')
        # #346 froze the retained denominator but never recorded the scanned
        # denominator or the exclusion count, so those stay unresolved. They are
        # never back-filled by inference.
        return ({'ELIGIBLE_IN_SCOPE': retained, 'PLACED_UNIQUE': retained,
                 'MISSING': 0, 'DUPLICATE_PRIMARY': 0},
                ['TOTAL_SCANNED', 'EXCLUDED_WITH_REASON', 'UNRESOLVED_WITH_REASON'])
    fail('SOURCE_ITEM_LEDGER_UNAVAILABLE', 'unknown evidence kind ' + str(kind))


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------

def validate_instance(instance, profile, repo_root=REPO):
    iid = instance['instance_id']
    state = instance['freeze_state']
    if state not in profile['freeze_states']: fail('SOURCE_DENOMINATOR_NOT_FROZEN', iid + ':' + str(state))
    if state == 'UNFROZEN': fail('SOURCE_DENOMINATOR_NOT_FROZEN', iid)
    derived, unresolved = derive_counters(instance, repo_root)
    if sorted(instance.get('unresolved_counters', [])) != sorted(unresolved):
        fail('SOURCE_ITEM_LEDGER_UNAVAILABLE', iid + ':unresolved counter set')
    frozen = instance['frozen_counters']
    for counter in profile['required_counters']:
        if counter in unresolved:
            if counter in frozen: fail('SOURCE_ITEM_LEDGER_UNAVAILABLE', iid + ':' + counter + ' claimed but unresolved')
            continue
        if counter not in frozen: fail('SOURCE_DENOMINATOR_NOT_FROZEN', iid + ':' + counter)
        if frozen[counter] != derived[counter]:
            fail('FROZEN_COUNTERS_NOT_DERIVED_FROM_EVIDENCE',
                 f'{iid}:{counter} frozen={frozen[counter]} derived={derived[counter]}')
    if frozen['ELIGIBLE_IN_SCOPE'] != frozen['PLACED_UNIQUE']: fail('ELIGIBLE_PLACED_MISMATCH', iid)
    if frozen['MISSING'] != 0: fail('MISSING_SOURCE_ITEM', iid)
    if frozen['DUPLICATE_PRIMARY'] != 0: fail('DUPLICATE_PRIMARY_PLACEMENT', iid)
    if 'TOTAL_SCANNED' not in unresolved:
        total = frozen['ELIGIBLE_IN_SCOPE'] + frozen['EXCLUDED_WITH_REASON'] + frozen['UNRESOLVED_WITH_REASON']
        if frozen['TOTAL_SCANNED'] != total:
            fail('SCANNED_TOTAL_RECONCILIATION_FAILURE',
                 f"{iid}: {frozen['TOTAL_SCANNED']} != {total}")
    if state == 'FROZEN_ITEM_LEDGER' and unresolved:
        fail('SOURCE_ITEM_LEDGER_UNAVAILABLE', iid + ':claims item ledger but counters unresolved')
    return derived


def validate_profile(profile, repo_root=REPO):
    if profile.get('subject') != 'CHEMISTRY': fail('SOURCE_DENOMINATOR_NOT_FROZEN', 'subject')
    if profile.get('stage') != 'SOURCE_INGESTION': fail('SOURCE_DENOMINATOR_NOT_FROZEN', 'stage')
    stored = profile.get('profile_digest', '')
    if stored and stored != digest(profile, 'profile_digest'):
        fail('INGESTION_EVIDENCE_DIGEST_MISMATCH', 'profile digest')
    ids = set()
    for instance in profile['frozen_instances']:
        if instance['instance_id'] in ids: fail('SOURCE_DENOMINATOR_NOT_FROZEN', 'duplicate instance id')
        ids.add(instance['instance_id'])
        validate_instance(instance, profile, repo_root)
    return True


def instance_by_id(profile, instance_id):
    for instance in profile['frozen_instances']:
        if instance['instance_id'] == instance_id: return instance
    fail('SOURCE_DENOMINATOR_NOT_FROZEN', str(instance_id) + ':not declared')


def assert_authoring_allowed(profile, instance_id, repo_root=REPO):
    """Gate the authoring phases on a frozen denominator.

    Called by PROBLEM_AUTHORING / INSTRUCTIONAL_AUTHORING in the generation
    contract: a scope whose denominator is not frozen to the profile's required
    level may not be authored against.
    """
    instance = instance_by_id(profile, instance_id)
    required = profile['authoring_requires_freeze_state']
    if instance['freeze_state'] not in required:
        fail('AUTHORING_BEFORE_DENOMINATOR_FREEZE',
             f"{instance_id}: freeze_state={instance['freeze_state']} required one of {sorted(required)}")
    validate_instance(instance, profile, repo_root)
    return True


def reconcile_with_closure(profile, closure, instance_id, repo_root=REPO):
    """Reconcile a frozen denominator against the live coverage closure.

    This is what makes freezing a pipeline stage rather than a document: the
    numbers frozen before authoring must still be the numbers the finished
    product reconciles to.
    """
    instance = instance_by_id(profile, instance_id)
    frozen = instance['frozen_counters']
    summary = closure['external_matrix']['summary']
    actual = {'TOTAL_SCANNED': summary['candidate_total'],
              'ELIGIBLE_IN_SCOPE': summary['eligible_total'],
              'PLACED_UNIQUE': summary['placed_unique_total'],
              'MISSING': summary['missing_total'],
              'DUPLICATE_PRIMARY': summary['duplicate_primary_total']}
    for counter, value in actual.items():
        if counter in instance.get('unresolved_counters', []): continue
        if frozen[counter] != value:
            fail('POST_AUTHORING_DENOMINATOR_DRIFT',
                 f'{instance_id}:{counter} frozen={frozen[counter]} realized={value}')
    if actual['MISSING']: fail('MISSING_SOURCE_ITEM', instance_id)
    if actual['DUPLICATE_PRIMARY']: fail('DUPLICATE_PRIMARY_PLACEMENT', instance_id)
    return True


def seal(profile_path=PROFILE_PATH):
    profile = load(profile_path)
    profile['profile_digest'] = ''
    profile['profile_digest'] = digest(profile, 'profile_digest')
    Path(profile_path).write_text(json.dumps(profile, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return profile['profile_digest']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--profile', default=str(PROFILE_PATH))
    ap.add_argument('--repo-root', default=str(REPO))
    ap.add_argument('--seal', action='store_true')
    a = ap.parse_args()
    if a.seal:
        print(json.dumps({'profile_digest': seal(a.profile)}, sort_keys=True)); return
    profile = load(a.profile)
    validate_profile(profile, a.repo_root)
    print(json.dumps({'profile_id': profile['profile_id'],
                      'frozen_instances': len(profile['frozen_instances']),
                      'status': 'PASS'}, sort_keys=True))


if __name__ == '__main__': main()
