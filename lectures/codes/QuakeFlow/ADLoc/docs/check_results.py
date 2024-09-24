# %%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# %%
true_events = pd.read_csv("stanford/true_event.csv")
# pred_events = pd.read_csv("results/stanford/adloc_events.csv")
# pred_events = pd.read_csv("results/stanford/adloc_events_sst.csv")
# pred_events = pd.read_csv("results/stanford/adloc_events_grid_search.csv")
pred_events = pd.read_csv("results/stanford/adloc_dd_events.csv")
# pred_events = pd.read_csv("results/stanford/ransac_events_sst.csv")

# %%
true_events["event_index"] = np.arange(1, len(true_events) + 1)
true_events.rename({"Lat": "latitude", "Lon": "longitude", "Dep": "depth_km"}, axis=1, inplace=True)

# %%
true_events.set_index("event_index", inplace=True)
pred_events.set_index("event_index", inplace=True)

# %%
s = 5
fig, ax = plt.subplots(2, 2, figsize=(15, 12), gridspec_kw={"width_ratios": [1, 1], "height_ratios": [1, 0.5]})

# ax[0, 0].scatter(true_events["longitude"], true_events["latitude"], c=true_events["depth_km"], s=s, label="True events")
ax[0, 0].scatter(
    pred_events["longitude"],
    pred_events["latitude"],
    c=pred_events["depth_km"],
    s=s,
    label="Predicted events",
    vmin=0,
    vmax=15,
    cmap="viridis_r",
)
ax[0, 0].set_title(f"{len(true_events)} true events and {len(pred_events)} predicted events")

ax[0, 1].scatter(true_events["longitude"], true_events["latitude"], c="r", s=s, label="True events")
ax[0, 1].scatter(pred_events["longitude"], pred_events["latitude"], c="b", s=s, label="Predicted events")
for i in true_events.index:
    if i in pred_events.index:
        ax[0, 1].plot(
            [true_events.loc[i, "longitude"], pred_events.loc[i, "longitude"]],
            [true_events.loc[i, "latitude"], pred_events.loc[i, "latitude"]],
            "k--",
            linewidth=0.5,
            alpha=0.5,
        )
    else:
        ax[0, 1].plot(
            true_events.loc[i, "longitude"],
            true_events.loc[i, "latitude"],
            "rx",
            markersize=5,
            alpha=0.5,
        )

ax[1, 0].scatter(true_events["longitude"], true_events["depth_km"], c="r", s=s, label="True events")
ax[1, 0].scatter(pred_events["longitude"], pred_events["depth_km"], c="b", s=s, label="Predicted events")
for i in true_events.index:
    if i in pred_events.index:
        ax[1, 0].plot(
            [true_events.loc[i, "longitude"], pred_events.loc[i, "longitude"]],
            [true_events.loc[i, "depth_km"], pred_events.loc[i, "depth_km"]],
            "k--",
            linewidth=0.5,
            alpha=0.5,
        )
    else:
        ax[1, 0].plot(
            true_events.loc[i, "longitude"],
            true_events.loc[i, "depth_km"],
            "rx",
            markersize=5,
            alpha=0.5,
        )
ax[1, 0].set_ylim([15, 0])


ax[1, 1].scatter(true_events["latitude"], true_events["depth_km"], c="r", s=s, label="True events")
ax[1, 1].scatter(pred_events["latitude"], pred_events["depth_km"], c="b", s=s, label="Predicted events")
for i in true_events.index:
    if i in pred_events.index:
        ax[1, 1].plot(
            [true_events.loc[i, "latitude"], pred_events.loc[i, "latitude"]],
            [true_events.loc[i, "depth_km"], pred_events.loc[i, "depth_km"]],
            "k--",
            linewidth=0.5,
            alpha=0.5,
        )
    else:
        ax[1, 1].plot(
            true_events.loc[i, "latitude"],
            true_events.loc[i, "depth_km"],
            "rx",
            markersize=5,
            alpha=0.5,
        )
ax[1, 1].set_ylim([15, 0])

# %%
km2deg = 1 / 111.32

if (
    ("sigma_x_km" in pred_events.columns)
    and ("sigma_y_km" in pred_events.columns)
    and ("sigma_z_km" in pred_events.columns)
):
    # plot error larger than median
    idx = (
        (pred_events["sigma_x_km"] > pred_events["sigma_x_km"].median())
        | (pred_events["sigma_y_km"] > pred_events["sigma_y_km"].median())
        | (pred_events["sigma_z_km"] > pred_events["sigma_z_km"].median())
    )
    fig, ax = plt.subplots(2, 2, figsize=(15, 12), gridspec_kw={"width_ratios": [1, 1], "height_ratios": [1, 0.5]})
    ax[0, 0].errorbar(
        pred_events["longitude"],
        pred_events["latitude"],
        xerr=pred_events["sigma_x_km"] * km2deg,
        yerr=pred_events["sigma_y_km"] * km2deg,
        fmt="none",
        c="k",
        alpha=0.5,
    )

    ax[0, 1].errorbar(
        pred_events[idx]["longitude"],
        pred_events[idx]["latitude"],
        xerr=pred_events[idx]["sigma_x_km"] * km2deg,
        yerr=pred_events[idx]["sigma_y_km"] * km2deg,
        fmt="none",
        c="k",
        alpha=0.5,
    )

    ax[1, 0].errorbar(
        pred_events[idx]["longitude"],
        pred_events[idx]["depth_km"],
        xerr=pred_events[idx]["sigma_x_km"] * km2deg,
        yerr=pred_events[idx]["sigma_z_km"],
        fmt="none",
        c="k",
        alpha=0.5,
    )

    ax[1, 1].errorbar(
        pred_events[idx]["latitude"],
        pred_events[idx]["depth_km"],
        xerr=pred_events[idx]["sigma_y_km"] * km2deg,
        yerr=pred_events[idx]["sigma_z_km"],
        fmt="none",
        c="k",
        alpha=0.5,
    )

    ax[1, 0].set_ylim([15, 0])
    ax[1, 1].set_ylim([15, 0])

    plt.show()

# %%
