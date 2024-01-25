import streamlit as st
from trash.FTSCheng import semesta, mean, interval

st.header("Himpunan Semesta")
b1, b2 = st.columns([0.4, 0.6])
b1.markdown("**Dmin**")
b2.markdown(": " + str(semesta[0]))
b1.markdown("**Dmax**")
b2.markdown(": " + str(semesta[1]))
b1.markdown("**D1**")
b2.markdown(": 50")
b1.markdown("**D2**")
b2.markdown(": 150")
b1.markdown("**Mean**")
b2.markdown(": " + str(round(mean[1])))
b1.markdown("**Panjang Interval**")
b2.markdown(": " + str(round(interval[0])))
b1.markdown("**Jumlah Interval**")
b2.markdown(": " + str(round(interval[1])))

st.latex(
    r"""
    \text{Mean} = \frac{\sum_{t=1}^n (D_{t+1} - D_1)}{n}
    """
)
st.latex(
    r"""
    l = \frac{\text{Mean}}{2}
    """
)
st.latex(
    r"""
    p = \frac{(D_{\text{max}} + D_2) - (D_{\text{min}} + D_1)}{l}
    """
)
st.latex(
    r"""
    m_i = \frac{(\text{batas atas} + \text{batas bawah})}{2}
    """
)
st.latex(
    r"""
    A_i = \frac{\mu A_i(u_1)}{u_1} + \frac{\mu A_i(u_2)}{u_2} + \frac{\mu A_i(u_3)}{u_3} + \ldots + \frac{\mu A_i(u_n)}{u_n}

    """
)
st.latex(
    r"""
    \mu A_i(u_j) =
    \begin{cases}
    1 & \text{jika } (i = j) \text{ atau } (i = j - 1 \text{ atau } j + 1) \\
    0.5 & \text{untuk yang lainnya}
    \end{cases}
    """
)
st.latex(
    r"""
    A_1 = \frac{1}{u_1} + \frac{0.5}{u_2} + \frac{0.5}{u_3} + \frac{0.5}{u_4} + \ldots + \frac{0}{u_n}
    """
)

st.latex(
    r"""
    A_2 = \frac{0.5}{u_1} + \frac{1}{u_2} + \frac{0.5}{u_3} + \frac{0}{u_4} + \ldots + \frac{0}{u_n}
    """
)
st.latex(
    r"""
    A_3 = \frac{0}{u_1} + \frac{0.5}{u_2} + \frac{1}{u_3} + \frac{0.5}{u_4} + \ldots + \frac{0}{u_n}
    """
)
st.latex(
    r"""
    A_n = \frac{0}{u_1} + \frac{0}{u_2} + \frac{0}{u_3} + \frac{0}{u_4} + \ldots + \frac{0.5}{u_{n-1}} + \frac{1}{u_n}
    """
)
st.latex(
    r"""
    W = \begin{bmatrix}
        w_{11} & w_{21} & \cdots & w_{n1} \\
        w_{12} & w_{22} & \cdots & w_{n2} \\
        \vdots & \vdots & \ddots & \vdots \\
        w_{1n} & w_{2n} & \cdots & w_{nn}
    \end{bmatrix}
    """
)
st.latex(
    r"""
    W^* = \begin{bmatrix}
        w_{11^*} & w_{21^*} & \cdots & w_{n1^*} \\
        w_{12^*} & w_{22^*} & \cdots & w_{n2^*} \\
        \vdots & \vdots & \ddots & \vdots \\
        w_{1n^*} & w_{2n^*} & \cdots & w_{nn^*}
    \end{bmatrix}

    """
)
st.latex(
    r"""
    W_{ij^*} = \frac{w_{ij}}{\sum_{j=1}^n w_{ij}}
    """
)
st.latex(
    r"""
    F_i = W_{i1^*}(m_1) + W_{i2^*}(m_2) + \ldots + W_{in^*}(m_n)
    """
)
st.latex(
    r"""
    \text{Mape} = \frac{1}{n} \sum_{i=1}^n \left|\frac{D_i - F_i}{D_i}\right| \times 100\%
    """
)
