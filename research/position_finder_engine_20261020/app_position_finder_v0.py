"""Streamlit research UI for the non-legacy stock-position finder v0.

Run locally:
    streamlit run position_finder_app_v0.py
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from leader_gate_v0 import GateInput, evaluate_leader_gate
from position_finder_core import historical_stage_references, named_layout_ranges, classify_price


# Keep v0 self-contained: a refetch must be an explicit, versioned research
# action rather than an unrecorded network dependency at runtime.
DEFAULT_STAGE_PATH = BASE_DIR / "data" / "historical_stage_reference_legacy38_v0.csv"
DEFAULT_LAYOUT_PATH = BASE_DIR / "data" / "screen_relative_layout_prior_v0.csv"


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def checkbox_or_unknown(label: str, help_text: str) -> bool | None:
    value = st.selectbox(label, ["��Ȯ��", "��", "�ƴϿ�"], help=help_text)
    return {"��Ȯ��": None, "��": True, "�ƴϿ�": False}[value]


def main() -> None:
    st.set_page_config(page_title="�ְ���ġŽ���� v0", layout="wide")
    st.title("�ְ���ġŽ���� v0 ? ������ ���� ��� Ž����")
    st.caption("���� �������̷� ���� �Է� ����, ���� 5��7 ������ ���� ȭ�� ����ġ�� �и� ǥ���մϴ�.")

    with st.sidebar:
        st.header("1. ���� ����Ŭ �Է�")
        ticker = st.text_input("�����ڵ�", value="000660")
        cycle_low = st.number_input("Ȯ���� ����Ŭ ���� �Ǵ� ���� ��Ŀ", min_value=0.01, value=100000.0)
        current_price = st.number_input("���簡", min_value=0.01, value=150000.0)
        st.caption("���������� ��Ŀ�� ��� ������ Ȯ�� ������ ���� �Է��մϴ�.")

        st.header("2. LeaderGate")
        base_breakout = checkbox_or_unknown("�ڽ�/������ ����", "��� �̵���� ���� ��Ģ�� �ƴ� ���ݱ��� ����")
        breakout_hold = checkbox_or_unknown("���� �� ���� Ȯ��", "���� ���� ������ ��ȣ�� ���ϰ� ���")
        turnover = checkbox_or_unknown("�ŷ���ݡ��ŷ��� Ȯ��", "���� ������ ���� ���� ��� Ȯ��")
        peers = checkbox_or_unknown("���� ���� ����", "���� �ֵ� �ĺ��� ���� �ʱ� ��ȣ�� �ִ°�")
        earnings = st.selectbox("EPS/���� ����", ["unknown", "accelerating", "turnaround", "flat", "deteriorating"])
        valuation = st.selectbox("��� �ƶ�", ["unknown", "supported", "stretched"])
        post_top = checkbox_or_unknown("1�� �������޶� ���� ����", "���� �ű� ���� �ؼ��� �ߴ�")

    try:
        stage_data = load_csv(DEFAULT_STAGE_PATH)
        layout_data = load_csv(DEFAULT_LAYOUT_PATH)
    except Exception as exc:  # UI should remain usable even if remote source is unavailable.
        st.error(f"���� CSV�� �ҷ����� ���߽��ϴ�: {exc}")
        return

    gate = evaluate_leader_gate(
        GateInput(base_breakout, breakout_hold, turnover, peers, earnings, valuation, post_top)
    )
    left, right = st.columns((1, 2))
    with left:
        st.subheader("�ֵ��ּ� ����Ʈ")
        status_color = {
            "confirmed": "??",
            "candidate": "??",
            "rejected": "??",
            "unknown": "?",
        }[gate.status]
        st.metric("����", f"{status_color} {gate.status}")
        st.metric("���� ������", f"{gate.evidence_coverage_pct}%")
        st.write("**Ȯ�ε� �ٰ�**")
        st.write(list(gate.reasons) or ["����"])
        st.write("**���������**")
        st.write(list(gate.warnings) or ["����"])
    with right:
        st.subheader("������ 5��7��� ���� ����")
        cohort = st.selectbox("���� ��ȣƮ", sorted(stage_data["sample_origin"].dropna().unique()))
        subset = stage_data[(stage_data["sample_origin"] == cohort) & (stage_data["weighting"] == "cycle_equal")]
        st.warning(
            "This v0 bundle contains only LEGACY38 selected-sample calibration. "
            "It is a temporary reference, not the rebuilt all-leader universe "
            "or an original-formula coefficient."
        )
        tabs = st.tabs(["�α� 5���", "�α� 7���"])
        for tab, k in zip(tabs, (5, 7)):
            with tab:
                references = historical_stage_references(subset.to_dict("records"), cycle_low, k)
                table = pd.DataFrame(
                    [
                        {"stage": item.stage, "p25": round(item.low, 0), "median": round(item.median, 0), "p75": round(item.high, 0)}
                        for item in references
                    ]
                )
                st.dataframe(table, use_container_width=True, hide_index=True)
                st.caption("�Ϸ�� ���� �ֵ��ֿ����� ����� ���� �����Դϴ�. ���� ������ �̷� ���� �������� �ƴմϴ�.")

    st.divider()
    st.subheader("���� ��Ʈ���� ������ ���� ��� ��ġ ? ���Ǻ� ǥ��")
    st.caption("�Ʒ��� ȭ��� �����ǥ ���������Դϴ�. ���� ��Ʈ�� �������� �α׷� ����ǰ�, ���������� ��Ŀ�� ���������� Ȯ�ε� ��쿡�� ��ȭ ������ ��ȯ�մϴ�.")
    observed_anchors = st.checkbox("������ ���������� ��Ŀ�� �ִ�", value=False)
    axis_scale = st.selectbox("Audited chart price-axis", ["unknown", "linear", "log"])
    if observed_anchors and axis_scale == "unknown":
        st.warning("Price conversion is blocked until the source chart axis is audited as linear or log.")
    if observed_anchors and axis_scale != "unknown":
        col1, col2 = st.columns(2)
        with col1:
            knee_price = st.number_input("������ ���� ����", min_value=0.01, value=cycle_low)
        with col2:
            top_price = st.number_input("������ ���� ����", min_value=0.01, value=cycle_low * 3)
        q_ranges = {
            row.band: (float(row.q_low), float(row.q_median), float(row.q_high))
            for row in layout_data.itertuples(index=False)
        }
        try:
            bands = named_layout_ranges(knee_price, top_price, q_ranges, axis_scale=axis_scale)
            band_table = pd.DataFrame(
                [{"band": item.band, "low": round(item.low, 0), "median": round(item.median, 0), "high": round(item.high, 0)} for item in bands]
            ).sort_values("median")
            st.dataframe(band_table, use_container_width=True, hide_index=True)
            st.metric("���� ��ġ (���Ǻ�)", classify_price(current_price, bands))
        except ValueError as exc:
            st.warning(str(exc))
    elif not observed_anchors:
        st.info("���� ��Ŀ�� ���Ƿ� ���� �ʽ��ϴ�. ��ġ�� ����ġ �ڷ�� �����ϵ�, ���簡�� ���� ��ǥ���� ��ȯ���� �ʽ��ϴ�.")

    st.divider()
    st.caption(f"�Է� ����: {ticker}. �� ȭ���� ������ v0�̸� �Ÿ� ��õ������ ���� �߰� ������ �ƴմϴ�.")


if __name__ == "__main__":
    main()

