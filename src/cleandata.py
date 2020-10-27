import pandas as pd

(
    JMCSR_AnyGl_RS_1o16,
    JMCSR_AnyGl_RS_1o9t1o15,
    JMCSR_AnyGl_RS_p1o9,
    JMCSR_AnyGl_SS_1o9t1o15,
    JMCSR_AnyGl_SS_p1o9,
    JMCSR_Any_RS_1o9t,
    JMCSR_Any_RS_p1o9,
    JMCSR_Any_SS_1o9t,
    JMCSR_Any_SS_p1o9,
) = (
    pd.read_csv("./data/versions/JMCSR_AnyGl_RS_1.16.csv"),
    pd.read_csv("./data/versions/JMCSR_AnyGl_RS_1.9-1.15.csv"),
    pd.read_csv("./data/versions/JMCSR_AnyGl_RS_p1.9.csv"),
    pd.read_csv("./data/versions/JMCSR_AnyGl_SS_1.9-1.15.csv"),
    pd.read_csv("./data/versions/JMCSR_AnyGl_SS_p1.9.csv"),
    pd.read_csv("./data/versions/JMCSR_Any_RS_1.9-.csv"),
    pd.read_csv("./data/versions/JMCSR_Any_RS_p1.9.csv"),
    pd.read_csv("./data/versions/JMCSR_Any_SS_1.9-.csv"),
    pd.read_csv("./data/versions/JMCSR_Any_SS_p1.9.csv"),
)
JMCSR_AnyGl_RS, JMCSR_AnyGl_SS, JMCSR_Any_RS, JMCSR_Any_SS = (
    (
        JMCSR_AnyGl_RS_1o16.append(JMCSR_Any_RS_p1o9.append(JMCSR_AnyGl_RS_1o9t1o15))
    ).sort_values("Real time"),
    (JMCSR_AnyGl_SS_1o9t1o15.append(JMCSR_AnyGl_SS_p1o9)).sort_values("Real time"),
    (JMCSR_Any_RS_1o9t.append(JMCSR_Any_RS_p1o9)).sort_values("Real time"),
    (JMCSR_Any_SS_1o9t.append(JMCSR_AnyGl_SS_p1o9)).sort_values("Real time"),
)
JMCSR_AnyGl_RS.to_csv("./data/combined/JMCSR_AnyGl_RS.csv", index=False)
JMCSR_AnyGl_SS.to_csv("./data/combined/JMCSR_AnyGl_SS.csv", index=False)
JMCSR_Any_RS.to_csv("./data/combined/JMCSR_Any_RS.csv", index=False)
JMCSR_Any_SS.to_csv("./data/combined/JMCSR_Any_SS.csv", index=False)
