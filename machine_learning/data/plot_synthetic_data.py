import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

should_show = "--no-show" not in sys.argv


def load_synthetic_data(csv_path: str = "synthetic_plotting_data.csv") -> pd.DataFrame:
    """Wczytaj wygenerowane dane syntetyczne przygotowane do wykresów."""
    return pd.read_csv(csv_path)


def plot_pension_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Generuje histogram rozkładu emerytury urealnionej z dodatkowymi informacjami w hover.
    """
    # Przedziały emerytury zgodne ze statystykami
    pension_bins = [0, 2800, 3000, 3200, 3400, 3600, float("inf")]
    pension_labels = [
        "do 2800 zł",
        "2800-3000 zł",
        "3000-3200 zł",
        "3200-3400 zł",
        "3400-3600 zł",
        "powyżej 3600 zł",
    ]
    expected_percentages = [
        38.4,
        7.0,
        6.5,
        5.8,
        5.1,
        37.2,
    ]  # ostatnia kategoria = pozostałe

    # Kategoryzacja emerytury
    df["emerytura_kategoria"] = pd.cut(
        df["emerytura_urealniona"],
        bins=pension_bins,
        labels=pension_labels,
        include_lowest=True,
    )

    # Oblicz rzeczywiste rozkłady
    pension_counts = df["emerytura_kategoria"].value_counts().sort_index()
    pension_percentages = (pension_counts / len(df) * 100).round(1)

    # Przygotuj dane do histogramu
    histogram_data = []
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"]

    for i, (category, count) in enumerate(pension_counts.items()):
        percentage = pension_percentages[category]
        expected_pct = expected_percentages[i] if i < len(expected_percentages) else 0

        histogram_data.append(
            {
                "category": category,
                "count": count,
                "percentage": percentage,
                "expected_percentage": expected_pct,
                "color": colors[i % len(colors)],
            }
        )

    # Stwórz histogram
    fig = go.Figure()

    for data in histogram_data:
        fig.add_trace(
            go.Bar(
                x=[data["category"]],
                y=[data["count"]],
                name=data["category"],
                marker_color=data["color"],
                hovertemplate=(
                    f"<b>{data['category']}</b><br>"
                    f"Liczba przypadków: {data['count']}<br>"
                    f"Odsetek w danych: {data['percentage']}%<br>"
                    f"Oczekiwany odsetek: {data['expected_percentage']}%<br>"
                    f"Różnica: {data['percentage'] - data['expected_percentage']:+.1f} p.p."
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

    # Dodaj informacje o średniej i medianie
    mean_pension = df["emerytura_urealniona"].mean()
    median_pension = df["emerytura_urealniona"].median()

    fig.add_annotation(
        x=0.02,
        y=0.98,
        xref="paper",
        yref="paper",
        text=f"Średnia: {mean_pension:.0f} PLN<br>Mediana: {median_pension:.0f} PLN",
        showarrow=False,
        bgcolor="white",
        bordercolor="black",
        borderwidth=1,
    )

    # Dostosowanie layoutu
    fig.update_layout(
        xaxis_title="Przedziały emerytury",
        yaxis_title="Liczba przypadków",
        height=600,
        hovermode='closest',
        xaxis={'categoryorder': 'array', 'categoryarray': pension_labels},
        showlegend=False,
        margin=dict(t=20, b=40, l=40, r=20)
    )
    
    # Usuń kontrolki plotly
    config = {'displayModeBar': False}
    fig.update_layout(dragmode=False)
    
    return fig


def plot_pension_by_gender(df: pd.DataFrame) -> go.Figure:
    """
    Porównanie rozkładu emerytury według płci.
    """
    fig = px.histogram(
        df,
        x="emerytura_urealniona",
        color="plec",
        nbins=25,
        labels={
            "emerytura_urealniona": "Emerytura urealniona (PLN)",
            "count": "Liczba przypadków",
            "plec": "Płeć",
        },
        color_discrete_map={"k": "pink", "m": "lightblue"},
    )

    fig.update_layout(
        xaxis_title="Emerytura urealniona (PLN)",
        yaxis_title="Liczba przypadków",
        height=600,
        barmode='overlay',
        margin=dict(t=20, b=40, l=40, r=20),
        dragmode=False
    )

    fig.update_traces(opacity=0.7)

    return fig


def plot_salary_vs_pension(df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot: wynagrodzenie vs emerytura z dodatkowymi informacjami.
    """
    fig = px.scatter(
        df,
        x="wynagrodzenie_brutto",
        y="emerytura_urealniona",
        color="plec",
        hover_data={
            "rok_rozpoczecia": True,
            "rok_zakonczenia": True,
            "absence": True,
            "stopa_zastapienia": ":.2%",
        },
        labels={
            "wynagrodzenie_brutto": "Wynagrodzenie brutto (PLN)",
            "emerytura_urealniona": "Emerytura urealniona (PLN)",
            "plec": "Płeć",
        },
        color_discrete_map={"k": "pink", "m": "lightblue"},
    )
    
    fig.update_layout(
        height=600,
        margin=dict(t=20, b=40, l=40, r=20),
        dragmode=False
    )
    
    return fig


def create_dashboard(df: pd.DataFrame) -> go.Figure:
    """
    Tworzy dashboard z wieloma wykresami.
    """
    # Subplots
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Histogram emerytury urealnionej",
            "Emerytura według płci",
            "Wynagrodzenie vs Emerytura",
            "Statystyki podstawowe",
        ),
        specs=[[{"type": "xy"}, {"type": "xy"}], [{"type": "xy"}, {"type": "table"}]],
    )

    # Histogram główny
    hist_data = df["emerytura_urealniona"]
    fig.add_trace(go.Histogram(x=hist_data, nbinsx=30, name="Wszystkie"), row=1, col=1)

    # Histogram według płci
    for plec, color in [("k", "pink"), ("m", "lightblue")]:
        data = df[df["plec"] == plec]["emerytura_urealniona"]
        fig.add_trace(
            go.Histogram(
                x=data, nbinsx=25, name=f"Płeć: {plec}", marker_color=color, opacity=0.7
            ),
            row=1,
            col=2,
        )

    # Scatter plot
    fig.add_trace(
        go.Scatter(
            x=df["wynagrodzenie_brutto"],
            y=df["emerytura_urealniona"],
            mode="markers",
            marker=dict(
                color=df["plec"].map({"k": "pink", "m": "lightblue"}),
                size=8,
                opacity=0.7,
            ),
            name="Wynagrodzenie vs Emerytura",
        ),
        row=2,
        col=1,
    )

    # Tabela statystyk
    stats = df["emerytura_urealniona"].describe()
    fig.add_trace(
        go.Table(
            header=dict(values=["Statystyka", "Wartość (PLN)"]),
            cells=dict(
                values=[
                    ["Średnia", "Mediana", "Min", "Max", "Odchylenie std."],
                    [
                        f"{stats['mean']:.0f}",
                        f"{stats['50%']:.0f}",
                        f"{stats['min']:.0f}",
                        f"{stats['max']:.0f}",
                        f"{stats['std']:.0f}",
                    ],
                ]
            ),
        ),
        row=2,
        col=2,
    )
    
    fig.update_layout(
        height=800,
        margin=dict(t=20, b=40, l=40, r=20),
        dragmode=False
    )
    
    return fig


if __name__ == "__main__":
    # Wczytaj dane
    df = load_synthetic_data()

    print(f"Wczytano {len(df)} rekordów")
    print(f"Kolumny: {list(df.columns)}")

    # Generuj wykresy
    config = {
        'displayModeBar': False,
        'staticPlot': False,
        'scrollZoom': False,
        'doubleClick': False,
        'showTips': False,
        'displaylogo': False,
        'watermark': False
    }
    fig1 = plot_pension_distribution(df)

    fig2 = plot_pension_by_gender(df)
    
    fig3 = plot_salary_vs_pension(df)
    
    # Dashboard
    dashboard = create_dashboard(df)
    dashboard.show(config=config)
    
    # Zapisz wykresy do HTML

    dashboard.write_html("pension_dashboard.html", config=config)
    
    print("Wykresy zapisane do plików HTML")
