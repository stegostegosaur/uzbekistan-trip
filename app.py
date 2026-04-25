import calendar
from dataclasses import dataclass
from datetime import date

import streamlit as st


@dataclass(frozen=True)
class DayPlan:
    title: str
    city: str
    weather: str
    schedule: list[str]
    accommodation: str | None = None
    accommodation_links: list[tuple[str, str]] | None = None
    notes: str | None = None


def _get_query_param_day() -> int | None:
    """Return ?day=<int> if present, else None.

    Supports both modern st.query_params and legacy experimental API.
    """

    try:
        qp = st.query_params  # type: ignore[attr-defined]
        raw = qp.get("day")
        if raw is None:
            return None
        # st.query_params may return str or list[str] depending on version.
        if isinstance(raw, list):
            raw = raw[0] if raw else None
        if raw is None:
            return None
        return int(raw)
    except Exception:
        try:
            qp = st.experimental_get_query_params()
            raw_list = qp.get("day")
            if not raw_list:
                return None
            return int(raw_list[0])
        except Exception:
            return None


def _set_query_param_day(day: int) -> None:
    """Set ?day=<int> (best-effort) without breaking on older Streamlit."""

    try:
        st.query_params["day"] = str(day)  # type: ignore[attr-defined]
    except Exception:
        try:
            st.experimental_set_query_params(day=str(day))
        except Exception:
            # If query params aren't supported, the app still works via default day.
            pass


def build_itinerary() -> dict[int, DayPlan]:
    """Sample itinerary (May 1-10, 2026)."""

    def gmaps_search(query: str) -> str:
        # Simple, stable links (no affiliate IDs).
        return f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    def web_search(query: str) -> str:
        return f"https://www.google.com/search?q={query.replace(' ', '+')}"

    return {
        1: DayPlan(
            title="Warsaw → Tashkent (arrival after midnight)",
            city="Tashkent",
            weather=(
                "Typical early-May: mild to warm evenings; pack layers. "
                "(Forecast placeholder — add live API later if needed.)"
            ),
            schedule=[
                "15:55 — Flight Warsaw → Tashkent (LOT Polish Airlines)",
                "Flight: LO189 • Economy • Duration: 5h 55m",
                "00:50 (May 2) — Arrive in Tashkent",
                "Take a cab to accommodation; check-in / late arrival",
            ],
            accommodation="National Hostel in Tashkent (requested late checkout)",
            accommodation_links=[
                ("Maps: National Hostel Tashkent", gmaps_search("National Hostel Tashkent")),
                ("Web search", web_search("National Hostel Tashkent")),
            ],
            notes="Consider buying a local SIM at/near the airport if open at arrival time.",
        ),
        2: DayPlan(
            title="Tashkent day + night train to Urgench",
            city="Tashkent",
            weather=(
                "Typical early-May: warm daytime, cooler night. "
                "(Forecast placeholder.)"
            ),
            schedule=[
                "Check-out from National Hostel (store luggage if needed)",
                "Day in Tashkent: easy walking + metro sightseeing",
                "Evening: food + last-minute supplies for the west",
                "21:45 — Tashkent Yuzhniy → Urgench (overnight train)",
            ],
            accommodation=None,
            accommodation_links=[],
            notes="Keep passport handy for train checks; arrive early to the station.",
        ),
        3: DayPlan(
            title="Urgench → Nukus",
            city="Urgench / Nukus",
            weather=(
                "Khorezm + Karakalpakstan in May can be sunny and dry; "
                "windy evenings are possible. (Forecast placeholder.)"
            ),
            schedule=[
                "10:57 — Arrive in Urgench",
                "Urgench feels quiet; keep it brief (rest + lunch)",
                "Plan car transfer to Nukus during the day (≈ 3 hours)",
                "Check-in: NUKUS GUEST HOUSE (possibly late arrival)",
            ],
            accommodation="NUKUS GUEST HOUSE in Nukus",
            accommodation_links=[
                ("Maps: Nukus Guest House", gmaps_search("NUKUS GUEST HOUSE Nukus")),
                ("Web search", web_search("NUKUS GUEST HOUSE Nukus")),
            ],
            notes="Confirm driver and price in advance; carry water/snacks for the road.",
        ),
        4: DayPlan(
            title="Roadtrip west — Day 1",
            city="Nukus → western route",
            weather=(
                "Likely dry; strong sun possible. Bring sunscreen + hat. "
                "(Forecast placeholder.)"
            ),
            schedule=[
                "Check-out from NUKUS GUEST HOUSE",
                "Start Day 1 of the western roadtrip",
                "Stops depend on route/permits; keep buffer time",
                "Evening: settle in (location depends on roadtrip progress)",
            ],
            notes="Offline maps + extra water are strongly recommended for remote stretches.",
        ),
        5: DayPlan(
            title="Roadtrip west — Day 2 (overnight still unconfirmed)",
            city="Western route → Nukus or Khiva (TBD)",
            weather="Dry and warm is common; dust/wind possible. (Forecast placeholder.)",
            schedule=[
                "Continue Day 2 of the western roadtrip",
                "Arrive to Nukus or Khiva (overnight STILL UNCONFIRMED)",
                "If finishing in Khiva: evening walk in/near Itchan Kala",
            ],
            notes="Decide overnight city by midday to avoid last-minute accommodation stress.",
        ),
        6: DayPlan(
            title="Khiva → Bukhara (evening train)",
            city="Khiva / Bukhara",
            weather=(
                "Bukhara in May: warm afternoons; cooler at night. "
                "(Forecast placeholder.)"
            ),
            schedule=[
                "Day in/around Khiva (finish sights + food)",
                "~18:00 — Train Khiva → Bukhara",
                "Check-in: Dervish Hostel in Bukhara",
            ],
            accommodation="Dervish Hostel in Bukhara",
            accommodation_links=[
                ("Maps: Dervish Hostel Bukhara", gmaps_search("Dervish Hostel Bukhara")),
                ("Web search", web_search("Dervish Hostel Bukhara")),
            ],
            notes="Verify exact train time + station; keep ticket screenshots offline.",
        ),
        7: DayPlan(
            title="Bukhara → Samarkand",
            city="Bukhara / Samarkand",
            weather=(
                "Samarkand in May: usually pleasant for walking, "
                "but midday sun can be strong. (Forecast placeholder.)"
            ),
            schedule=[
                "Check-out from Dervish Hostel",
                "Train to Samarkand",
                "Check-in: Imran&Bek in Samarkand",
                "Evening: short walk + early night",
            ],
            accommodation="Imran&Bek in Samarkand",
            accommodation_links=[
                ("Maps: Imran&Bek Samarkand", gmaps_search("Imran&Bek Samarkand")),
                ("Web search", web_search("Imran&Bek Samarkand")),
            ],
        ),
        8: DayPlan(
            title="Samarkand full day",
            city="Samarkand",
            weather="Comfortable mornings; warm afternoons. (Forecast placeholder.)",
            schedule=[
                "Stay at Imran&Bek",
                "Buffer day for Registan / Shah-i-Zinda / local food",
                "Optional: museum time + sunset viewpoint",
            ],
            accommodation="Imran&Bek in Samarkand",
            accommodation_links=[
                ("Maps: Imran&Bek Samarkand", gmaps_search("Imran&Bek Samarkand")),
            ],
        ),
        9: DayPlan(
            title="Samarkand → Tashkent (midday arrival)",
            city="Samarkand / Tashkent",
            weather="Likely warm; stay hydrated. (Forecast placeholder.)",
            schedule=[
                "Check-out from Imran&Bek",
                "Train to Tashkent",
                "Arrive Passazhirskiy at 12:01",
                "Prepare for very early flight (night logistics)",
            ],
            notes="Decide whether to book a short nap hotel or use airport lounge if available.",
        ),
        10: DayPlan(
            title="Fly home",
            city="Tashkent → home",
            weather="Night/early morning departure; bring a warm layer. (Forecast placeholder.)",
            schedule=[
                "03:35 — Flight back",
                "Leave plenty of time for airport transfer + check-in",
            ],
        ),
    }


def calendar_html(year: int, month: int, clickable_days: set[int], selected_day: int | None) -> str:
    """Render a month view calendar as HTML with clickable day links."""

    cal = calendar.Calendar(firstweekday=0)  # Monday
    month_days = list(cal.itermonthdays(year, month))

    weekday_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_cells: list[str] = []
    for d in month_days:
        if d == 0:
            day_cells.append('<div class="day empty"></div>')
            continue

        classes = ["day"]
        is_clickable = d in clickable_days
        if is_clickable:
            classes.append("clickable")
            classes.append("highlight")
        if selected_day is not None and d == selected_day:
            classes.append("selected")

        class_attr = " ".join(classes)
        if is_clickable:
            # Streamlit sets a page-wide base target that opens links in a new tab.
            # Force same-tab navigation for intra-app day selection.
            day_cells.append(
                f'<a class="{class_attr}" href="?day={d}" target="_self" role="button" aria-label="Select day {d}">{d}</a>'
            )
        else:
            day_cells.append(f'<span class="{class_attr}">{d}</span>')

    weekday_header = "".join(f'<div class="weekday">{w}</div>' for w in weekday_labels)
    days_grid = "".join(day_cells)
    month_label = date(year, month, 1).strftime("%B %Y")

    return f"""
    <div class="calendar-wrap">
      <div class="month-title">{month_label}</div>
      <div class="calendar">
        {weekday_header}
        {days_grid}
      </div>
    </div>
    """.strip()


def main() -> None:
    st.set_page_config(page_title="Uzbekistan itinerary", layout="wide")
    st.title("Uzbekistan trip 1-10 May 2026 itinerary")

    itinerary = build_itinerary()
    clickable_days = set(itinerary.keys())

    # Establish selected day from query param (preferred) and store in session state.
    qp_day = _get_query_param_day()
    if "selected_day" not in st.session_state:
        st.session_state.selected_day = 1
    if qp_day in clickable_days and qp_day != st.session_state.selected_day:
        st.session_state.selected_day = qp_day

    selected_day: int = int(st.session_state.selected_day)
    if selected_day not in clickable_days:
        selected_day = 1
        st.session_state.selected_day = 1
        _set_query_param_day(1)

    st.markdown(
        """
        <style>
          .calendar-wrap { max-width: 820px; }
          .month-title { font-size: 1.2rem; font-weight: 700; margin: 0.25rem 0 0.75rem 0; }
          .calendar {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.45rem;
            align-items: stretch;
          }
          .weekday {
            font-size: 0.85rem;
            color: #6b7280;
            text-align: center;
            padding: 0.15rem 0;
          }
          .day {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 44px;
            border-radius: 10px;
            border: 1px solid rgba(0,0,0,0.08);
            background: rgba(0,0,0,0.02);
            text-decoration: none;
            color: inherit;
            user-select: none;
          }
          .day.empty {
            border: 1px dashed rgba(0,0,0,0.06);
            background: transparent;
          }
          .day.highlight {
            background: rgba(59, 130, 246, 0.10);
            border-color: rgba(59, 130, 246, 0.35);
            font-weight: 600;
          }
          .day.clickable:hover {
            background: rgba(59, 130, 246, 0.18);
            border-color: rgba(59, 130, 246, 0.55);
          }
          .day.selected {
            background: rgba(16, 185, 129, 0.18);
            border-color: rgba(16, 185, 129, 0.55);
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.15) inset;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.1, 1.4], gap="large")
    with left:
        st.subheader("Calendar")
        st.markdown(
            calendar_html(
                year=2026,
                month=5,
                clickable_days=clickable_days,
                selected_day=selected_day,
            ),
            unsafe_allow_html=True,
        )
        st.caption("Only May 1–10 are interactive; other days are shown for context.")

        # Optional quick-jump for accessibility.
        day_choice = st.selectbox(
            "Jump to day",
            options=sorted(clickable_days),
            index=sorted(clickable_days).index(selected_day),
        )
        if day_choice != selected_day:
            st.session_state.selected_day = int(day_choice)
            _set_query_param_day(int(day_choice))
            st.rerun()

    with right:
        plan = itinerary[selected_day]
        st.subheader(f"May {selected_day}, 2026")
        st.markdown(f"**{plan.title}**")
        st.markdown(f"**City / region:** {plan.city}")

        st.markdown("**Weather (placeholder):**")
        st.write(plan.weather)

        st.markdown("**Schedule:**")
        for item in plan.schedule:
            st.markdown(f"- {item}")

        if plan.accommodation:
            st.markdown("**Accommodation:**")
            st.write(plan.accommodation)

        links = plan.accommodation_links or []
        if links:
            st.markdown("**Links:**")
            for label, url in links:
                st.markdown(f"- [{label}]({url})")

        if plan.notes:
            st.markdown("**Notes:**")
            st.info(plan.notes)


if __name__ == "__main__":
    main()
