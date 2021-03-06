import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

(
    JMCSR_AnyGl_RS,
    JMCSR_AnyGl_SS,
    JMCSR_Any_RS,
    JMCSR_Any_SS,
    JMCSR_all,
    JMCSR_AnyGl,
    JMCSR_Any,
) = (
    pd.read_csv("./data/combined/JMCSR_AnyGl_RS.csv"),
    pd.read_csv("./data/combined/JMCSR_AnyGl_SS.csv"),
    pd.read_csv("./data/combined/JMCSR_Any_RS.csv"),
    pd.read_csv("./data/combined/JMCSR_Any_SS.csv"),
    pd.read_csv("./data/combined/JMCSR_all.csv"),
    pd.read_csv("./data/combined/JMCSR_AnyGl.csv"),
    pd.read_csv("./data/combined/JMCSR_Any.csv"),
)

# Once the data is gotten the columns are not in the right data type so this changes them to it
def convert_to_units(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df["Real time"] = pd.to_timedelta(df["Real time"])
    df["In-game time"] = pd.to_timedelta(df["In-game time"])


# Make a bunch of sample data. Boolean testing and plot the means
def bootstrap_test(df, n=1000):
    convert_to_units(df)
    return [
        int(
            (
                (df.sample(n=df.iloc[:, 0].size, replace=True))["Real time"].mean()
            ).to_timedelta64()
        )
        / 60000000000
        for i in range(n)
    ]


def create_plot_info(df):
    mean_lst = bootstrap_test(df)
    mean, std = np.mean(mean_lst), np.std(mean_lst)
    normal = stats.norm(mean, std)
    x = np.linspace(np.min(mean_lst), np.max(mean_lst), 100)

    return normal, x, mean_lst, mean, std


def plot_bootstrap(df, ax, name="Bootstrap Test"):
    normal, x, mean_lst, mean, std = create_plot_info(df)
    ax.hist(mean_lst, density=True)
    ax.plot(
        x, normal.pdf(x), "r-", lw=5, alpha=0.6, label="norm pdf", color="black",
    )
    ax.set_xlabel("Time")
    ax.set_ylabel("Count")
    ax.set_title(name)


def welch_test_statistic(sample_1, sample_2):
    numerator = np.mean(sample_1) - np.mean(sample_2)
    denominator_sq = (np.var(sample_1) / len(sample_1)) + (
        np.var(sample_2) / len(sample_2)
    )
    return numerator / np.sqrt(denominator_sq)


def welch_satterhwaithe_df(sample_1, sample_2):
    ss1 = len(sample_1)
    ss2 = len(sample_2)
    df = ((np.var(sample_1) / ss1 + np.var(sample_2) / ss2) ** (2.0)) / (
        (np.var(sample_1) / ss1) ** (2.0) / (ss1 - 1)
        + (np.var(sample_2) / ss2) ** (2.0) / (ss2 - 1)
    )
    return df


def welch_test_statistic(sample_1, sample_2):
    numerator = np.mean(sample_1) - np.mean(sample_2)
    denominator_sq = (np.var(sample_1) / len(sample_1)) + (
        np.var(sample_2) / len(sample_2)
    )
    return numerator / np.sqrt(denominator_sq)


fig, ax_1 = plt.subplots()
fig, ax_2 = plt.subplots()
fig, ax_compare = plt.subplots(2, sharex=True, sharey=True)
for df, ax, name, ax2 in zip(
    [JMCSR_Any, JMCSR_AnyGl],
    [ax_1, ax_2],
    ["Glitched", "Glitchless"],
    ax_compare.flatten(),
):
    # plot_bootstrap(df, ax)
    plot_bootstrap(df, ax2, name)
plt.savefig("./images/hypotesting/bootstraptest.png")
plt.tight_layout()
# plt.show()
# Test wether the difference is significant
boot_any, boot_anygl = bootstrap_test(JMCSR_Any), bootstrap_test(JMCSR_AnyGl)

sem_any, sem_anygl = stats.sem(boot_any), stats.sem(boot_anygl)
degoffree = welch_satterhwaithe_df(boot_any, boot_anygl)
teststat = welch_test_statistic(boot_any, boot_anygl)
p_val = stats.ttest_ind(boot_any, boot_anygl)
print(sem_any, sem_anygl)
print(degoffree, teststat)
print(p_val)
plt.show()
# print(welch_test_statistic(boot_any, boot_anygl))
# -556.0919156975093
# 0.03995593835054164 0.033410421929411814
# 1937.2897306025372 -556.8467828075966
# Ttest_indResult(statistic=-556.5682897755202, pvalue=0.0)
