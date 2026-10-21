"""Structural, NOT factual, audit of v1.0 ABC research output; synthetic tests only."""
import json
import re
import sys
from pathlib import Path

HEADERS = ('A.', 'B.', 'C.')

def audit(item):
    errors=[]; holds=[]
    txt=item.get('answer_text','')
    positions=[('\n'+txt).find('\n## '+h) for h in HEADERS]
    if any(v<0 for v in positions) or positions != sorted(positions):
        errors.append('ABC_DISPLAY_ORDER_OR_MISSING')
    if not item.get('value_chain',{}).get('simple_product_explanations'):
        errors.append('NO_SIMPLE_VALUE_CHAIN')
    if not item.get('value_chain',{}).get('separate_axes'):
        errors.append('CLASSIFICATION_AXES_CONFLATED_OR_UNAUDITED')
    groups=item.get('peer_groups',[])
    if not groups or not any(len(g.get('firms',[])) >= 2 for g in groups):
        errors.append('NO_REAL_PEER_COMPARISON')
    if not any(g.get('economic_difference') for g in groups):
        errors.append('NO_FIRM_ECONOMIC_DIFFERENCES')
    for g in groups:
        for firm in g.get('firms',[]):
            fid=firm.get('name','UNKNOWN')
            if not firm.get('actual_product') or not firm.get('business_role'):
                errors.append('NO_PRODUCT_ROLE:'+fid)
            for seg in firm.get('segments',[]):
                if seg.get('share') is not None:
                    if not (seg.get('denominator') and seg.get('period') and seg.get('source_id')):
                        errors.append('UNGROUNDED_SEGMENT_SHARE:'+fid)
                    if seg.get('basis') not in ('OFFICIAL','ANALYST_ESTIMATE'):
                        errors.append('SEGMENT_SHARE_BASIS_MISSING:'+fid)
                elif seg.get('disclosure') not in ('NOT_DISCLOSED','UNKNOWN'):
                    holds.append('SEGMENT_VALUE_UNRESOLVED:'+fid)
    frontier=item.get('source_frontier',[])
    if not frontier or not any(x.get('seed_origin')=='ROLE_SEARCH' for x in frontier):
        errors.append('NO_INDEPENDENT_SECTOR_SOURCE_DISCOVERY')
    kinds={x.get('source_kind') for x in frontier if x.get('discovery_status')=='FOUND'}
    if len(kinds)<2:
        holds.append('SOURCE_FAMILY_CONCENTRATION')
    if item.get('foreign_material_supply_region'):
        region=item['foreign_material_supply_region']
        if not any(x.get('geography')==region and x.get('search_language') not in ('ko','en','') for x in frontier):
            errors.append('FOREIGN_NATIVE_LANGUAGE_DISCOVERY_MISSING:'+region)
    if not item.get('themes'):
        errors.append('NO_THEMATIC_TRANSMISSION')
    return sorted(set(errors)),sorted(set(holds))

if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: python scripts/audit_output_v10.py delivery.json');sys.exit(2)
    data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    errs,holds=audit(data)
    print(json.dumps({'structural_errors':errs,'review_holds':holds},ensure_ascii=False,indent=2))
    sys.exit(bool(errs))
